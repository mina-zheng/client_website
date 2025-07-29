from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import os, json, uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

app = Flask(__name__)
PRODUCTS_FILE = 'products.json'

load_dotenv()
print(os.environ.get("SQL_URL"))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQL_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key = True)
    password = db.Column(db.String)

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

"""@app.route("/create-user")
def create_user():
    if Users.query.get("1"):
        return "User already exists."
    hashed_pw = generate_password_hash(os.environ.get("ADMIN_PASSWORD"))
    user = Users(id="1", password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return "User created!"""

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

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
@login_required
def admin():
    print("Current user:", current_user)
    print("Is authenticated?", current_user.is_authenticated)
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
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/admin")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form['password']
        user = Users.query.filter_by(id = '1').first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect("/admin")
        else:
            flash("Wrong password. Try again.")
            return redirect('/login')
    return render_template('login.html')

@app.route("/crystals")
def item1():
    products = Product.query.filter_by(itemtype = "c").all()
    return render_template("item1.html", products = products)


@app.route("/unicorns")
def item2():
    products = Product.query.filter_by(itemtype = "u").all()
    return render_template("item2.html", products = products)


@app.route("/culturalhandicrafts")
def item3():
    products = Product.query.filter_by(itemtype = "p").all()
    return render_template("item3.html", products = products)


if __name__ == '__main__':
    app.run(debug = True)