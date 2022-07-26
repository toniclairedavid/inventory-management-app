import sqlite3 #, pandas, matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import datetime
from werkzeug.exceptions import abort
from email.mime.text import MIMEText
import smtplib as smtp

app = Flask(__name__)

def get_db_connection():
    db = sqlite3.connect('inventory.db')
    db.row_factory = sqlite3.Row
    return db

def email_confirm_notif(user_email): ## sending notification to user_emails
    connection = smtp.SMTP_SSL('smtp.gmail.com', 465) ##establishing connection
    connection.set_debuglevel(1)

    message = MIMEText("Hi! Your e-mail has been successfully added to the database") 
    
    email_addr = 'itmcapstonegr32022@gmail.com'
    email_passwd = 'hawzayvzljzwkdhs' 

    message["Subject"] = "E-mail Confirmation Message"
    message["From"] = email_addr
    message["To"] = user_email
    connection.login(email_addr, email_passwd) #logsin with application password
   
    connection.sendmail(email_addr, user_email, message.as_string()) ##sends email
    connection.close() ##close connection

#login
@app.route("/", methods=["POST", "GET"])
def logIn():
    conn = get_db_connection()
    cursor = conn.cursor()

    if (request.method == "POST"):
        user_name    = request.form['user_name']
        user_email = request.form['user_email']

        users = cursor.execute("SELECT * FROM user").fetchall()
        for row in users:
            email = row[1]
            if email==user_email:
                return redirect("/instructions/")

        try:
            cursor.execute('INSERT INTO user (name, email) VALUES (?, ?)', 
            (user_name, user_email))
            email_confirm_notif(user_email)
            conn.commit()
            conn.close()
            return redirect("/instructions/")

        except:
            return "There was an issue while logging in."

    else:
        return render_template("login.html")

