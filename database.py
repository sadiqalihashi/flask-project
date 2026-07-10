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


products=get_products()
print(products)

def insert_products():
 cur.execute("insert into products(name,buying_price,selling_price)values('shoes',2000,2500) ")
 conn.commit()

insert_products()
products=get_products()
print(products)


def get_sales():
 cur.execute('select*from sales')
 sales=cur.fetchall()
 return sales

sales=get_sales()
print(sales)

def insert_sales():
 cur.execute("insert into sales(pid,quantity)values(3,5)")
 conn.commit()

insert_sales()
sales=get_sales()
print(sales)