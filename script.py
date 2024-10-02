import sqlite3

# Step 1: Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('car_buyers.db')  # This will create the 'car_buyers.db' file
cursor = conn.cursor()

# Step 2: Create the 'potential_buyers' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS potential_buyers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT NOT NULL,
        type TEXT NOT NULL,                -- e.g., Dealership, Fleet Owner
        contact_person_name TEXT,
        job_title TEXT,                    -- e.g., Fleet Manager, Purchasing Manager
        phone_number TEXT,
        email_address TEXT,
        postal_address TEXT,
        website_url TEXT,
        notes TEXT
    )
''')

# Step 3: Insert sample data into the table
sample_data = [
    ('Big Auto Dealership Inc.', 'Dealership', 'John Doe', 'Purchasing Manager', '555-1234', 'john.doe@bigauto.com', '123 Main St, Springfield, IL', 'https://bigautodealership.com', 'Interested in large quantity orders'),
    ('Fleet Management Corp.', 'Fleet Owner', 'Jane Smith', 'Fleet Manager', '555-5678', 'jane.smith@fleetcorp.com', '456 Fleet Ave, Madison, WI', 'https://fleetmanagementcorp.com', 'Has a requirement for delivery vans'),
    ('Rental Cars Unlimited', 'Rental Company', 'Mike Johnson', 'Procurement Officer', '555-9012', 'mike.johnson@rentalcars.com', '789 Rental Way, Chicago, IL', 'https://rentalcarsunlimited.com', 'Prefers low-mileage vehicles')
]

# Step 4: Insert sample data into the table
cursor.executemany('''
    INSERT INTO potential_buyers (business_name, type, contact_person_name, job_title, phone_number, email_address, postal_address, website_url, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

# Step 5: Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully.")