#index (dashboard)
@app.route('/index/', methods=["POST", "GET"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST") and ('product_name' in request.form):
        product_name        = request.form["product_name"]
        product_summary     = request.form["product_summary"]
        product_quantity    = request.form["product_quantity"]
        try:
            cursor.execute('INSERT INTO product (name, summary, quantity, createdAt) VALUES (?, ?, ?, ?)',
            (product_name, product_summary, product_quantity, datetime.now()))
            conn.commit()
            conn.close()
            return redirect("/index/")
        except:
            return "There Was an issue while add a new Product"
    
    if (request.method == "POST") and ('customer_name' in request.form):
        customer_name       = request.form["customer_name"]
        customer_mobile     = request.form["customer_mobile"]
        customer_email      = request.form["customer_email"]
        customer_address    = request.form["customer_address"]
        try:
            cursor.execute('INSERT INTO customer (name, mobile, email, address, createdAt) VALUES (?, ?, ?, ?, ?)',
            (customer_name, customer_mobile, customer_email, customer_address, datetime.now()))
            conn.commit()
            conn.close()
            return redirect("/index/")
        except:
            return "There Was an issue while add a new Customer"
    else:
        products    = cursor.execute('SELECT * FROM product').fetchall()
        customers   = cursor.execute('SELECT * FROM customer').fetchall()
        return render_template("index.html", products = products, customers = customers)

@app.route('/product/', methods=["POST", "GET"])
def viewProduct():
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST"):
        product_name        = request.form["product_name"]
        product_summary     = request.form["product_summary"]
        product_quantity    = request.form["product_quantity"]
        
        try:
            cursor.execute('INSERT INTO product (name, summary, quantity, createdAt) VALUES (?, ?, ?, ?)',
            (product_name, product_summary, product_quantity, datetime.now()))
            conn.commit()
            conn.close()
            return redirect("/product/")

        except:
            products = cursor.execute('SELECT * FROM product').fetchall()
            return "There was an issue while add a new Product"
    else:
        products = cursor.execute('SELECT * FROM product').fetchall()
        return render_template("product.html", products=products)

@app.route('/customer/', methods=["POST", "GET"])
def viewCustomer():
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST"):
        customer_name    = request.form['customer_name']
        customer_mobile = request.form['customer_mobile']
        customer_email = request.form['customer_email']
        customer_address = request.form['customer_address']

        try:
            cursor.execute('INSERT INTO customer (name, mobile, email, address, createdAt) VALUES (?, ?, ?, ?, ?)', 
            (customer_name, customer_mobile, customer_email, customer_address, datetime.now()))
            conn.commit()
            conn.close()
            return redirect("/customer/")

        except:
            customers = cursor.execute('SELECT * FROM customer').fetchall()
            return "There was an issue while add a new Customer"
    else:
        customers  = cursor.execute('SELECT * FROM customer').fetchall()
        return render_template("customer.html", customers=customers)

@app.route("/update-product/<name>", methods=["POST", "GET"])
def updateProduct(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST"):
        product_name    = request.form['product_name']
        product_summary = request.form['product_summary']
        product_quantity = request.form['product_quantity']

        try:
            cursor.execute('UPDATE product SET name = ?, summary = ?, quantity = ?, updatedAt = ? WHERE name = ?', 
            (product_name, product_summary, product_quantity, datetime.now(), name))
            conn.commit()
            conn.close()
            return redirect("/product/")

        except:
            products = cursor.execute('SELECT * FROM product').fetchall()
            return "There was an issue while add a new Product"
    else:
        products  = cursor.execute('SELECT * FROM product').fetchall()
        return render_template("update-product.html", products=products)

@app.route("/add-quantity/<name>", methods=["POST", "GET"])
def addQuantity(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST"):
        product_quantity = request.form['product_quantity']

        try:
            product_row = cursor.execute('SELECT * FROM product').fetchall()
            for row in product_row:
                prod_row = str(row[1])
                prod_input = str(name)
                if prod_row == prod_input:                
                    new_quantity = int(row[3]) + int(product_quantity)

            cursor.execute('UPDATE product set quantity = ?, updatedAt = ? WHERE name = ?', 
            (new_quantity, datetime.now(), name))

            conn.commit()
            conn.close()
            return redirect("/product/")

        except:
            products = cursor.execute('SELECT * FROM product').fetchall()
            return "There was an issue while adding to the Stock"
    else:
        products  = cursor.execute('SELECT * FROM product').fetchall()
        return render_template("add-quantity.html", products=products)

@app.route("/update-customer/<name>", methods=["POST", "GET"])
def updateCustomer(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    if (request.method == "POST"):
        customer_name    = request.form['customer_name']
        customer_mobile = request.form['customer_mobile']
        customer_email = request.form['customer_email']
        customer_address = request.form['customer_address']

        try:
            cursor.execute('UPDATE customer SET name = ?, mobile = ?, email = ?, address = ?, updatedAt = ? WHERE name = ?', 
            (customer_name, customer_mobile, customer_email, customer_address, datetime.now(), name))
            conn.commit()
            conn.close()
            return redirect("/customer/")

        except:
            customers = cursor.execute('SELECT * FROM customer').fetchall()
            return "There was an issue while add a new Customer"
    else:
        customers  = cursor.execute('SELECT * FROM customer').fetchall()
        return render_template("update-customer.html", customers=customers)

@app.route("/order/", methods=["POST", "GET"])
def viewOrder():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST" :
        product_name    = request.form.get('productName')
        quantity        = request.form["quantity"]
        customer_name     = request.form.get('customerName')
        content         = request.form["content"]

        try:
            cursor.execute('INSERT INTO order_item (productName, quantity, customerName, content, orderedOn) VALUES (?, ?, ?, ?, ?)',
            (product_name, quantity, customer_name, content, datetime.now()))

            product_row = cursor.execute('SELECT * FROM product').fetchall()
            for row in product_row:
                prod_row = str(row[1])
                prod_input = str(product_name)
                if prod_row == prod_input:                
                    new_quantity = int(row[3]) - int(quantity)

            cursor.execute('UPDATE product set quantity = ?, updatedAt = ? WHERE name = ?', 
            (new_quantity, datetime.now(), product_name))

            conn.commit()
            conn.close()
            return redirect("/order/")

        except:
            orders = cursor.execute('SELECT * FROM order_item').fetchall()
            return "There was an issue while adding a new order"
    
    else:
        products  = cursor.execute('SELECT * FROM product').fetchall()
        customers  = cursor.execute('SELECT * FROM customer').fetchall()
        orders  = cursor.execute('SELECT * FROM order_item').fetchall()
        return render_template("order.html", products=products, customers=customers, orders=orders)

@app.route("/order-received/<id>", methods=["POST", "GET"])
def receiveOrder(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE order_item SET receivedOn = ? WHERE id = ?', (datetime.now(), id))
    conn.commit()
    cursor.close()
    return redirect("/order/")

@app.route('/delete-product/<id>')
def deleteProduct(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    return redirect("/product/")

@app.route('/delete-customer/<id>')
def deleteCustomer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    return redirect("/customer/")

@app.route('/delete-order/<id>')
def deleteOrder(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM order_item WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    return redirect("/order/")

@app.route("/product-analysis/")
def productAnalysis():
    conn = get_db_connection()
    cursor = conn.cursor()
    overall_sql = 'SELECT productName, SUM(quantity) sum_quantity FROM order_item GROUP BY productName'
    overall = cursor.execute(overall_sql).fetchall()
    # overall_data = pandas.read_sql(overall_sql, conn)
    # plt.bar(overall_data.productName, overall_data.sum_quantity)
    # plt.title("Overall Sale per Product")
    # plt.savefig('overall_plot.png')

    monthly = cursor.execute('SELECT productName, strftime("%Y-%m", orderedOn) AS year_month, SUM(quantity) FROM order_item GROUP BY productName, year_month').fetchall() 

    conn.commit()
    return render_template("product-analysis.html", overall=overall, monthly=monthly)

@app.route("/instructions/")
def instructions():
    return render_template("instructions.html")