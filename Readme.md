# Backend Development Notes: Git, PostgreSQL, OOP & Flask

A cleaned-up, organized version of your notes — grouped by topic, with code separated from explanations, and a few gaps filled in so each section stands on its own.

---

## 1. Git & GitHub

### 1.1 Key Definitions

| Term | Meaning |
|---|---|
| **Git** | A version control system that tracks changes to your project over time. |
| **GitHub** | A cloud hosting/storage platform that hosts Git repositories. |
| **Repository ("repo")** | A project folder tracked by Git and stored on GitHub. |

### 1.2 Why use GitHub?

1. Store your projects securely online
2. Back up your code
3. Collaborate with other developers
4. Share your work with employers/clients
5. Contribute to open-source projects

### 1.3 One-time setup

Tell Git who you are (only needs to be done once per machine):

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

### 1.4 Pushing a brand-new project to GitHub

```bash
# 1. Start tracking this folder with Git
git init

# 2. Connect your local folder to a GitHub repository
git remote add origin https://github.com/l-tting/flask-project.git

# 3. Stage all files (prepare them to be saved)
git add .

# 4. Commit — take a saved "snapshot" of the project
git commit -m "My first commit"

# 5. Push that snapshot up to GitHub
git push origin main
# (older repos may use "master" instead of "main")
```

**Branch:** a parallel version/timeline of your code. `main`/`master` is usually the default, primary branch.

### 1.5 Updating a project that's already on GitHub

Once a repo exists, you repeat a shorter cycle every time you make changes:

```bash
git add .
git commit -m "added a p-tag in index"
git push origin master
```

### 1.6 Git status letters

When you run `git status`, files are labelled:

| Letter | Meaning |
|---|---|
| **U** | Untracked — Git doesn't know about this file yet |
| **A** | Added — staged, ready to be committed |
| **M** | Modified — an already-tracked file has changed |

---

## 2. PostgreSQL & psycopg2

### 2.1 Setting up the project

```bash
pip install flask
pip install psycopg2-binary
```

### 2.2 Creating the database and tables

```sql
CREATE DATABASE flask_myduka;
\c flask_myduka

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    buying_price NUMERIC(20, 2) NOT NULL CHECK (buying_price >= 0),
    selling_price NUMERIC(20, 2) NOT NULL CHECK (selling_price >= 0)
);

CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    pid INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    pid INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Example row
INSERT INTO products (name, buying_price, selling_price)
VALUES ('eggs', 50, 60);
```

> **Note on `pid`:** in `stock` and `sales`, `pid` stands for "product id" — a **foreign key** pointing back to `products.id`. `ON DELETE CASCADE` means if a product is deleted, its related stock/sales rows are deleted automatically.

### 2.3 Introduction to psycopg2

**psycopg2** is a driver — a library that lets Python talk to a PostgreSQL database.

| Term | Meaning |
|---|---|
| `psycopg2.connect()` | Function used to establish a connection to the database |
| `conn` | Variable that represents your connection to Postgres |
| `cur` | The **cursor** — the object responsible for running database operations (SELECT, INSERT, UPDATE, DELETE) |
| `cur.execute()` | Runs a SQL query |
| `cur.fetchall()` | Pulls the query results from Postgres into Python |
| `conn.commit()` | Permanently saves your changes to the database |

Connection parameters you need to supply:

1. **host** — where Postgres is located (which server); `localhost` for your own machine
2. **port** — which "door" on that server Postgres is listening on (default `5432`)
3. **user** — the Postgres user to log in as
4. **password** — the password for that user
5. **dbname** — the name of the database you want to connect to

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="your_password",
    dbname="flask_myduka"
)
cur = conn.cursor()
```

### 2.4 IP addresses and domain names (why "localhost" works)

| Term | Meaning |
|---|---|
| **IP address** | A number that uniquely identifies a device on a network |
| **IPv4** | e.g. `192.181.102.255` |
| **IPv6** | A newer, longer format designed to support far more devices |
| **Domain name** | A human-friendly name that stands in for an IP address (e.g. `www.google.com` instead of a raw IP) |
| `127.0.0.1` | The default IP address that always points back to your own device ("loopback") |
| `localhost` | The domain name for `127.0.0.1` |

So: an app is built → deployed to a server (which has an IP address) → and a domain name is pointed at that IP so people can reach it with a friendly URL.

### 2.5 Fetching data with psycopg2

```python
def get_sales():
    cur.execute("SELECT * FROM sales")
    data = cur.fetchall()
    return data
