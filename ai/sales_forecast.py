import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_sales(orders_df):
    df = orders_df.copy()

    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")

    df["x"] = range(len(df))

    X = df[["x"]]
    y = df["orders"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[len(df)]]
    prediction = model.predict(next_month)[0]

    return model, df, max(0, round(prediction))