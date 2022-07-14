import pandas as pd
import matplotlib.pyplot as plt
import csv as csv

# Import Data to dataframe
sales = pd.read_csv("Walmart.csv")
print(sales.head(50))
print(sales.describe())

pd.set_option('display.float_format', lambda x: '%.9f' % x)


#Turn stores and holiday flag into a category
sales.Store = pd.Categorical(sales.Store)
sales.Holiday_Flag = pd.Categorical(sales.Holiday_Flag)

#Convert Dates to date objects
sales.Date = pd.to_datetime(sales.Date, errors='ignore', dayfirst=True)
print(sales.dtypes)

#calculate sum of sales per store and top and lowest performers
sales_groups = sales.groupby('Store')['Weekly_Sales'].sum()
top_ten = sales.groupby('Store')['Weekly_Sales'].sum().nlargest(10)
bottom_ten = sales.groupby('Store')['Weekly_Sales'].sum().nsmallest(10)
#create bar plot by group
f1 = plt.figure(1)
sales_groups.plot(kind='bar', title='All Sales by Store', figsize=(7, 4))


f2 = plt.figure(2)
top_ten.plot(kind='bar', title='Highest Performing stores', figsize=(7, 4))


f3 = plt.figure(3)
bottom_ten.plot(kind='bar', title='Lowest Performing Stores', figsize=(7, 4))


plt.show()