from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import os, json, uuid

app = Flask(__name__)
app.config['UPLOADS'] = "static/uploads"
PRODUCTS_FILE = 'products.json'
app.secret_key = "test"

if os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, 'r') as file:
        products = json.load(file)
    
else:
    products = []

@app.route("/")
def index():
    return render_template("index.html", products = products)

@app.route("/product/<product_id>")
def product_page(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
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

        image_urls = []
        for image in images:
            filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            path = os.path.join(app.config["UPLOADS"], filename)
            image.save(path)
            image_urls.append(f'/static/uploads/{filename}')
        
        product = {
            'id': uuid.uuid4().hex,
            'name': name,
            'price': price,
            'description': description,
            'images': image_urls
        }

        products.append(product)
        with open(PRODUCTS_FILE, 'w') as file:
            json.dump(products, file)

        return redirect("/admin")
    
    return render_template('admin.html', products = products)

@app.route("/delete/<product_id>", methods = ["POST"])
def delete_product(product_id):
    global products
    products = [product for product in products if product['id'] != product_id]
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file)
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

if __name__ == '__main__':
    os.makedirs(app.config['UPLOADS'], exist_ok = True)
    app.run(debug = True)