```

**Data shape:** `cur.fetchall()` always returns a **list of tuples**.

- **list** → the entire result set (all rows)
- **tuple** → a single row/record

Example:

```python
[
    (1, 'eggs', Decimal('50.00'), Decimal('60.00')),
    (2, 'bread', Decimal('55.00'), Decimal('65.00')),
    (3, 'shoes', Decimal('2000.00'), Decimal('2500.00')),
]
```

### 2.6 Inserting data with psycopg2

```python
def insert_sale(pid, quantity):
    cur.execute(
        "INSERT INTO sales (pid, quantity) VALUES (%s, %s)",
        (pid, quantity)
    )
    conn.commit()   # don't forget this, or the insert won't persist!
```

> **Tip:** always pass values with `%s` placeholders and a tuple of parameters (as above), never by building the SQL string with f-strings/concatenation — that avoids SQL injection.

### 2.7 Functions, parameters & arguments (quick recap)

- **function** — a reusable block of code that performs a specific task
- **parameter** — the placeholder variable in a function's definition (makes it reusable)
- **argument** — the real value you pass in when you actually call the function

```python
def insert_sale(pid, quantity):   # pid, quantity = parameters
    ...

insert_sale(3, 5)   # 3, 5 = arguments
```

### 2.8 Joining tables — sales per product

Goal: combine `products` and `sales` to get, per product, the total revenue (`selling_price × quantity`).

```sql
SELECT
    products.name AS p_name,
    SUM(products.selling_price * sales.quantity) AS total_sales
FROM products
JOIN sales ON sales.pid = products.id
GROUP BY p_name;
```

**Multiline strings in Python:** wrap a string in triple quotes (`""" ... """`) to let it span several lines — handy for writing longer SQL queries readably inside Python:

```python
query = """
    SELECT products.name AS p_name,
           SUM(products.selling_price * sales.quantity) AS total_sales
    FROM products
    JOIN sales ON sales.pid = products.id
    GROUP BY p_name;
"""
```

### 2.9 Practice queries to write yourself

Using the same join pattern, try building queries (and matching Python functions) for:

1. **Sales per day**
   ```sql
   SELECT sales.created_at::date AS sale_date,
          SUM(products.selling_price * sales.quantity) AS total_sales
   FROM products
   JOIN sales ON sales.pid = products.id
   GROUP BY sale_date;
   ```
2. **Profit per product** (profit = (selling_price − buying_price) × quantity sold)
   ```sql
   SELECT products.name AS p_name,
          SUM((products.selling_price - products.buying_price) * sales.quantity) AS total_profit
   FROM products
   JOIN sales ON sales.pid = products.id
   GROUP BY p_name;
   ```
3. **Profit per day**
   ```sql
   SELECT sales.created_at::date AS sale_date,
          SUM((products.selling_price - products.buying_price) * sales.quantity) AS total_profit
   FROM products
   JOIN sales ON sales.pid = products.id
   GROUP BY sale_date;
   ```

### 2.10 Must-know checklist before moving on

- **SQL:** basic queries, primary keys & foreign keys, joins, aggregate functions (`SUM`, `COUNT`, `AVG`...), `WHERE`/filtering, `GROUP BY`
- **Python:** data types, data structures (lists & tuples especially), conditionals, loops, and — with extra emphasis — **functions**

---

## 3. Object-Oriented Programming (OOP)

**OOP** is a programming paradigm where code is organized around **classes** and **objects**, rather than just plain functions and variables.

Python has two broad categories of data types:

1. **Built-in types** — come with the language (int, str, list, dict...)
2. **User-defined / custom types** — built by you, using classes

| Term | Meaning |
|---|---|
| **Class** | A blueprint/template for creating objects |
| **Object** | A specific instance created from a class |

Analogy: a **class** is the architectural sketch of a building; an **object** is an actual building constructed from that sketch. You can build many different real buildings (objects) from the same sketch (class).

### 3.1 The three things every class has

1. **Identity** — the class's name
2. **State** — defined by its **attributes** (variables that live inside the class). Answers: *what does it have?*
3. **Behaviour** — defined by its **methods** (functions that live inside the class). Answers: *what can it do?*

**Example — `Car`:**
- Identity: `Car`
- State (attributes): `make`, `model`, `year_of_manufacture`, `is_imported`, `colour`, `no_of_doors`
- Behaviour (methods): `move()`, `stop()`, `carry_goods()`

**Practice — sketch out these classes yourself first:**

- `Student`
  - State: `name`, `age`, `course`
  - Behaviour: `study()`, `eat()`, `sleep()`, `walk()`
- `Phone` — think about state (brand, model, storage, battery_level...) and behaviour (call(), send_message(), charge()...)
- `Dog` — think about state (breed, name, age...) and behaviour (bark(), eat(), fetch()...)

### 3.2 The constructor and `self`

```python
class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

    def study(self):
        print(f"{self.name} is studying {self.course}")
