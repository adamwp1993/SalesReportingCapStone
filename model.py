import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class Model:

    def __init__(self):
        # Initialize the Linear regression model
        sales = pd.read_csv("Walmart.csv")
        sales.dtypes

        print(sales.dtypes)
        pd.set_option('display.float_format', lambda x: '%.9f' % x)

        # Turn stores and holiday flag into a category
        sales.Store = pd.Categorical(sales.Store)
        sales.Holiday_Flag = pd.Categorical(sales.Holiday_Flag)

        # Dummy data
        dummy = pd.get_dummies(sales, columns=['Store', 'Holiday_Flag'])

        x = dummy.drop(["Date", "Weekly_Sales"], axis=1)
        y = dummy.Weekly_Sales

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

        # build model
        model = LinearRegression()

        self.lr_model = model.fit(x_train, y_train)

