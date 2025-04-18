import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# MySQL connection details
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kishu31101999",
        database="expense_tracker"
    )

# Function to execute a query and fetch results
def execute_query(query):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert result to pandas DataFrame for easy display
        df = pd.DataFrame(result, columns=columns)
        
        # Set the index to start from 1
        df.index = df.index + 1  # Adjust index to start from 1
        # List of columns to round to 2 decimal places
        columns_to_round = ['Total_Amount', 'Total_Cashback', 'Total_Spending', 'Percentage_Contribution', 'Average_Spending']

        # Iterate through the columns and round them if they exist in the DataFrame
        for column in columns_to_round:
            if column in df.columns:
                df[column] = df[column].round(2)
   
        
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        # Clean up
        cursor.close()
        connection.close()

# Streamlit UI
st.title("Expense Tracker")

# Display a list of questions as buttons
questions = [
    "What is the total amount spent in each category?",
    "What is the total amount spent using each payment method?",
    "What is the total cashback received across all transactions?",
    "Which are the top 5 most expensive categories in terms of spending?",
    "How much was spent on transportation using different payment modes?",
    "Which transactions resulted in cashback?",
    "What is the total spending in each month of the year",
    'Which months have the highest spending in categories like "Travel," "Entertainment," or "Gifts"?',
    "Are there any recurring expenses that occur during specific months of the year?",
    "How much cashback or rewards were earned in each month?",
    "How has your overall spending changed over time?",
    "Are there any patterns in grocery spending?",
    "Define High and Low Priority Categories?",
    "Which category contributes the highest percentage of the total spending?",
    "Which is the most common payment method used?",
    "What is the total spending on subscriptions?",
    "Which category shows the most consistent spending over the months?",
    "Which day of the week has the highest spending?",
    "What is the average spending per transaction across each category?",
    "What is the total amount spent on each payment method in each category?"
]


# Button to show total amount spent in each category
if st.button(questions[0]):
    query = """
    SELECT Category, SUM(Amount) AS Total_Amount
    FROM expenses
    GROUP BY Category
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write("Total Amount Spent in Each Category:")
        st.dataframe(result_df)
        # Display bar chart
        st.bar_chart(result_df.set_index("Category")["Total_Amount"])

# Button to show total amount spent using each payment method
if st.button(questions[1]):
    query = """
    SELECT Payment_Mode, SUM(Amount) AS Total_Amount
    FROM expenses
    GROUP BY Payment_Mode
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write("Total Amount Spent Using Each Payment Method:")
        st.dataframe(result_df)
        # Display bar chart
        st.bar_chart(result_df.set_index("Payment_Mode")["Total_Amount"])

# Button to show total cashback received across all transactions
if st.button(questions[2]):
    query = """
    SELECT SUM(Cashback) AS Total_Cashback
    FROM expenses
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write("Total Cashback Received Across All Transactions:")
        st.dataframe(result_df)

# Button to show top 5 most expensive categories in terms of spending
if st.button(questions[3]):
    query = """
    SELECT Category, SUM(Amount) AS Total_Amount
    FROM expenses
    GROUP BY Category
    ORDER BY Total_Amount DESC
    LIMIT 5
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write(" Top 5 Most Expensive Categories In Terms of Spending:")
        st.dataframe(result_df)
        # Display bar chart
        st.bar_chart(result_df.set_index("Category")["Total_Amount"])

# Button to show how much was spent on transportation using different payment modes
if st.button(questions[4]):
    query = """
    SELECT Payment_Mode, SUM(Amount) AS Total_Amount
    FROM expenses
    Where Category = 'Transport'
    GROUP BY Payment_Mode
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write("How much was spent on transportation using different payment modes:")
        st.dataframe(result_df)
        # Display bar chart
        st.bar_chart(result_df.set_index("Payment_Mode")["Total_Amount"])

#Button to show which transactions resulted in cashback
if st.button(questions[5]):
    query = """
    SELECT *
    FROM expenses
    Where Cashback > 0
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write("Transactions resulted in cashback:")
        st.dataframe(result_df)

