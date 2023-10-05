from flask import Flask,render_template,request,redirect
from flask import current_app as app
from application.models import *
import matplotlib.pyplot as plt

@app.route("/",methods=["GET"])
def index():
    return render_template("page1.html")
    
@app.route("/admin",methods=["GET","POST"])
def adminindex():
    if request.method=="GET":
        return render_template("admin_login.html")
    elif request.method=="POST":
        managers=Admin.query.all()
        username=request.form.get("username")
        password=request.form.get("password")
        if username==managers[0].username:
            if password==managers[0].password:
                return redirect("/admin/dashboard")
            else:
                return render_template("admin_login.html",message="password")
        else:
            return render_template("admin_login.html",message="username")
        

@app.route("/admin/dashboard",methods=["GET"])
def admin_dashboard():
    categories=Category.query.all()
    return render_template("admin_dash.html",categories=categories)

@app.route("/admin/create",methods=["GET","POST"])
def create():
    if request.method=="GET":
        return render_template("create_category.html")
    elif request.method=="POST":
        c_name=request.form.get("name")
        if c_name=="":
            return redirect("/admin/dashboard")
        else:
            c1=Category(name=c_name)
            try:
                db.session.add(c1)
                db.session.commit()
                return redirect("/admin/dashboard")
            except:
                db.session.rollback()
                message=f"{c_name} already exists"
                return render_template("create_category.html",message=message)

@app.route("/admin/edit",methods=["GET","POST"])
def edit():
    if request.method=="GET":
        categories=Category.query.all()
        return render_template("edit_and_delete_category.html",categories=categories)
    elif request.method=="POST":
        categories=Category.query.all()
        if request.form.get("category")=="0":
            return render_template("edit_and_delete_category.html",categories=categories,message="No Category Selected")
        else:
            cat_id=request.form.get("category")
            c1=Category.query.get(int(cat_id))
            action=request.form.get("action")
            if action=="edit":
                new_name=request.form.get("new_name")
                if new_name=="":
                    return redirect("/admin/dashboard")
                try:
                    c1.name=new_name
                    db.session.commit()
                    return redirect("/admin/dashboard")
                
                except:
                    db.session.rollback()
                    message=f"{new_name} already exists"
                    return render_template("edit_and_delete_category.html",message=message)
            
            elif action=="delete":
                if c1.items==0:
                    
                    db.session.delete(c1)
                    db.session.commit()
                else:
                    items=c1.items
                    for p in c1.items:
                        db.session.delete(p)
                    db.session.commit()
                    db.session.delete(c1)
                    db.session.commit()
        return redirect("/admin/dashboard")
    
@app.route("/admin/add_product/<int:id>",methods=["GET","POST"])
def add_products(id):
    c1=Category.query.get(id)
    if request.method=="GET":
        return render_template("add_product.html",c=c1)
    elif request.method=="POST":
        p_name=request.form.get("name")
        p_unit=request.form.get("unit")
        p_cost=request.form.get("cost")
        p_quantity=request.form.get("quantity")
        if p_name=="" or p_cost=="" or p_quantity=="":
            message="Empty Input!"
            return render_template("add_product.html",message=message,c=c1)
        if p_cost==0:
            message="Cost can not be 0!"
            return render_template("add_product.html",message=message,c=c1)
        try:
            p1=Product(name=p_name,unit=p_unit,cost=int(p_cost),quantity=int(p_quantity),category_id=int(id))
            db.session.add(p1)
            db.session.commit()
            return redirect("/admin/dashboard")  
        except:
            db.session.rollback()
            message=f"{p_name} already exists!"
            return render_template("add_product.html",message=message,c=c1,newname=p_name)

      

@app.route("/admin/delete_product/<int:id>",methods=["GET"])
def delete_product(id):
    p1=Product.query.get(id) 
    db.session.delete(p1)
    db.session.commit()
    return redirect("/admin/dashboard") 

@app.route("/admin/edit_product/<int:id>",methods=["GET","POST"])
def edit_product(id):
    if request.method=="GET":
        p=Product.query.get(id)
        return render_template("edit_product.html",p=p)
    elif request.method=="POST":
        p=Product.query.get(id)
        p_name=request.form.get("name")
        p_unit=request.form.get("unit")
        p_cost=request.form.get("cost")
        p_quantity=request.form.get("quantity")
        if p_name=="" or p_cost=="" or p_quantity=="":
            message="Empty Input!"
            return render_template("edit_product.html",message=message,p=p)
        if int(p_cost)==0:
            message="Cost can not be 0!"
            return render_template("edit_product.html",message=message,p=p)
        
        p.name=p_name
        p.unit=p_unit
        p.cost=p_cost
        p.quantity=p_quantity
        try:
            db.session.commit()
            return redirect("/admin/dashboard")
        except:
            db.session.rollback()
            message=f"{p_name} already exists!"
            return render_template("edit_product.html",message=message,p=p)
        
@app.route("/admin/summary",methods=["GET"])
def summary():
    bought=Bought.query.all()
    volume={}
    revenue={}
    for b in bought:
        if b.product.product_type.name in volume.keys():
            volume[b.product.product_type.name]+=b.quantity
        else:
            volume[b.product.product_type.name]=b.quantity
        if b.product.product_type.name in revenue.keys():    
            revenue[b.product.product_type.name]+=b.total_cost
        else:
            revenue[b.product.product_type.name]=b.total_cost

    labels1 = list(volume.keys())
    values1 = list(volume.values())

    labels2 = list(revenue.keys())
    values2 = list(revenue.values())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.bar(labels1, values1, color='b')
    ax1.set_title('Volumes sold by categories')
    ax1.set_xlabel('categories')
    ax1.set_ylabel('volumes sold')

    ax2.bar(labels2, values2, color='g')
    ax2.set_title('revenue generated by category')
    ax2.set_xlabel('categories')
    ax2.set_ylabel('revenue')

    plt.tight_layout()
    plt.savefig('static/bar_charts.png')  
    path='static/bar_charts.png'     

    return render_template("summary.html",path=path)


@app.route("/admin/clear_transaction_records",methods=["GET"])
def reset():
    o=Order.query.all()
    b=Bought.query.all()
    for _ in b:
        db.session.delete(_)
    db.session.commit()
    for _ in o:
        db.session.delete(_)
    db.session.commit()

    return redirect("/admin/dashboard")

