from flask import Flask, request, jsonify
import products_dao
import uom_dao
from sql_connection import get_sql_connection
import json
import orders_dao

app = Flask(__name__)

connection = get_sql_connection()


@app.route('/getProducts',methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


@app.route('/getUOM', methods = ['GET'])
def get_uom():
    response = uom_dao.get_ums(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


@app.route('/deleteProduct',methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'Product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'Product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting pyhon Flask server for pharmacy store management system")
    app.run(port=5000)