from datetime import datetime
from sql_connection import get_sql_connection


def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO orders "
                   "(customer_name,total,date_time)"
                   "VALUES (%s,%s,%s)")
    order_data = (order['customer_name'], order['total'], datetime.now())
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s,%s,%s,%s)")
    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            int(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])

    cursor.executemany(order_details_query, order_details_data)

    connection.commit()
    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()
    query = ("SELECT * from order_details where order_id = %s")
    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
             "products.name, products.price_per_unit FROM order_details LEFT JOIN products on "\
             "order_details.product_id = products.product_id where order_details.order_id = %s"
    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * from orders")
    cursor.execute(query)

    responses = []
    for (order_id, customer_name, total, datetime) in cursor:
        responses.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': datetime,
        })

    cursor.close()

    for response in responses:
        response['order_details'] = get_order_details(connection, response['order_id'])
    return responses


if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))