#Button to show what is the total spending in each month of the year
if st.button(questions[6]):
    query = """
    SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, SUM(Amount) AS Total_Spending
    FROM expenses
    GROUP BY YEAR(Date), MONTH(Date)
    ORDER BY Year, Month
    """
    result_df = execute_query(query)
    
    if result_df is not None:
        st.write("Total spending in each month of the year:")
        st.dataframe(result_df)

        # Combine Year and Month for better readability
        result_df["Month_Year"] = result_df["Year"].astype(str) + "-" + result_df["Month"].astype(str)

        # Create an interactive line chart
        fig = px.line(result_df, x="Month_Year", y="Total_Spending", markers=True, title="Monthly Spending Trend")
        fig.update_xaxes(title_text="Month-Year", tickangle=-45)
        fig.update_yaxes(title_text="Total Spending")
        st.plotly_chart(fig)

#Button to show  which months have the highest spending in categories like "Travel," "Entertainment," or "Gifts"?
if st.button(questions[7]):
    query = """
    SELECT YEAR(Date) AS Year, 
           MONTH(Date) AS Month, 
           Category, 
           SUM(Amount) AS Total_Spending
    FROM expenses
    WHERE Category IN ('Transport', 'Subscription', 'Gifts')  
    GROUP BY YEAR(Date), MONTH(Date), Category
    ORDER BY Year, Month, Category
    """
    result_df = execute_query(query)

    if result_df is not None:
        st.write('Months with the highest spending in categories like "Travel," "Entertainment," or "Gifts":')
        st.dataframe(result_df)

        # Convert Month number to a proper Month-Year format
        result_df["Month_Year"] = result_df["Year"].astype(str) + "-" + result_df["Month"].astype(str)

        # Create an Area Chart
        fig = px.area(result_df, x="Month_Year", y="Total_Spending", color="Category", 
                      title="Spending Trends in Travel, Entertainment, and Gifts", 
                      line_group="Category")

        fig.update_xaxes(title_text="Month-Year", tickangle=-45)
        fig.update_yaxes(title_text="Total Spending")

        # Show the chart
        st.plotly_chart(fig)

#Button to show are there any recurring expenses that occur during specific months of the year
if st.button(questions[8]):
    query = """
    SELECT 
        YEAR(Date) AS Year, 
        MONTH(Date) AS Month, 
        Description, 
        SUM(Amount) AS Total_Spending,
        COUNT(*) AS Frequency
    FROM expenses
    GROUP BY YEAR(Date), MONTH(Date), Description
    HAVING COUNT(*) > 1
    ORDER BY Frequency DESC;
    """
    result_df = execute_query(query)

    if result_df is not None:
        st.write('Recurring expenses that occur during specific months of the year:')
        st.dataframe(result_df)

         # Create a bar chart
        fig = px.bar(
            result_df,
            x="Description",
            y="Frequency",
            color="Month",
            barmode="group",
            title="Recurring Expenses by Description and Month",
            labels={"Frequency": "Occurrences", "Month": "Month"},
        )

        fig.update_layout(xaxis_tickangle=-45)  # Rotate labels for readability
        st.plotly_chart(fig)

#Button to show how much cashback or rewards were earned in each month

if st.button(questions[9]):
    query = """
    SELECT YEAR(Date) AS Year, 
           MONTH(Date) AS Month, 
           SUM(Cashback) AS Total_Cashback
    FROM expenses
    GROUP BY YEAR(Date), MONTH(Date)
    ORDER BY Year, Month;
    """
    result_df = execute_query(query)

    if result_df is not None:
        st.write('Cashback or Rewards earned in each month:')
        st.dataframe(result_df)

        # Convert Month number to name for better readability
        result_df["Month"] = result_df["Month"].apply(lambda x: pd.to_datetime(f'2024-{x}-01').strftime('%b'))

        # Create an area chart
        fig = px.area(result_df, x="Month", y="Total_Cashback", 
                      title="Monthly Cashback or Rewards Earned",
                      labels={"Total_Cashback": "Total Cashback", "Month": "Month"},
                      line_shape="spline", 
                      markers=True)

        fig.update_traces(fill='tozeroy', line=dict(color='green'))  # Green area fill

        # Show the chart
        st.plotly_chart(fig)

