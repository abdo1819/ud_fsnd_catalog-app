#!/usr/bin/env python3.7
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, CatItem
from flask import session as login_session

import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
import requests

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
# prevent auto sorting from jsonify
app.config['JSON_SORT_KEYS'] = False


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
    return render_template("categories.html", categories=categories)

# http://localhost:5000/catalog/BASKETBALL/items
@app.route('/catalog/<string:category_name>/items')
def showCatItems(category_name):
    catagory = session.query(Category).filter_by(name=category_name).one()
    catItems = session.query(CatItem).filter_by(cat_id=catagory.id).all()
    return render_template("catItems.html",
                           catItems=catItems, category=catagory)

# http://localhost:5000/catalog/BASKETBALL/Basketballs
@app.route('/catalog/<string:category_name>/<string:item_title>')
def showItemDetail(category_name, item_title):
    catItem = session.query(CatItem).filter_by(title=item_title).one()
    return render_template("catItem_user.html", catItem=catItem)

# http://localhost:5000/catalog/Basketballs/edit
@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
def editItem(item_title):
    # TODO check if user
    catItem = session.query(CatItem).filter_by(title=item_title).one()
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
                               catItem=catItem, categories=categories)


# http://localhost:5000/catalog/Basketballs/edit
@app.route('/catalog/<string:category_name>/add', methods=['GET', 'POST'])
def addItem(category_name):
    # TODO check if user
    catItem = CatItem()
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
        # for preselecting current catagory
        selected_catagory = session.query(Category).filter_by(name = category_name).one()
        
        categories = session.query(Category).all()
        return render_template('addItem.html',
                               categories=categories,selected_id =selected_catagory.id )





# http://localhost:5000/catalog/Basketballs/delete
@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
def deleteItem(item_title):
    # check if user
    catItem = session.query(CatItem).filter_by(title=item_title).one()
    catagory = session.query(Category).filter_by(id=catItem.cat_id).one()
    if request.method == 'POST':
        session.delete(catItem)
        session.commit()
        flash('item Successfully deleted %s' % catItem.title)
        return redirect(url_for('showCatItems', category_name=catagory.name))

    else:
        return render_template('delete_item.html',
                               catagory=catagory, catItem=catItem)
    pass


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
