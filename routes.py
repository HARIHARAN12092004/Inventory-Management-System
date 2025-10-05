from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Product, Location, ProductMovement
from forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Add a context processor to make 'now' available to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}  # Using utcnow() for consistency

# Home route
@app.route('/')
def index():
    # Get counts for dashboard stats
    products_count = Product.query.count()
    locations_count = Location.query.count()
    movements_count = ProductMovement.query.count()
    
    return render_template('index.html', 
                          products_count=products_count,
                          locations_count=locations_count,
                          movements_count=movements_count)

# Product routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products/index.html', products=products)

@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                sku=form.sku.data
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: SKU already exists!', 'danger')
    
    return render_template('products/form.html', form=form, title='Add New Product', now=datetime.now())

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.sku = form.sku.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('products/form.html', form=form, title="Edit Product", now=datetime.now())

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Location routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations/index.html', locations=locations, now=datetime.now())

@app.route('/locations/new', methods=['GET', 'POST'])
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(
            name=form.name.data,
            address=form.address.data
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    return render_template('locations/form.html', form=form, title="Add Location", now=datetime.now())

@app.route('/locations/<int:location_id>/edit', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.name = form.name.data
        location.address = form.address.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    return render_template('locations/form.html', form=form, title="Edit Location", now=datetime.now())

@app.route('/locations/<int:location_id>/delete', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))

# Product Movement routes
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements/index.html', movements=movements, now=datetime.now())

@app.route('/movements/new', methods=['GET', 'POST'])
def new_movement():
    form = ProductMovementForm()
    # Populate select fields
    form.product_id.choices = [(p.product_id, p.name) for p in Product.query.all()]
    form.from_location_id.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    form.to_location_id.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    
    if form.validate_on_submit():
        movement = ProductMovement(
            product_id=form.product_id.data,
            qty=form.qty.data
        )
        
        if form.from_location_id.data != 0:
            movement.from_location_id = form.from_location_id.data
        
        if form.to_location_id.data != 0:
            movement.to_location_id = form.to_location_id.data
            
        db.session.add(movement)
        db.session.commit()
        flash('Product movement recorded successfully!', 'success')
        return redirect(url_for('movements'))
        
    return render_template('movements/form.html', form=form, title="Record Movement", now=datetime.now())

@app.route('/movements/<int:movement_id>/edit', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = ProductMovementForm(obj=movement)
    
    # Populate select fields
    form.product_id.choices = [(p.product_id, p.name) for p in Product.query.all()]
    form.from_location_id.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    form.to_location_id.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    
    # Set default values
    if movement.from_location_id is None:
        form.from_location_id.data = 0
    if movement.to_location_id is None:
        form.to_location_id.data = 0
    
    if form.validate_on_submit():
        movement.product_id = form.product_id.data
        movement.qty = form.qty.data
        
        movement.from_location_id = form.from_location_id.data if form.from_location_id.data != 0 else None
        movement.to_location_id = form.to_location_id.data if form.to_location_id.data != 0 else None
            
        db.session.commit()
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('movements'))
        
    return render_template('movements/form.html', form=form, title="Edit Movement", now=datetime.now())

@app.route('/movements/<int:movement_id>/delete', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

# Report route
@app.route('/report')
def report():
    # This query calculates the current quantity of each product in each location
    # by summing the incoming and outgoing movements
    
    # Get all products and locations for the report
    products = Product.query.all()
    locations = Location.query.all()
    
    # Create a dictionary to store the quantities
    inventory = {}
    
    for product in products:
        inventory[product.product_id] = {'name': product.name, 'locations': {}}
        for location in locations:
            # Calculate incoming quantity (to_location = this location)
            incoming = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location_id == location.location_id
            ).scalar() or 0
            
            # Calculate outgoing quantity (from_location = this location)
            outgoing = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location_id == location.location_id
            ).scalar() or 0
            
            # Calculate balance
            balance = incoming - outgoing
            
            # Store in inventory dictionary
            inventory[product.product_id]['locations'][location.location_id] = {
                'name': location.name,
                'qty': balance
            }
    
    return render_template('report.html', inventory=inventory, products=products, locations=locations, now=datetime.now())

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Roll back the session in case of database errors
    return render_template('errors/500.html'), 500