import psycopg2

# connecting to a database
conn=psycopg2.connect(host='localhost',port=5432,user='postgres',password='194747',dbname='flask_myduka')

# creating a cursor object to perform db operations
cur=conn.cursor()

def get_products():
# function used to execute queries
 cur.execute('select * from products')
# function that fetches the query
 products=cur.fetchall()
 return products


# products=get_products()
# print(products)

def insert_products(product_values):
 cur.execute("insert into products(name,buying_price,selling_price)values(%s,%s,%s)", product_values)
 conn.commit()

# product1=('juice',200,400)
# product2=('charger',400,600)
# insert_products(product1)
# insert_products(product2)
# products=get_products()
# print(products)


def get_sales():
 cur.execute('select*from sales')
 sales=cur.fetchall()
 return sales

# sales=get_sales()
# print(sales)

def insert_sales(sales_values):
 cur.execute("insert into sales(pid,quantity)values(%s,%s)",sales_values)
 conn.commit()

# sales1=(2,50)
# sales2=(3,60)
# insert_sales(sales1)
# insert_sales(sales2)
# sales=get_sales()
# print(sales)



def get_stock():
 cur.execute('select*from stock')
 stock=cur.fetchall()
 return stock

# stock=get_stock()
# print(stock)

def insert_stock(stock_values):
 cur.execute("insert into stock(pid,stock_quantity)values(%s,%s)",stock_values)
 conn.commit()

# stock1=(3,40)
# stock2=(6,30)
# insert_stock(stock1)
# insert_stock(stock2)
# stock=get_stock()
# print(stock)


def sales_per_product():
    cur.execute("""
        select products.name as p_name , sum(products.selling_price * sales.quantity) as 
        total_sales from products join sales on sales.pid = products.id group by p_name;
    """)
    sales_product = cur.fetchall()
    return sales_product


sales_product = sales_per_product()
print(sales_product)

def profit_per_day():
  cur.execute(""" SELECT 
    DATE(s.created_at) AS day,  SUM(s.quantity * (p.selling_price - p.buying_price)) AS total_profit 
    FROM sales s JOIN products p ON s.pid = p.id GROUP BY DATE(s.created_at) ORDER BY day;
  """)
  
  sales_product=cur.fetchall()
  return sales_product


profit_day=profit_per_day()
print(profit_day)

def profit_per_product():
  cur.execute("""
    select p.name,SUM(s.quantity * (p.selling_price - p.buying_price)) AS total_profit
    FROM sales s JOIN products p on s.pid =p.id GROUP BY p.name ORDER BY total_profit
  """)
  sales_product=cur.fetchall()
  return sales_product

profit_product=profit_per_product()
print(profit_product)

def sales_per_day():
  cur.execute("""
    SELECT DATE(s.created_at) AS day, SUM(s.quantity * p.selling_price) AS total_sales
    FROM sales s JOIN products p on s.pid =p.id GROUP BY day ORDER BY total_sales

  """)

  sales_product=cur.fetchall()
  return sales_product
sales_day=sales_per_day()
print(sales_day)




