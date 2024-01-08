
from flask import Flask,render_template,request,redirect
from flask import current_app as app
from application.models import *
import matplotlib.pyplot as plt

@app.route("/search",methods=["GET"])
def search():
    q=request.args.get("query")
    query="%"+q+"%"
    result=Product.query.filter(Product.name.like(query)).all()
    return render_template("search_result.html",result=result,q=q)