#Button to show how has your overall spending changed over time

if st.button(questions[10]):
    query = """
    SELECT YEAR(Date) AS Year, 
           MONTH(Date) AS Month, 
           SUM(Amount) AS Total_Spending
    FROM expenses
    GROUP BY YEAR(Date), MONTH(Date)
    ORDER BY Year, Month;
    """
    result_df = execute_query(query)

    if result_df is not None:
        st.write('How has your overall spending changed over time:')
        st.dataframe(result_df)

        # Convert Month number to name for better readability
        result_df["Month"] = result_df["Month"].apply(lambda x: pd.to_datetime(f'2024-{x}-01').strftime('%b'))

        # Create a combined Year-Month column for better visualization
        result_df["YearMonth"] = result_df["Year"].astype(str) + "-" + result_df["Month"]

        # Create a line chart
        fig = px.line(result_df, x="YearMonth", y="Total_Spending",
                      title="Overall Spending Trend Over Time",
                      labels={"Total_Spending": "Total Spending", "YearMonth": "Month-Year"},
                      markers=True, line_shape="spline")

        fig.update_traces(line=dict(color='blue', width=2))

        # Show the chart
        st.plotly_chart(fig)
        
#Button to show are there any patterns in grocery spending (e.g., higher spending on weekends)
if st.button(questions[11]):
    query = """
    SELECT YEAR(Date) AS Year,
           MONTH(Date) AS Month,
           DAYOFWEEK(Date) AS Day_Of_Week,
           SUM(Amount) AS Total_Spending
    FROM expenses
    WHERE Category = 'Groceries' AND (DAYOFWEEK(Date) = 1 OR DAYOFWEEK(Date) = 7)
    GROUP BY YEAR(Date), MONTH(Date), DAYOFWEEK(Date)
    ORDER BY Year DESC, Month DESC;
    """
    try:
        result_df = execute_query(query)
        if result_df is not None and not result_df.empty:
            st.write("📅 **Grocery Spending on Weekends (Saturday & Sunday)**")
            st.dataframe(result_df)

            # Convert Day_Of_Week to names
            day_map = {1: "Sunday", 7: "Saturday"}
            result_df["Day_Of_Week"] = result_df["Day_Of_Week"].map(day_map)

            # Line Chart for Weekend Spending Trend
            fig = px.line(result_df, x="Month", y="Total_Spending", color="Day_Of_Week",
                          title="Weekend Grocery Spending Pattern",
                          markers=True, line_shape="spline",
                          labels={"Month": "Month", "Total_Spending": "Total Spending ($)"})
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")


#Button to show high and low priority categories
if st.button(questions[12]):
    query = """
   SELECT 
    YEAR(Date) AS Year, 
    MONTH(Date) AS Month, 
    Category,
    CASE 
        WHEN Category IN ('Bills', 'EMI', 'Transport') THEN 'High Priority'
        WHEN Category IN ('Groceries', 'Subscription', 'Investment') THEN 'Low Priority'
        ELSE 'Unclassified'
    END AS Priority,
    SUM(Amount) AS Total_Spending
    FROM expenses
    WHERE Category IN ('Investment', 'Bills', 'Groceries', 'EMI', 'Subscription', 'Transport')
    GROUP BY YEAR(Date), MONTH(Date), Category, Priority
    ORDER BY Year DESC, Month DESC;
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('High and Low priority categories:')
        st.dataframe(result_df)

        # Convert Month numbers to Month names
        result_df["Month"] = pd.to_datetime(result_df["Month"], format="%m").dt.strftime("%b")

        # Stacked Area Chart for Spending Trends
        fig = px.area(result_df, 
                      x="Month", 
                      y="Total_Spending", 
                      color="Priority",
                      title="High vs. Low Priority Spending Trends",
                      labels={"Total_Spending": "Total Spending ($)", "Month": "Month"},
                      category_orders={"Priority": ["High Priority", "Low Priority"]})

        st.plotly_chart(fig)

#Button to show which category contributes the highest percentage of the total spending
if st.button(questions[13]):
    query = """
    SELECT 
        Category,
        SUM(Amount) AS Total_Spending,
        (SUM(Amount) / (SELECT SUM(Amount) FROM expenses)) * 100 AS Percentage_Contribution
        FROM expenses
        GROUP BY Category
        ORDER BY Percentage_Contribution DESC
        LIMIT 1;
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('Category contributes the highest percentage of the total spending:')
        st.dataframe(result_df)

