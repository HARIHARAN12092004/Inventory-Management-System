# Inventory Management System

A Flask-based web application for managing inventory across multiple locations. This system allows you to track products, manage locations, record movements, and generate balance reports.

## Features

- **Product Management**: Add, edit, and delete products with unique IDs and descriptions
- **Location Management**: Manage multiple warehouses and storage locations
- **Movement Tracking**: Record incoming and outgoing product movements between locations
- **Balance Reports**: View current inventory balance for each product in each location
- **Modern UI**: Clean, responsive interface built with Bootstrap 5

## Database Schema

### Tables
- **Product** (product_id, name, description)
- **Location** (location_id, name, address)
- **ProductMovement** (movement_id, timestamp, from_location, to_location, product_id, qty)

### Key Features
- Primary keys are text/varchar for easy identification
- Movements can have either from_location or to_location (or both)
- Automatic timestamp tracking for all movements
- Balance calculation based on incoming vs outgoing quantities

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application** Open your web browser and navigate to http://127.0.0.1:5000

## Usage

### Dashboard
The dashboard provides an overview of your inventory system with:
- Count of products, locations, and movements
- Quick access buttons to add new items
- System information and help

### Managing Products
- Navigate to "Products" from the main menu
- Click "Add New Product" to create a new product
- Fill in the Product ID, Name, and Description
- Use Edit/Delete buttons to modify existing products

### Managing Locations
- Navigate to "Locations" from the main menu
- Click "Add New Location" to create a new location
- Fill in the Location ID, Name, and Address
- Use Edit/Delete buttons to modify existing locations

### Recording Movements
- Navigate to "Movements" from the main menu
- Click "Add New Movement" to record a movement
- Select the product and at least one location (from or to)
- Enter the quantity being moved
- Use Edit/Delete buttons to modify existing movements

### Viewing Balance Reports
- Navigate to "Balance Report" from the main menu
- View current inventory balance for all products in all locations
- Only locations with positive stock are displayed
- Use the Print button to generate a printable report

## Sample Data
The application comes with pre-loaded sample data including:
- 4 sample products (Laptop, Mouse, Keyboard, Monitor)
- 4 sample locations (Main Warehouse, Store Front, Storage Room A, Online Orders)
- 20 sample movements demonstrating various scenarios

## Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLite (included with Python)
- **Frontend**: HTML5, Bootstrap 5, Bootstrap Icons
- **ORM**: Flask-SQLAlchemy
- **Forms**: Flask-WTF with WTForms

### Key Features
- Responsive design that works on desktop and mobile
- Form validation with user-friendly error messages
- Flash messages for user feedback
- Print-friendly balance reports
- Clean, modern UI with Bootstrap components


Inventory Management System/
├── app.py                 # Main Flask application entry point
├── models.py              # Database models (Product, Location, ProductMovement)
├── routes.py              # Application routes and view functions
├── forms.py               # Form definitions using Flask-WTF
├── seed_data.py           # Script to populate sample data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables configuration
├── README.md              # Project documentation
├── instance/              # Instance-specific data
│   └── inventory.db       # SQLite database file
├── pycache /           # Python compiled bytecode
│   ├── app.cpython-313.pyc
│   ├── forms.cpython-313.pyc
│   ├── models.cpython-313.pyc
│   └── routes.cpython-313.pyc
└── templates/             # HTML templates
├── base.html          # Base template with common layout
├── index.html         # Dashboard/homepage template
├── errors/            # Error page templates
│   ├── 404.html       # Not found error page
│   └── 500.html       # Server error page
├── products/          # Product-related templates
│   ├── index.html     # Products listing page
│   └── form.html      # Product add/edit form
├── locations/         # Location-related templates
│   ├── index.html     # Locations listing page
│   └── form.html      # Location add/edit form
├── movements/         # Movement-related templates
│   ├── index.html     # Movements listing page
│   └── form.html      # Movement add/edit form
└── report.html        # Inventory report template

## API Endpoints

### Dashboard
- GET / - Main dashboard showing system overview
### Products
- GET /products - List all products
- GET /products/add - Display form to add a new product
- POST /products/add - Create a new product with submitted data
- GET /products/edit/<id> - Display form to edit an existing product
- POST /products/edit/<id> - Update an existing product with submitted data
- GET /products/delete/<id> - Delete a product by ID
### Locations
- GET /locations - List all locations
- GET /locations/add - Display form to add a new location
- POST /locations/add - Create a new location with submitted data
- GET /locations/edit/<id> - Display form to edit an existing location
- POST /locations/edit/<id> - Update an existing location with submitted data
- GET /locations/delete/<id> - Delete a location by ID
### Movements
- GET /movements - List all product movements
- GET /movements/add - Display form to add a new product movement
- POST /movements/add - Create a new product movement with submitted data
- GET /movements/edit/<id> - Display form to edit an existing movement
- POST /movements/edit/<id> - Update an existing movement with submitted data
- GET /movements/delete/<id> - Delete a movement by ID
### Reports
- GET /balance - Display inventory balance report showing product quantities by location

## Development

### Running in Development Mode
```bash
python app.py
```
The application will run in debug mode with auto-reload enabled.

### Database Reset
To reset the database with fresh sample data:
```bash
python scripts\reset_db.py
```
## Screenshots
<img width="1599" height="808" alt="Screenshot 2025-10-05 152822" src="https://github.com/user-attachments/assets/232fdcdf-233c-4677-aabd-8edc4caa2786" />
<img width="1594" height="804" alt="Screenshot 2025-10-05 152839" src="https://github.com/user-attachments/assets/d947430b-88a6-45dd-9166-42c3262badf4" />
<img width="1596" height="817" alt="Screenshot 2025-10-05 152854" src="https://github.com/user-attachments/assets/1d9f48ae-1e27-4171-9c0e-1f8df8188daa" />
<img width="1599" height="812" alt="Screenshot 2025-10-05 152909" src="https://github.com/user-attachments/assets/8b2bd8c7-7b22-44ba-9375-8fcfb3413c87" />
<img width="1599" height="808" alt="Screenshot 2025-10-05 152923" src="https://github.com/user-attachments/assets/68de69f8-c019-4ce9-91ce-e0b6cb49d53a" />




