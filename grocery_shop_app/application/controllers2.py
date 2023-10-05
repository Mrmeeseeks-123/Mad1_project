from flask import Flask,render_template,request,redirect
from flask import current_app as app
from application.models import *

@app.route("/user",methods=["GET","POST"])
def user_index():
    if request.method=="GET":
        return render_template("user_login.html")
    elif request.method=="POST":
        users=User.query.all()
        username=request.form.get("username")
        password=request.form.get("password")
        for u in users:
            if u.username==username:
                if u.password==password:
                    path=f"/user/{u.u_id}"
                    return redirect(path)
                else:
                    return render_template("user_login.html",message="password")
        return render_template("user_login.html",message="username")
    
@app.route("/user/register",methods=["GET","POST"])
def register_user():
    if request.method=="GET":
        return render_template("register_user.html")
    elif request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        name=request.form.get("name")
        users=User.query.all()
        for u in users:
            if u.username==username:
                return render_template("register_user.html",message="username already exists!")
        u1=User(username=username,name=name,password=password)
        db.session.add(u1)
        db.session.commit()
        return redirect("/user")

@app.route("/user/<int:id>",methods=["GET","POST"])
def user_dashboard(id):
    if request.method=="GET":
        u=User.query.get(id)
        categories=Category.query.all()
        return render_template("user_dashboard.html",u=u,categories=categories)
    
@app.route("/user/<int:uid>/<int:pid>",methods=["GET","POST"])
def add_product_to_cart(uid,pid):
    u=User.query.get(uid)
    p=Product.query.get(pid)
    if request.method=="GET":
        return render_template("add_product_to_cart.html",u=u,p=p)
    if request.method=="POST":
        quantity=request.form.get("quantity")
        if quantity=="":
            message="Empty Input!"
            return render_template("add_product_to_cart.html",u=u,p=p,message=message)
        elif int(quantity)>p.quantity:
            message='Can not order more than the total stock!'
            return render_template("add_product_to_cart.html",u=u,p=p,message=message)
        elif int(quantity)==0:
            path=f'/user/{u.u_id}/{p.p_id}'
            return redirect(path)
        else:
            try:
                totalcost=int(quantity)*p.cost

                cart_item=Cart(user_id=u.u_id,product_id=p.p_id,quantity=int(quantity),total_cost=totalcost)
                db.session.add(cart_item)
                p.quantity-=int(quantity)
                db.session.commit()
                path=f'/user/{u.u_id}'
                return redirect(path)
            except:
                message="cannot book order!"
                return render_template("add_product_to_cart.html",u=u,p=p,message=message)
@app.route("/user/<int:id>/cart",methods=["GET","POST"])
def user_cart(id):
    if request.method=="GET":
        u=User.query.get(id)
        cart=Cart.query.filter_by(user_id=u.u_id).all()
        grand_total=0
        for c in cart:
            grand_total+=c.total_cost
        if request.method=="GET":
            return render_template("user_cart.html",u=u,cart=cart,grand_total=grand_total)
    elif request.method=="POST":
        u=User.query.get(id)
        cart=Cart.query.filter_by(user_id=u.u_id).all()
        grand_total=0
        for c in cart:
            grand_total+=c.total_cost
        
        o1=Order(user_id=u.u_id,total_cost=grand_total)
        db.session.add(o1)
        db.session.commit()
        
        for c in cart:
            b1=Bought(user_id=c.user_id,product_id=c.product_id,quantity=c.quantity,total_cost=c.total_cost,order_id=o1.o_id)
            db.session.add(b1)
            o1.items.append(b1)

        for c in cart :
            db.session.delete(c)

        db.session.commit()

        u=User.query.get(id)
        cart=Cart.query.filter_by(user_id=u.u_id).all()
        grand_total=0
        for c in cart:
            grand_total+=c.total_cost
        return render_template("user_cart.html",u=u,cart=cart,grand_total=grand_total)
            
        # except:
        #     db.session.rollback()
        #     message="Failed!"
        #     return render_template("user_cart.html",u=u,cart=cart,grand_total=grand_total,message=message)

@app.route("/user/<int:uid>/<int:cid>/del",methods=["GET"])
def del_product_from_cart(uid,cid):
    c=Cart.query.get(cid)
    q=c.quantity
    p=c.product
    p.quantity=p.quantity+q
    db.session.delete(c)
    db.session.commit()
    path=f'/user/{uid}/cart'
    return redirect(path)

@app.route("/user/<int:id>/profile",methods=["GET"])
def user_profile(id):
    if request.method=="GET":
        u=User.query.get(id)
        orders=Order.query.filter_by(user_id=u.u_id).all()
        return render_template("user_profile.html",u=u,orders=orders)
    



