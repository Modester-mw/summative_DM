import mysql.connector

# create a connection to the database
cnx = mysql.connector.connect(user='root', password='Foundation30',
                              host='localhost',
                              database='enrollment')

# create a cursor object to execute SQL queries
cursor = cnx.cursor()

# execute a query to fetch all the records from the courses table
query = "SELECT * FROM courses"
cursor.execute(query)

# iterate over the result set and print each row
for row in cursor.fetchall():
    print(row)

# close the cursor and connection objects
cursor.close()
cnx.close()
