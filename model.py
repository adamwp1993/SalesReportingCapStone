import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class Model:

    @staticmethod
    def predict(data):
        # Initialize the Linear regression model
        sales = pd.read_csv("Walmart.csv")


        # Turn stores and holiday flag into a category
        sales.Store = pd.Categorical(sales.Store)
        sales.Holiday_Flag = pd.Categorical(sales.Holiday_Flag)
        sales.describe()

        # Dummy data
        dummy = pd.get_dummies(sales, columns=['Store', 'Holiday_Flag'])

        x = dummy.drop(["Date", "Weekly_Sales"], axis=1)
        y = dummy.Weekly_Sales

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

        # build model
        lrmodel = LinearRegression()

        lrmodel.fit(x_train, y_train)

        # index 0 = temp, 1 = gas, 2 = CPI, 3 = unemployment rate 4-48 = stores, 49 = not holiday, 50 = is holiday,
        # 3 + store number = index of store number
        user_input = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        user_input[0][0] = int(data['temp'])
        user_input[0][1] = float(data['gasPrice'])
        user_input[0][2] = float(data['cpi'])
        user_input[0][3] = float(data['unemployment'])

        is_holiday = int(data['holiday'])
        if is_holiday == 1:
            user_input[0][50] = 1
        elif is_holiday == 0:
            user_input[0][49] = 1

        index = 3 + int(data['storeNum'])
        user_input[0][index] = 1

        result = float(lrmodel.predict(user_input))
        return_list = [0, 0]
        return_list[0] = result
        # Get the Variance / accuracy
        return_list[1] = lrmodel.score(x_test, y_test)

        return return_list
