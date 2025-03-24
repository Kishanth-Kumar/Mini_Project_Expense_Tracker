from faker import Faker
import random
import pandas as pd

fake = Faker()

categories = ["Investment", "Bills", "Groceries", "EMI", "Subscription", "Transport"]
paymentMode = ["Cash", "UPI", "Credit Card"]
bills = ["Electricity Bill", "Mobile", "Gas", "Broadband"]
subscription = ["Prime", "JioHotstar", "Zee5"]
investment = ["Stocks", "Real Estate", "Bonds", "Mutual Funds"]
transport = ["Fuel", "Taxi", "Public Transport", "Car Rental"]

def generate_monthly_expense_data(no_of_records):
    data = []
    
    for month in range(1, 13):  # Generate data for each month (1-12)
        for _ in range(no_of_records):
            category = random.choice(categories)
            description = ""
            
            if category == "Investment":
                description = f"Investment in {random.choice(investment)}"
            elif category == "Bills":
                description = f"{random.choice(bills)} payment"
            elif category == "Groceries":
                description = f"Groceries shopping at {fake.company()}"
            elif category == "EMI":
                description = f"EMI for {fake.company()} product"
            elif category == "Subscription":
                description = f"Subscription for {random.choice(subscription)}"
            elif category == "Transport":
                description = f"Transport cost for {random.choice(transport)}"
            
            expense = {
                "Date" : fake.date_this_month().replace(year=2025, month=month).strftime('%Y-%m-%d'),  # Adjust to the respective month
                "Category" : category,
                "Payment Mode" : random.choice(paymentMode),
                "Description" : description,
                "Amount" : round(random.uniform(1000, 10000), 2),
                "Cashback": round(random.uniform(1, 10), 2)
            }
            data.append(expense)
    
    return pd.DataFrame(data)

# Generate data for all 12 months
exp_data = generate_monthly_expense_data(5)    

# Save the data to a CSV file or return for further use
exp_data.to_csv('expenses_data.csv', index=False)  # Saving as CSV to be used by another script
