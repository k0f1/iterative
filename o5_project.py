#! /usr/bin/env python2
# Message Flashing

# Good applications and user interfaces,
# incorporate feedback throughout the user experience
# We should add a feature that explicitly notifies
# the user that the system has responded to thier input.
# Message Flashing is a feature of flask
# that will prompt a message to the user immediately,
# after a certain action has taken place, and
# then disappear the next time the page is requested.

# We can use our template to reveal a flash message,
# wherever and however we want, from within the
# aplication.
# To get started, lets import flash from our flask module.

# --sessions-- concept
# Flashing works in Flask by using a concept, called sessions.
# sessions are a way a server can store information
# accross multiple web pages, to create a more
# personalised user experience.

# Secret key
# In the bottom of our project.py file,
# lets first add a secret key just under __name__ = __main__
# which flask will use to create sessions for our users.
# Normally, this should be a very secure password,
# if our application was live on the internet,
# but for development purposes,
# let's just set our key to super_secret_key.
# >>> app.secret_key = 'super_secret_key'

# The flash methods
# To flash the message within our application,
# we simply use the flash function like this.
# >>> flash("insert message here")

# To get a hold of all the flash messages, we can use
# >>> get_flashed_messages(),
# which also work from our templates.

# Where to add flash()
# From within my newMenuItem method, I will create a flash message
# right after I call, session.commit.
# I will add the message, ("new menu item created!)" now,
# In my menu.html template, I will add code show in my menu.html

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import these classes
from database_setup import Base, Restaurant, MenuItem

# Create these instances
# 1. Create an instance of Flask class
app = Flask(__name__)

# 2. Create an instance of create_engine
# This lets our program know which database engine
# we want to communicate with.
engine = create_engine('sqlite:///restaurantmenu.db')

# Then, lets bind the engine to the Base class
# with the following command: Base.metadata.bind=engine.
# This command just makes the connections
# between our class definitions and the
# corresponding tables within our database
Base.metadata.bind = engine

# 3. create a sessionmaker object/instance  called DBsession.
# This establishes a link of communication
# between our code executions and the engine
# we have just created.
# DBsession much like declarative Base is a class.
DBSession = sessionmaker(bind=engine)

# 4. Create an instance of DBsession class.
# In order to perform CRUD on our database,
# SQLAlchemy executes database operations via
# an interface called a session.
# A session allows us to write down all the commands
# we want to execute, but not send them to the database
# until we call a commit. I will create an instance
# of a DBsession and call it session for short.
# From now on, when I want to make a change to my database,
# I can do it by just calling a method from within session.
# The BDsession object gives me a staging zone
# for all of the objects loaded into a database session object.
session = DBSession()

@app.route('/')
# The route decorator is used to bind
# a function to URL.
# We can make certain parts of the URL dynamic

# Restful API - (Representational State Transfer)
# Sometimes are that needs to be communicated is information.
# For example, let's say there's a webapp out there called Yum
# that wants to collect our restaurant menus and
# advertise them to mobile clients based on thier location.
# This app wants to see the restaurants and menus available
# in our database but doesn't really need to parse through HTML
# or waste bandwidth receiving CSS files. It just wants the data.
# For this reason, developers have  created APIs, or
# Application Programming Interfaces, that allow external
# aaplications to use public information our apps want to share,
# without all the bells and whistles.
# When an API is communicated over the Internet, following
# the rules of HTTP, we call this restful API.

# Responding with JSON
# One of the most popular ways of sending data with a
# restful architecture is with the format called JSON,
# which stands for JavaScript object notation.
# JSON uses attribute value pairings which are delimited by a colon.
# Brackets are used to encapsulate individual objects.
# Before writing JSON function in our Flask menu app,
# let's firstopen up the databse setup.py add a decorator method.
# This serializable function will help define what data we want
# to send across, and put it in a format that Flask can easily use.
# Flask has a built-in package, called jsonify, that will allow us to
# easily configure an API endpoint for our application.
# For this lesson we will focus only on get request to get a
# collection of menu items.


# Making an API Endpoint
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
	"""Making an API Endpoint (GET Request)"""
	restaurants = session.query(Restaurant).all()
	# But instead of returning a template, I will return this jsonify class
	# and use this loop to serialize all of my database entries.
	return jsonify(Restaurants = [r.serialize() for r in restaurants])
	# The quote infron of serialize is because we are acessing an instance method.



@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
# Create a route similar to my restaurant menu page with backslash
# JSON at the end /JSON.
# Then create a function and name it restaurant menu JSON and
# then perform the same query as in my restaurant menu class.
def restaurantMenuJSON(restaurant_id):
	"""Making all Dishes API Endpoint (GET Request)"""
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize() for i in items]) # Returns all menu items of the restaurant we are looking at.

# Add a menu item API Endpoint Here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id): # Becuase both args are in the method
	"""Making a menu item API Endpoint (GET Request)"""
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	# Then perform a query to get one menu ID that I want to get
	# information about. Then jsonify that menu item, but serializing it first.
	return jsonify(MenuItem = menuItem.serialize())

# Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	# Add CRUD Functionality
	# SQLAlchemy statements
	restaurants = session.query(Restaurant).all()
	# return "This page will show all my restaurants"
	return render_template('restaurants.html', restaurants = restaurants)# since
	# I am querying on my restaurant table, I will path my query into the template, so that my escape code has access to this variable.



@app.route('/restaurants/new', methods = ['GET', 'POST'])
def newRestaurant():
    # Add CRUD Functionality
    # SQLAlchemy statements
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        # Using url_for method requires you to pass the function it serves
        # and it parameters if any.
        return redirect(url_for('showRestaurants')) # This function has no args.
    else:
        # return "This page will be for making a new restaurant"
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    # Add CRUD Functionality
    # SQLAlchemy statements
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.add(editedRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		# return "This page will be for editing restaurant %s" %restaurant_id
		return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurant = editedRestaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # Add CRUD Functionality
    # SQLAlchemy statements
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		# return "This page will be for deleting restaurant %s" %restaurant_id
		return render_template('deleteRestaurant.html', restaurant_id  = restaurant_id, restaurant = restaurantToDelete)



@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
# Use restaurant_id to specify which
# menu I want to see.
# It is handy to leave the trailing slash
# Make certain parts of the URL dynamic like above,
# and attach multiple rules to a function as below.
# By adding variables to URL.
# By specifying a rule with - type: variable_name,
# "path/<type:variable_name>/path".
# Where type can be - an integer, string or another path.

def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	# Instead of returning a string output, I will return render_template.
	return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id) # Since I am querying on my restaurant
	# and menu items table,
	# I will path my queries into the template, so that my escape code has
	# access to these variables. These are the variables from
	# the queries and my route decorator.

	# I will also need to import render_template from our flask libarary

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = 	request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		# To properly handle the GET request.
		# If my server didn't receive a POST request, it going to go ahead and render the newMenuItem html template I have just created as a GET request.
		return render_template('newMenuItem.html', restaurant_id =  restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']: # dict['name'] key to access its value pair.
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.descrition = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course =request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu Item has been edited")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu Item has been deleted")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:# If it is a get request, I will go ahead and render that
	# deleteMenuitem.html file with the item i want to delete.
		return render_template('deleteMenuItem.html', i = itemToDelete)



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(threaded=False)
	app.run(host='0.0.0.0', port=5000)
