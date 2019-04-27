#!/usr/bin/env python3.7

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__='user'
    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    email =Column(String(150), nullable = True)
    picture = Column(String(250), nullable = True)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # serilizing catagory
    @property
    def serialize(self):

        return {
            'id': self.id,   
            'name': self.name,
        }



class CatItem(Base):
    __tablename__ = 'cat_item'

    title = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(550))
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    
    user_id =Column(Integer,ForeignKey('user.id'), nullable=True)
    user =relationship(User)

# serilizing item
    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }



class Log(Base):
    __tablename__='log'
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    item_id = Column(Integer,ForeignKey('cat_item.id'))
    item = relationship(CatItem)

    time = Column(DateTime, default=func.now())


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)

# to generate uml code plantuml use vscode extention
# http://www.plantuml.com
# if __name__ == '__main__':
#     import codecs
#     import sadisplay

#     desc = sadisplay.describe(globals().values())

#     with codecs.open('schema.plantuml', 'w', encoding='utf-8') as f:
#         f.write(sadisplay.plantuml(desc))