```

| Term | Meaning |
|---|---|
| `__init__()` | The **constructor** — a special method automatically called when a new object is created; used to set the object's initial attribute values |
| `self` | Refers to the specific object itself, so each object keeps its own separate data |
| **dunder method** | Short for "**d**ouble **under**score" method, e.g. `__init__`, `__str__` — special methods Python recognizes and calls automatically in certain situations |

Creating and using objects:

```python
s1 = Student("Amina", 21, "Computer Science")
s2 = Student("Brian", 23, "Data Science")

s1.study()   # Amina is studying Computer Science
s2.study()   # Brian is studying Data Science
```

### 3.3 Practice task — `BankAccount`

Build a class with these attributes and methods, then create two objects from it.

```python
class BankAccount:
    def __init__(self, account_number, balance, owner_name, date_opened):
        self.account_number = account_number
        self.balance = balance
        self.owner_name = owner_name
        self.date_opened = date_opened

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")

    def display_info(self):
        print(f"Account #{self.account_number} | Owner: {self.owner_name} "
              f"| Opened: {self.date_opened} | Balance: {self.balance}")


account1 = BankAccount("001", 1000, "Amina", "2024-01-10")
account2 = BankAccount("002", 500, "Brian", "2024-03-22")

account1.deposit(200)
account1.withdraw(150)
account1.display_info()

account2.display_info()
```

### 3.4 The four core OOP concepts

- **Encapsulation** — bundling an object's data (attributes) and the methods that operate on it together inside one class, and controlling access to that data (e.g. hiding internal details from outside code).
- **Inheritance** — one class (the *child*) can reuse and extend the attributes/methods of another class (the *parent*), instead of rewriting them from scratch. **Method overriding** is when a child class redefines a method it inherited, giving it new behaviour.
- **Polymorphism** — the same method name can behave differently depending on the object calling it. **Method overloading** (defining a method to accept different combinations of arguments) is one form of this.
- **Abstraction** — hiding complex internal implementation details and only exposing the essential parts of an object that the outside world needs to interact with.

A quick inheritance example, to make it concrete:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):          # Dog inherits from Animal
    def make_sound(self):   # overriding the parent's method
        print(f"{self.name} barks")

d = Dog("Rex")
d.make_sound()   # Rex barks  -> polymorphism + method overriding in action
```

---

## 4. Flask

**Flask** is a Python framework used to build web applications.

### 4.1 Framework vs. Library

> **Analogy — building a house**
>
> **David** wants to build a house, so he hires professionals (architects, engineers, construction workers). The process is faster and easier because the experts bring domain knowledge, but David must follow their process exactly as instructed. → This is a **framework**: faster, but you follow strict rules/structure.
>
> **Jerry** also wants to build a house, but does it entirely himself with no outside help. It's much harder, but he has total flexibility to do things his own way at every step. → This is a **library**: harder, but flexible.

