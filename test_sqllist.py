import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('foodtrucktest.db')
cursor = connection.cursor()

# Execute a SELECT query to retrieve data from the Data table
cursor.execute('SELECT * FROM Data')

# Fetch all rows and print them
rows = cursor.fetchall()
print(rows)

# Close the connection
connection.close()
