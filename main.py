import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import webserver
import callAPI
import params

#Start up
# webserver.app

import csv as csv

# Import Data to dataframe
sales = pd.read_csv("Walmart.csv")
sales.dtypes

print(sales.dtypes)
pd.set_option('display.float_format', lambda x: '%.9f' % x)


#Turn stores and holiday flag into a category
sales.Store = pd.Categorical(sales.Store)
sales.Holiday_Flag = pd.Categorical(sales.Holiday_Flag)

sales.dtypes

sales.head()

# Dummy data
dummy = pd.get_dummies(sales, columns=['Store', 'Holiday_Flag'])

x = dummy.drop(["Date", "Weekly_Sales"], axis=1)
y = dummy.Weekly_Sales

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

# build model
model = LinearRegression()
model.fit(x_train, y_train)

# evaluate the variance score
print("Linear Regression Variance score: " + str(model.score(x_test, y_test)))

prediction = model.predict(x_test)


user_input = [[82, 3.49, 250.109, 1.6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
user_predictions = model.predict(user_input)
print("Sales Predictions by Week")
print(user_predictions)

#TODO - seperate these. when submitting for a sales forecast, we POST and flask returns the value
# break up the prediction portion
"""
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


# plt.show()
# get data ready
"""

# webserver.app