**Framework** — a prebuilt structure of code and tools that makes development faster by giving you scaffolding to build within, at the cost of having to follow its conventions.

Examples by language:

| Language | Frameworks |
|---|---|
| Python | Flask, Django, FastAPI |
| JavaScript | React, Angular, Vue, Svelte |
| Java | Spring |
| C# | .NET |
| PHP | Laravel |
| Go | Chi, Gin |
| Ruby | Ruby on Rails |

### 4.2 URLs and routing

**Routing** is the mechanism that connects a URL to a specific Python function.

**URL** (Uniform Resource Locator) — the full address used to reach an application, e.g. `https://meet.google.com/dsh-idtb-oqb`

**Parts of a URL:**

1. **Protocol** — tells the browser how to communicate
   - `http` — HyperText Transfer Protocol (sends data as plain text)
   - `https` — HTTP **Secure** (sends data encrypted). Getting from `http` to `https` requires an SSL/TLS certificate (free ones are available, e.g. via Let's Encrypt).
2. **Domain name** — the human-friendly name used instead of an IP address
3. **Path / route** — the specific resource being requested (e.g. `/products`)
4. **Port** (optional) — which "door" on the server to use

### 4.3 Defining routes

Routing is enabled in Flask through the `@app.route()` **decorator**.

**Decorator function** — a function that modifies or adds behaviour to another function, without changing its code directly. In Python, decorators are written with an `@` prefix, placed directly above the function they affect.

`@app.route()` takes arguments such as:

1. **rule/path** — e.g. `/`, `/login`, `/profile`
2. **methods** — which HTTP methods this route should accept (see below)

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")             # the "index" route — the default landing page
def index():
    return "Welcome!"

@app.route("/products")     # decorator
def products():              # view function
    return "This is products"

if __name__ == "__main__":
    app.run(debug=True)      # starts your server and runs the application
```

**View function** — the function attached to a route; it runs some logic and returns a response. View function names must all be **unique** — two routes can't share a view function name.

### 4.4 Returning HTML pages

Instead of returning small strings, we usually want to return full HTML pages that can hold as much content as we like. To do that, Flask expects a specific project structure:

```
project/
├── main.py
├── database.py
├── static/          # CSS, images, videos, icons, favicons
└── templates/        # HTML files ("templates")
```

Use `render_template()` (imported from Flask) to return an HTML file from a view function — think of "render" as "return, but as a rendered page":

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

### 4.5 Template inheritance & Jinja

**Template inheritance** lets you define one parent/base template holding everything common to every page (navbar, footer, overall layout), so every other page just inherits those shared parts instead of repeating them. This is powered by **Jinja**, Flask's built-in templating engine.

`templates/base.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <nav>My Navbar</nav>

    {% block content %}
    <!-- each page's unique content goes here -->
    {% endblock %}

    <footer>My Footer</footer>
</body>
</html>
```

`templates/products.html`:

```html
{% extends "base.html" %}

{% block title %}Products{% endblock %}

{% block content %}
    <h1>Our Products</h1>
{% endblock %}
```

- `block title` — a "slot" for each page's unique title
- `block content` — a "slot" for each page's unique content
- `{% extends "base.html" %}` — tells Jinja "this page inherits from base.html"

### 4.6 Jinja syntax

Jinja is the templating language used to render dynamic HTML. Its syntax depends on whether you're outputting a **variable** or using a **control structure**.

**Control structures** (the building blocks of any programming logic):

1. **Sequence** — code executes top to bottom, left to right
2. **Selection** — decision-making (`if` statements)
3. **Repetition** — looping (`for`, `while`)

**1. Variables** — use double curly braces:

```html
<p>{{ product_name }}</p>
```

**2. Control structures** — use curly-brace-percent tags, with a clear start and end:

```html
{% if x == 5 %}
    <p>x is five</p>
{% endif %}

{% for product in products %}
    <p>{{ product.name }}</p>
{% endfor %}
```

Every control structure needs:
- **Initialization** — where it starts (`{% if %}`, `{% for %}`)
- **Termination** — where it ends (`{% endif %}`, `{% endfor %}`)

### 4.7 Displaying database data in HTML

The full data flow looks like this:

```
Database (Postgres) → psycopg2 → Python → Jinja → HTML
```

Data arrives as a **list of tuples**, e.g.:

```python
[
    (1, 'eggs', Decimal('50.00'), Decimal('60.00')),
    (2, 'bread', Decimal('55.00'), Decimal('65.00')),
    (3, 'shoes', Decimal('2000.00'), Decimal('2500.00')),
    (4, 'samsung phone', Decimal('20000.00'), Decimal('25000.00')),
    (5, 'juice', Decimal('80.00'), Decimal('120.00')),
]
```

A typical view function passes that data into a template:

```python
@app.route("/products")
def products():
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    return render_template("products.html", products=data)
```

And the template loops over it into a table:

```html
{% extends "base.html" %}

{% block content %}
<table border="1">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Buying Price</th>
        <th>Selling Price</th>
    </tr>
    {% for product in products %}
    <tr>
        <td>{{ product[0] }}</td>
        <td>{{ product[1] }}</td>
        <td>{{ product[2] }}</td>
        <td>{{ product[3] }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```

**Practice task:** display your sales and stock data using a similar table.

### 4.8 Posting data (forms)

**Posting data workflow:**

1. User is shown a form to fill in
2. User fills it in and submits
3. The form is submitted to a Flask route for processing
4. Flask extracts the submitted data using the **`request`** object
   - Data arrives as key–value pairs
   - The **key** is the input's `name` attribute
   - `request.method` — tells you which HTTP method was used (`GET`, `POST`, etc.)
   - `request.form` — extracts form data using the key
5. Data is processed and stored (e.g. inserted into the database)
6. The user is notified and redirected

**Form checklist** (what an HTML form needs to successfully post data):

1. **`action`** — the route the form data should be submitted to
2. **`method`** — what the server should do with the data (usually `POST`)
3. **`name`** attribute on every input — this becomes the *key* used to read that field's value
4. **`input type`** — e.g. `text`, `number`, `email`, `password`
5. A **submit button** — `<button type="submit">` or `<input type="submit">`

Example form (`templates/add_product.html`):

```html
<form action="/add-product" method="POST">
    <input type="text" name="p_name" placeholder="Product name">
    <input type="number" name="b_price" placeholder="Buying price">
    <input type="number" name="s_price" placeholder="Selling price">
    <button type="submit">Add Product</button>
</form>
```

Matching Flask route:

```python
from flask import request, redirect, url_for

@app.route("/add-product", methods=["POST"])
def add_product():
    p_name = request.form["p_name"]
    b_price = request.form["b_price"]
    s_price = request.form["s_price"]

    cur.execute(
        "INSERT INTO products (name, buying_price, selling_price) VALUES (%s, %s, %s)",
        (p_name, b_price, s_price)
    )
    conn.commit()

    return redirect(url_for("products"))
```

### 4.9 The four HTTP methods, in plain terms

| Method | What it does | Example |
|---|---|---|
| **GET** | Moves data **from** the server **to** the client | Viewing a list of products |
| **POST** | Moves data **from** the client **to** the server (creates something new) | Posting a photo on Instagram, adding a new product |
| **PUT** | Updates an existing resource | Changing your username/password, editing a product's price |
| **DELETE** | Removes a resource | Deleting a product |

### 4.10 Redirecting

**Redirecting** means sending the user from one route/page to another — typically done right after successfully processing a form, so the same form can't be accidentally re-submitted by refreshing the page.

Flask gives you `redirect()` and `url_for()` for this, both imported from `flask`:

```python
from flask import redirect, url_for

return redirect(url_for("products"))   # pass the *name* of the view function, not the URL string
```

### 4.11 Practice task

Apply the exact same form → route → insert → redirect pattern you just learned for products to **sales** and **stock** data as well.

---

## Suggested order to revise this in

1. Git & GitHub (5–10 min refresher, it's mostly commands)
2. PostgreSQL basics + psycopg2 connection/fetch/insert
3. Joins + the practice queries (sales/profit per product/day)
4. OOP fundamentals → `BankAccount` task → the four core concepts
5. Flask routing → templates → Jinja → displaying data → posting data
