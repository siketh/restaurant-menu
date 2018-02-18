from database_setup import Base, MenuItem, Restaurant
from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant)
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        name = request.form["name"]
        new_restaurant = Restaurant(name=name)

        session.add(new_restaurant)
        session.commit()

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

        return redirect(url_for('restaurants'))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return render_template("delete-restaurant.html", restaurant=restaurant)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template("restaurant.html", restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu')
def menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

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

        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == "GET":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_item_id).one()

        return render_template("delete-menu-item.html", restaurant=restaurant, menu_item=menu_item)
    else:
        return "Request method [{}] not supported!".format(request.method)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/')
def menuItem(restaurant_id, menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_item_id).one()

    return render_template("menu-item.html", restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
