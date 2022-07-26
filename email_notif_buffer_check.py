
from app import *
import smtplib as smtp
import schedule
import numpy as np
import time
import functools

from email.mime.text import MIMEText


def get_email(): ## gets email addresses of users
    conn = get_db_connection()
    cursor = conn.cursor() 
    
    email = list()
    users = cursor.execute('SELECT * FROM user').fetchall()
    for row in users:
        email.append(str(row[1]))

    return email
  

def check_stock(): ## checking if stock is above buffer level
    conn = get_db_connection()
    cursor = conn.cursor()        

    sales_avg = np.array([])
    products = np.array([])
    product_qty = np.array([])
    lead_time = np.array([])

    sales_avg_result = cursor.execute('SELECT productName, AVG(quantity) FROM order_item GROUP BY productName').fetchall() 

    for row in sales_avg_result: #loops each product and extracts the avg(quantity) and puts it in a numpy array
        prod_sales_avg = int(row[1]) 
        sales_avg = np.append(sales_avg, prod_sales_avg) 
    #https://stackoverflow.com/questions/7332841/add-single-element-to-array-in-numpy

    product_qty_result = cursor.execute('SELECT productName, SUM(quantity) FROM order_item GROUP BY productName').fetchall() 

    for row in product_qty_result: #loops each product and extracts the sum(quantity) and puts it in a numpy array
        print("h4")
        prod_name = str(row[0])
        total_prod_qty = int(row[1]) 
        products = np.append(products, prod_name) 
        product_qty = np.append(product_qty, total_prod_qty)

    lead_time_result = cursor.execute('SELECT productName, JULIANDAY(receivedOn) - JULIANDAY(orderedOn) + 1 AS date_difference FROM order_item GROUP BY productName').fetchall() ## gets the lead time (time between ordering and receiving an item)

    for row in lead_time_result: #loops each product and extracts the sum(quantity) and puts it in a numpy array
        print("h6", row[1])
        prod_lead_time = int(row[1]) 
        lead_time = np.append(lead_time, prod_lead_time)


    buffer_stock = sales_avg * lead_time
    indices = np.where(product_qty < buffer_stock)
    low_stock_products = np.take(products, indices)
    
    return low_stock_products

def do(self, job_func, *args, **kwargs): ##https://stackoverflow.com/questions/26583557/typeerror-the-first-argument-must-be-callable
  
    self.job_func = functools.partial(job_func, *args, **kwargs)
    functools.update_wrapper(self.job_func, job_func)
    self._schedule_next_run()
    return self


def notification(): ## sending notification to user_emails
    connection = smtp.SMTP_SSL('smtp.gmail.com', 465) ##establishing connection
    connection.set_debuglevel(1)

    email_content = check_stock().tolist()
    low_stock_content = ", ".join(email_content[0]) ##converting low_stock_product list to string

    if check_stock().size == 0: ##no items are low stock
        message_template = "All items are of sufficient quantity. Thank you!"
    
    else: 
        message_template = "Good day! Please restock the following items: "  + low_stock_content + "."   


    message = MIMEText(message_template) 
    
    email_addr = 'itmcapstonegr32022@gmail.com'
    email_passwd = 'hawzayvzljzwkdhs' 

    recipients = get_email() 
    message["Subject"] = "Restock Notification Alert"
    message["From"] = email_addr
    message["To"] = ", ".join(recipients)
    connection.login(email_addr, email_passwd) #logsin with application password

    print(message)
    print(recipients)

    connection.sendmail(email_addr, recipients, message.as_string()) ##sends email
    print("Successfully sent!")
    connection.close() ##close connection


schedule.every().day.at("17:00").do(notification) ##schedules email everyday at 5 PM

while True:
    schedule.run_pending()
    time.sleep(1)