from flask import Flask, render_template,request,redirect,url_for
from database import get_products,get_sales,get_stock,insert_products,insert_sales,insert_stock

app=Flask(__name__)

@app.route('/')
def home():
    x= 5
    name='matt'
    numbers=[1,2,3,4,5]
    return render_template('index.html',value=x,y = name ,numbers = numbers)

@app.route('/products')
def products():
    product_data=get_products()
    return render_template('products.html',product_data=product_data)


@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method=='POST':
        product_name=request.form['p_name']
        buying_price=request.form['b_name']
        selling_price=request.form['s_name']

        new_product=(product_name,buying_price,selling_price)
        insert_products(new_product)
        print('product added successfully')
    return redirect(url_for('products'))
    

@app.route('/sales')
def sales():
    sales_data=get_sales()
    return render_template('sales.html',sales_data=sales_data)


app.route('/insert_sales',methods=['GET','POST'])
def insert_sales():
    if request.method=='POST':
        pid=request.form['pid']
        quantity=request.form['quantity']
        createdat=request.form['created at']

        new_sale=(pid,quantity,createdat)
        insert_sales(new_sale)
        print('sale added succefully')
    return redirect(url_for('sales'))    


@app.route('/stock')
def stocks():
    stock_data=get_stock
    return render_template('stock.html',stock_data=stock_data)

app.route('/insert_stock',methods=['GET','POST'])
def insert_stock():
    if request.method=='POST':
        pid=request.form['pid']
        stock_quantity=request.form['stock_quantity']
        created_at=request.form['created_at']

        new_stock=(pid,stock_quantity,created_at)
        insert_stock(new_stock)
        print('stock added succefully')
    return redirect(url_for('stock'))    

@app.route('/regester')
def regester():
    return render_template('regester.html') 

@app.route('/dashboard')
def dashboard():
    return render_template('dashbord.html')


@app.route('/login')
def login():
    return render_template('login.html')


app.run(debug=True)
