import sqlite3

connection = sqlite3.connect('inventory.db')

with open('inv.sql') as f:
    connection.executescript(f.read())

try:
    # Connect to DB and create a cursor
    cursor = connection.cursor()
    print("initialized")
  
    # Write a query and execute it with cursor
    query = 'SELECT * FROM product;'
    cursor.execute(query)
  
    # Fetch and output result
    result = cursor.fetchall()
    print(result)
  
    # Close the cursor
    cursor.close()
  
# Handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)
  
# Close DB Connection irrespective of success
# or failure
finally:
    if connection:
        connection.close()
        print('SQLite Connection closed')