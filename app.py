from flask import Flask, request, redirect, render_template
import pymongo

app = Flask(__name__, template_folder='C:/Users/Win10/Documents/flaskmongo/templates')

# Set up MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Ecommerce"]
collection = db["products"]

# Product model
class Product:
    def __init__(self, name, price, description,stock):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve form data from request
        name = request.form.get('name')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        stock = request.form.get('stock')
        
        # Create Product object and insert into MongoDB collection
        product = Product(name, price, description, stock)
        collection.insert_one(product.__dict__)
        
        # Redirect back to home page after form submission
        return redirect('/')
    else:
        # Retrieve products from MongoDB collection
        products = collection.find({})
        
        # Render the template with the products and the form to add new product
        return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)