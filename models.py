from app import db
from datetime import datetime

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    sku = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.name}>'

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))
    
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref=db.backref('outgoing_movements', lazy=True))
    
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref=db.backref('incoming_movements', lazy=True))
    
    qty = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'