from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import os, json, uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

app = Flask(__name__)
PRODUCTS_FILE = 'products.json'
app.secret_key = "test"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Snakehead505@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    images = db.Column(ARRAY(db.String))
    itemtype = db.Column(db.String)

    def __init__(self, name, price, description, images, itemtype):
        self.id = uuid.uuid4().hex
        self.name = name
        self.price = price
        self.description = description
        self.images = images
        self.itemtype = itemtype

@app.route("/test-db") #test db connection
def test_db():
    products = Product.query.all()
    return f"Found the database!"

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products = products)

@app.route("/product/<product_id>")
def product_page(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product = product)

@app.route("/admin", methods = ["GET", "POST"])
def admin():
    if not session.get("ok"):
        return redirect("/login")
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        images = request.files.getlist('images')
        itemtype = request.form['itemtype']

        image_urls = []
        for image in images:
            filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            path = os.path.join("static/uploads", filename)
            image.save(path)
            image_urls.append(f'/static/uploads/{filename}')
        
        new_product = Product(name = name, price = price, description = description, images = image_urls, itemtype = itemtype) 
        db.session.add(new_product)
        db.session.commit()
        return redirect("/admin")
    products = Product.query.all()

    return render_template('admin.html', products = products)

@app.route("/delete/<product_id>", methods = ["POST"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/admin")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form['password']
        if password == 'testpw':
            session['ok'] = True
            return redirect("/admin")
        else:
            flash("Wrong password. Try again.")
            return redirect('/login')
    return render_template('login.html')

@app.route("/login-redirect")
def home():
    if session['ok']: 
        return redirect("/admin")
    else:
        return redirect("/login")  

@app.route("/item1")
def item1():
    products = Product.query.filter_by(itemtype = "item1").all()
    return render_template("item1.html", products = products)


@app.route("/item2")
def item2():
    products = Product.query.filter_by(itemtype = "item2").all()
    return render_template("item2.html", products = products)


@app.route("/item3")
def item3():
    products = Product.query.filter_by(itemtype = "item3").all()
    return render_template("item2.html", products = products)


if __name__ == '__main__':
    app.run(debug = True)