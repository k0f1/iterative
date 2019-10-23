#! /usr/bin/env python2
# Using sqlalchemy - objected related mapping.

#######At begining of file#######

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# Make an instance - Base
Base = declarative_base()


class Restaurant(Base):
    """This class provide a way to store restaurant names"""

    __tablename__ = 'restaurant'

    # Mapping
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    # Instantiate the object of the class: self = Restaurant()

    @property # Add a decorator property
    def serialize(self): # Instance method that returns a dictionary
        """Returns object data in easily serializable format"""
        return {
            'name'        : self.name, # accessing instance attributes
            'id'          : self.id,
        }


class MenuItem(Base):
    """This class provide a way to store restaurant menu items. Same as Dishes table. The most suitable name here is Dishes"""

    __tablename__ = 'menu_item'

    # Mapping
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(25))
    description = Column(String(250))
    price = Column(String(8)) # This needed two decimal places ie Column(Decimal(3,2))
    # ingredients = Column(String(20)) allergy ingredient list
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to send JSON objects in
    # a serializable format. We do this before writing the JSON function in our flask app.
    @property
    def serialize(self):
        """Returns object data in easily serializable format"""
        return {
            'name'          : self.name,
            'description'   : self.description,
            'id'            : self.id,
            'price'         : self.price,
            'course'        : self.course,
        }

        # JSON stands for JavaScript object notation.
        # JSON uses attribute value pairings
        # which are delimited by a colon like so ":" as shown above.
        # Curly brackets are used to encapsulate individual objects
        # which you can see by going to localhost:5000/restaurants/1/menu/JSON



#######Insert at end of file #######

# Make an instance - engine. Point it to the database.
engine = create_engine ('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
