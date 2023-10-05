from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Admin(db.Model):
    a_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)

class Category(db.Model):
    c_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    items=db.relationship("Product",backref="product_type")

class Product(db.Model):
    p_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False,unique=True)
    category_id=db.Column(db.Integer,db.ForeignKey("category.c_id"),nullable=False)
    unit=db.Column(db.String(6),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    cost=db.Column(db.Integer,nullable=False)

    

class User(db.Model):
    u_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False,unique=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    

class Cart(db.Model):
    c_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.u_id"))
    product_id=db.Column(db.Integer,db.ForeignKey("product.p_id"))
    quantity=db.Column(db.Integer,nullable=False)
    total_cost=db.Column(db.Integer,nullable=False)
    product=db.relationship("Product")

class Bought(db.Model):
    b_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.u_id"))
    product_id=db.Column(db.Integer,db.ForeignKey("product.p_id"))
    quantity=db.Column(db.Integer,nullable=False)
    total_cost=db.Column(db.Integer,nullable=False)
    order_id=db.Column(db.Integer,db.ForeignKey("order.o_id"),nullable=False)
    product=db.relationship("Product")

class Order(db.Model):
    o_id=db.Column(db.Integer,primary_key=True)
    user_id=user_id=db.Column(db.Integer,db.ForeignKey("user.u_id"))
    items=db.relationship("Bought",backref="order",secondary="association")
    total_cost=db.Column(db.Integer,nullable=False)

class Association(db.Model):
    order_id=db.Column(db.Integer,db.ForeignKey("order.o_id"),primary_key=True)
    bought_id=db.Column(db.Integer,db.ForeignKey("bought.b_id"),primary_key=True)