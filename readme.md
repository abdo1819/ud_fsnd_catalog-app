# project catalog for sport items
## description 
this is a website shows sports catagories with main equipment reqierd for sport and some details about it
and the ability to edit/add items

# running project
## prereqirment 

> python interpeter: python3.7

### main pakages you may user /requirment.txt
> SQLAlchemy==1.3.3

> Flask==1.0.2

> httplib2==0.12.1

> oauth2client==4.1.3
* for uml diagram (optional)
> sadisplay==0.4.9

## create database and fill some data(optional *use catalog.db)
> ```python3.7 db_setup.py``` 

> ```python3.7 data.py```

## start server
> ```python3.7 application.py```

## open homepage by visiting in browser
[localhost:5000](http://localhost:5000/)
* don't use __0.0.0.0:5000__ for google aouth2 to work
 
[catalog in json](http://localhost:5000/catalog/json)

[](/category/<int:category_id>/items/json)

<!-- TODO recent created -->
 # site pages
