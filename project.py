import mock_data
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    return render_template("restaurants.html", restaurants=mock_data.restaurants)


@app.route('/restaurants/<int:restaurant_id>/new')
def newRestaurant(restaurant_id):
    return "New restaurant"


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "Edit restaurant"


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "Delete restaurant"


@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    return render_template("restaurant-menu.html", restaurant=mock_data.restaurant, menu_items=mock_data.items)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "New menu item"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit')
def editMenuItem(restaurant_id, menu_item_id):
    return "Edit menu item"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete')
def deleteMenuItem(restaurant_id, menu_item_id):
    return "Delete menu item"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
