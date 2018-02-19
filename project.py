from database_setup import Base, MenuItem, Restaurant
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# REST API Routes


@app.route('/restaurants/JSON')
def restaurantsJson():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurants=[restaurant.serialize])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menuItemsJson(restaurant_id):
    menu_items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[menu_item.serialize for menu_item in menu_items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def menuItemJson(restaurant_id, menu_item_id):
    menu_item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_item_id).one()
    return jsonify(MenuItems=[menu_item.serialize])


# Page Routes


@app.route('/')
@app.route('/restaurants/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurants(restaurant_id=None):
    if restaurant_id is None:
        restaurants = session.query(Restaurant)
    else:
        restaurants = session.query(
            Restaurant).filter_by(id=restaurant_id)
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        name = request.form["name"]
        new_restaurant = Restaurant(name=name)

        session.add(new_restaurant)
        session.commit()

        flash("New restaurant created successfully!")

        return redirect(url_for('restaurants'))
    elif request.method == "GET":
        return render_template("new-restaurant.html")
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == "POST":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()

        if(request.form["name"]):
            restaurant.name = request.form["name"]

        session.add(restaurant)
        session.commit()

        flash("Edited restaurant successfully!")

        return redirect(url_for('restaurants'))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return render_template("edit-restaurant.html", restaurant=restaurant)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == "POST":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()

        session.delete(restaurant)
        session.commit()

        flash("Deleted restaurant successfully!")

        return redirect(url_for('restaurants'))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return render_template("delete-restaurant.html", restaurant=restaurant)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/menu')
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/')
def menu(restaurant_id, menu_item_id=None):
    restaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()

    if menu_item_id is None:
        menu_items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id)
    else:
        menu_items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_item_id)

    return render_template("menu.html", restaurant=restaurant, menu_items=menu_items)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        course = request.form["course"]

        new_menu_item = MenuItem(
            name=name, description=description, price=price, course=course, restaurant_id=restaurant_id)

        session.add(new_menu_item)
        session.commit()

        flash("New menu item created successfully!")

        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()

        return render_template("new-menu-item.html", restaurant=restaurant)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id):
    if request.method == "POST":
        menu_item = session.query(MenuItem).filter_by(
            id=menu_item_id, restaurant_id=restaurant_id).one()

        if request.form["name"]:
            menu_item.name = request.form["name"]
        if request.form["description"]:
            menu_item.description = request.form["description"]
        if request.form["price"]:
            menu_item.price = request.form["price"]
        if request.form["course"]:
            menu_item.course = request.form["course"]

        session.add(menu_item)
        session.commit()

        flash("Edited menu item successfully!")

        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_item_id).one()

        return render_template("edit-menu-item.html", restaurant=restaurant, menu_item=menu_item)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id):
    if request.method == "POST":
        menu_item = session.query(MenuItem).filter_by(
            id=menu_item_id, restaurant_id=restaurant_id).one()

        session.delete(menu_item)
        session.commit()

        flash("Deleted menu item successfully!")

        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_item_id).one()

        return render_template("delete-menu-item.html", restaurant=restaurant, menu_item=menu_item)
    else:
        return "Request method [{}] not supported!".format(request.method)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "secretkey"
    app.run(host='0.0.0.0', port=5000)
