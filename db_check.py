import sqlite3

# Step 6: Connect again to verify data
conn = sqlite3.connect('car_buyers.db')
cursor = conn.cursor()

# Fetch and print all rows in the table
cursor.execute('SELECT * FROM potential_buyers')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connection
conn.close()
