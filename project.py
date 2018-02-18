from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    # Fake Restaurants
    restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

    restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
        'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]

    # Fake Menu Items
    items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables',
                                                                                                                                                                                                                                                            'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
    item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
            'price': '$5.99', 'course': 'Entree'}
    return render_template("restaurants.html", restaurants=restaurants)


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
    return "Restaurant menu"


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
