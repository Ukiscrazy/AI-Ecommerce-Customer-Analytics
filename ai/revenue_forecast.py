import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_revenue(revenue_df):

    df = revenue_df.copy()

    df["month"] = pd.to_datetime(df["month"])

    df = df.sort_values("month")

    df["x"] = range(len(df))

    X = df[["x"]]

    y = df["revenue"]

    model = LinearRegression()

    model.fit(X, y)

    next_month = pd.DataFrame(
        {"x": [len(df)]}
    )

    prediction = model.predict(next_month)[0]

    growth = (
        (
            prediction - df["revenue"].iloc[-1]
        )
        / df["revenue"].iloc[-1]
    ) * 100

    return (
        model,
        df,
        round(prediction, 2),
        round(growth, 2)
    )