#Button to show which is the most common payment method used
if st.button(questions[14]):
    query = """
    SELECT Payment_Mode, COUNT(*) AS Frequency
    FROM expenses
    GROUP BY Payment_Mode
    ORDER BY Frequency DESC
    LIMIT 1
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('The most common payment method used:')
        st.dataframe(result_df)

#Button to show what is the total spending on subscriptions
if st.button(questions[15]):
    query = """
    SELECT SUM(Amount) AS Total_Spending
    FROM expenses
    WHERE Category = 'Subscription'
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('The total spending on subscriptions:')
        st.dataframe(result_df)

#Button to show which category shows the most consistent spending over the months
if st.button(questions[16]):
    query = """
    SELECT Category, AVG(Amount) AS Average_Spending
    FROM expenses
    GROUP BY Category
    ORDER BY Average_Spending DESC
    LIMIT 1
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('Category shows the most consistent spending over the months:')
        st.dataframe(result_df)

#Button to show which day of the week has the highest spending
if st.button(questions[17]):
    query = """
    SELECT DAYNAME(Date) AS Day_Of_Week, SUM(Amount) AS Total_Spending
    FROM expenses
    GROUP BY Day_Of_Week
    ORDER BY Total_Spending DESC
    LIMIT 1;
    """
    result_df = execute_query(query)
    if result_df is not None:
        st.write('Which day of the week has the highest spending:')
        st.dataframe(result_df)

# Button to show average spending per transaction across each category
if st.button(questions[18]):
   query = """
    SELECT Category, AVG(Amount) AS Average_Spending
    FROM expenses
    GROUP BY Category
    ORDER BY Average_Spending DESC;
    """
   result_df = execute_query(query)
   if result_df is not None:
        st.write('Average spending per transaction across each category:')
        st.dataframe(result_df)

        # Bar Chart for Average Spending per Category
        fig = px.bar(result_df, 
                     x="Category", 
                     y="Average_Spending", 
                     title="Average Spending Per Transaction by Category",
                     labels={"Average_Spending": "Average Spending ($)"},
                     color="Average_Spending", 
                     color_continuous_scale="Blues")

        st.plotly_chart(fig)

# Button to show total spending by each payment method in each category
if st.button(questions[19]):
    query = """
    SELECT Category, Payment_Mode, SUM(Amount) AS Total_Spending
    FROM expenses
    GROUP BY Category, Payment_Mode
    ORDER BY Category, Total_Spending DESC;
    """
    result_df = execute_query(query)
    
    if result_df is not None:
        st.write('Total amount spent on each payment method in each category:')
        st.dataframe(result_df)

        # Stacked Bar Chart for Spending by Payment Mode in Each Category
        fig = px.bar(result_df, 
                     x="Category", 
                     y="Total_Spending", 
                     color="Payment_Mode",
                     title="Spending by Payment Mode Across Categories",
                     labels={"Total_Spending": "Total Spending ($)"},
                     barmode="stack")  # Stack bars to show contribution per payment mode

        st.plotly_chart(fig)