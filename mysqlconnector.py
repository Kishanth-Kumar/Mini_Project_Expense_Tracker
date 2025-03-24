import mysql.connector
import pandas as pd

# MySQL connection details
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kishu31101999",
    database="expense_tracker"  # Make sure to use the correct database name
)

cursor = connection.cursor()

# Ensure the connection is successful
if connection.is_connected():
    print("Connected to MySQL")

# Function to insert data into the MySQL database
def insert_expenses(dataframe):
    for _, row in dataframe.iterrows():
        sql = """
            INSERT INTO expenses (Date, Category, Payment_Mode, Description, Amount, Cashback)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            row['Date'],  # Extract the 'Date' value
            row['Category'],  # Extract the 'Category' value
            row['Payment Mode'],  # Extract the 'Payment Mode' value
            row['Description'],  # Extract the 'Description' value
            row['Amount'],  # Extract the 'Amount' value
            row['Cashback']  # Extract the 'Cashback' value
        )
        cursor.execute(sql, values)
    
    # Commit the transaction to save all the changes to the database
    connection.commit()

# Read the generated CSV file from File 1
exp_data = pd.read_csv('expenses_data.csv')

# Insert the data into the MySQL database
insert_expenses(exp_data)

# Close the cursor and connection
cursor.close()
connection.close()