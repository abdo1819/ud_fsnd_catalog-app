#!/usr/bin/env python3.7
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, CatItem, User,Log
from flask import session as login_session

import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
import requests

# CLIENT_ID ='907678801306-969cb2rticgq17i9849rnqb9t5el0eig.apps.googleusercontent.com'
client_secret = 'FMAIQ8H77ib2Nqo0gr8J5E3F'
CLIENT_ID = json.loads(
    open('credentials.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "app name"

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
# prevent auto sorting from jsonify
app.config['JSON_SORT_KEYS'] = False



# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None




@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,login_session=login_session)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    
    
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('credentials.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/disconnect')
def disconnect():
    if 'gplus_id' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))






@app.route('/catalog/json')
def categoryJSON():
    categories = session.query(Category).all()
    json_catagory = [c.serialize for c in categories]
    count = 0

    for cataoery in categories:
        items = session.query(CatItem).filter_by(cat_id=cataoery.id).all()
        json_catagory[count].update({'Items':[i.serialize for i in items]})
        count +=1

    return jsonify(cataoeries = json_catagory)
    

@app.route('/category/<int:category_id>/items/json')
def categoryItemsJSON(category_id):
    items = session.query(CatItem).filter_by(cat_id=category_id).all()
    return jsonify(categories_items=[i.serialize for i in items])

# Show all categories
# http://localhost:5000/catalog/
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    log = session.query(CatItem).join(Log).order_by(desc(Log.time)).all()
    not_user=True
    if 'username' in login_session:
        not_user=False

    return render_template("categories.html", categories=categories,log=log,not_user=not_user,login_session=login_session)

# http://localhost:5000/catalog/BASKETBALL/items
@app.route('/catalog/<string:category_name>/items')
def showCatItems(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    catagory = session.query(Category).filter_by(name=category_name).one()
    catItems = session.query(CatItem).filter_by(cat_id=catagory.id).all()
    not_user=True
    if 'username' in login_session:
        not_user=False
    count = len(catItems)
    return render_template("catItems.html",
                           catItems=catItems, category=catagory,categories=categories
                           ,count=count,not_user=not_user,login_session=login_session)

# http://localhost:5000/catalog/BASKETBALL/Basketballs
@app.route('/catalog/<string:category_name>/<string:item_title>')
def showItemDetail(item_title,category_name=None):
    catItem = session.query(CatItem).filter_by(title=item_title).one()
    itemOwner = session.query(User).filter_by(id=catItem.user_id).one()
    not_owner=True
    not_user=True
        
    if 'username' in login_session:
        not_user=False
        log = Log(item= catItem,user=getUserInfo(login_session['user_id']))    
        session.add(log)
        session.commit()    
        if  itemOwner.id == login_session['user_id']:
            not_owner=False

    return render_template("catItem_user.html", catItem=catItem,not_user=not_user,login_session=login_session,not_owner=not_owner)

# http://localhost:5000/catalog/Basketballs/edit
@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
def editItem(item_title):
    if 'username' not in login_session:
        return redirect('/login')
    catItem = session.query(CatItem).filter_by(title=item_title).one()
    if login_session['user_id'] != catItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add menu items to this restaurant. Please create your own restaurant in order to add items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        print(request.form)
        if request.form['title']:
            catItem.title = request.form['title']
        if request.form['description']:
            catItem.description = request.form['description']
        if request.form['catagory_id']:
            catItem.cat_id = request.form['catagory_id']
        session.add(catItem)
        session.commit()
        flash('item Successfully Edited %s' % catItem.title)
        catagory = session.query(Category).filter_by(id=catItem.cat_id).one()

        return redirect(url_for('showCatItems', category_name=catagory.name))

    # handling get request for edit page
    else:
        categories = session.query(Category).all()
        return render_template('edit_item.html',
                               catItem=catItem, categories=categories,login_session=login_session)


# http://localhost:5000/catalog/Basketballs/edit
@app.route('/catalog/<string:category_name>/add', methods=['GET', 'POST'])
def addItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    catItem = CatItem()
    if request.method == 'POST':
        print(request.form)
        if request.form['title']:
            catItem.title = request.form['title']
        if request.form['description']:
            catItem.description = request.form['description']
        if request.form['catagory_id']:
            catItem.cat_id = request.form['catagory_id']
        catItem.user_id = login_session['user_id']
        session.add(catItem)
        session.commit()
        flash('item Successfully added %s' % catItem.title)
        catagory = session.query(Category).filter_by(id=catItem.cat_id).one()

        return redirect(url_for('showCatItems', category_name=catagory.name,login_session=login_session))

    # handling get request for edit page
    else:
        #  selecting current catagory by default
        selected_catagory = session.query(Category).filter_by(name = category_name).one()
        
        categories = session.query(Category).all()
        return render_template('addItem.html',
                               categories=categories,selected_id =selected_catagory.id,login_session=login_session )





# http://localhost:5000/catalog/Basketballs/delete
@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
def deleteItem(item_title):
    if 'username' not in login_session:
        return redirect('/login')
    catItem = session.query(CatItem).filter_by(title=item_title).one()
    if login_session['user_id'] != catItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add menu items to this restaurant. Please create your own restaurant in order to add items.');}</script><body onload='myFunction()'>"
    catagory = session.query(Category).filter_by(id=catItem.cat_id).one()
    if request.method == 'POST':
        session.delete(catItem)
        session.commit()
        flash('item Successfully deleted %s' % catItem.title)
        return redirect(url_for('showCatItems', category_name=catagory.name))

    else:
        return render_template('delete_item.html',
                               catagory=catagory, catItem=catItem,login_session=login_session)
    pass


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
