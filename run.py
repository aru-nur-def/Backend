from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/umayshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    item_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "customer_name": o.customer_name, "item_name": o.item_name, "quantity": o.quantity} for o in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(customer_name=data["customer_name"], item_name=data["item_name"], quantity=data["quantity"])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
