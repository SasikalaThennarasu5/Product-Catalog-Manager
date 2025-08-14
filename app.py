from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import ProductForm
from models import db, Product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# MySQL connection (adjust username, password, db name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/product_catalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.order_by(Product.name).all()
    in_stock_products = Product.query.filter_by(in_stock=True).all()
    return render_template('index.html', products=products, in_stock_products=in_stock_products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            in_stock=form.in_stock.data,
            description=form.description.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.in_stock = form.in_stock.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_product.html', form=form)

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
