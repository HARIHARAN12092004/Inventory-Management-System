from app import app, db
from models import Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def seed_database():
    """Populate the database with sample data for testing"""
    with app.app_context():
        # Clear existing data
        db.session.query(ProductMovement).delete()
        db.session.query(Product).delete()
        db.session.query(Location).delete()
        db.session.commit()
        
        print("Creating sample products...")
        products = [
            Product(name="Laptop", description="High-performance laptop", price=999.99, sku="LAP-001"),
            Product(name="Smartphone", description="Latest smartphone model", price=699.99, sku="PHN-001"),
            Product(name="Tablet", description="10-inch tablet", price=499.99, sku="TAB-001"),
            Product(name="Monitor", description="27-inch 4K monitor", price=349.99, sku="MON-001")
        ]
        db.session.add_all(products)
        db.session.commit()
        
        print("Creating sample locations...")
        locations = [
            Location(name="Main Warehouse", address="123 Storage Ave, Warehouse District"),
            Location(name="Retail Store", address="456 Main St, Downtown"),
            Location(name="Distribution Center", address="789 Logistics Pkwy, Industrial Zone")
        ]
        db.session.add_all(locations)
        db.session.commit()
        
        print("Creating sample product movements...")
        # Initial stock arrival to Main Warehouse
        movements = []
        base_time = datetime.now() - timedelta(days=30)
        
        # Initial stock arrival to Main Warehouse
        for product in products:
            qty = random.randint(50, 100)
            movements.append(
                ProductMovement(
                    product_id=product.product_id,
                    to_location_id=locations[0].location_id,  # Main Warehouse
                    qty=qty,
                    timestamp=base_time
                )
            )
        
        # Move some stock to Distribution Center
        base_time += timedelta(days=5)
        for product in products:
            qty = random.randint(10, 30)
            movements.append(
                ProductMovement(
                    product_id=product.product_id,
                    from_location_id=locations[0].location_id,  # From Main Warehouse
                    to_location_id=locations[2].location_id,    # To Distribution Center
                    qty=qty,
                    timestamp=base_time + timedelta(minutes=product.product_id * 30)
                )
            )
        
        # Move some stock to Retail Store
        base_time += timedelta(days=5)
        for product in products:
            qty = random.randint(5, 15)
            movements.append(
                ProductMovement(
                    product_id=product.product_id,
                    from_location_id=locations[2].location_id,  # From Distribution Center
                    to_location_id=locations[1].location_id,    # To Retail Store
                    qty=qty,
                    timestamp=base_time + timedelta(minutes=product.product_id * 30)
                )
            )
        
        # Sales from Retail Store (outgoing)
        base_time += timedelta(days=7)
        for _ in range(5):  # 5 days of sales
            for product in products:
                if random.random() > 0.3:  # 70% chance of sale
                    qty = random.randint(1, 3)
                    movements.append(
                        ProductMovement(
                            product_id=product.product_id,
                            from_location_id=locations[1].location_id,  # From Retail Store
                            qty=qty,
                            timestamp=base_time + timedelta(days=random.randint(0, 4))
                        )
                    )
        
        # Restock Retail Store from Distribution Center
        base_time += timedelta(days=10)
        for product in products:
            qty = random.randint(5, 10)
            movements.append(
                ProductMovement(
                    product_id=product.product_id,
                    from_location_id=locations[2].location_id,  # From Distribution Center
                    to_location_id=locations[1].location_id,    # To Retail Store
                    qty=qty,
                    timestamp=base_time
                )
            )
        
        # New inventory arrival to Main Warehouse
        base_time += timedelta(days=3)
        for product in products:
            if random.random() > 0.5:  # 50% chance of restock
                qty = random.randint(20, 40)
                movements.append(
                    ProductMovement(
                        product_id=product.product_id,
                        to_location_id=locations[0].location_id,  # To Main Warehouse
                        qty=qty,
                        timestamp=base_time + timedelta(hours=random.randint(0, 24))
                    )
                )
        
        db.session.add_all(movements)
        db.session.commit()
        
        print(f"Database seeded with {len(products)} products, {len(locations)} locations, and {len(movements)} movements.")

if __name__ == "__main__":
    seed_database()