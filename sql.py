import sqlite3

# connecting to sqllite
connection=sqlite3.connect(r'F:\netsol_project\text_2_sql_llm\schema\apartment_rentals.sqlite') 

# creating cursor object to insert record, create tables, and retrieve
cursor=connection.cursor()

# Displaying all the records
print('The inserted records are as give:')
data = cursor.execute('SELECT * FROM Apartment_Bookings')

for row in data:
    print(row)

# close the connection
connection.commit()
connection.close()
