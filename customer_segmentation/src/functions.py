import psycopg2
import pandas as pd


def connect_to_redshift(dbname, host, port, user, password):
    # Function that connects to redshift

    connect = psycopg2.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    )

    print("connection to redshift made")

    return connect


def normalize(data_column):
    # Function that normalizes data_column
    min = data_column.min()
    max = data_column.max()
    norm = (data_column - min) / (max - min)

    return norm


def clean_data(data_frame):
    # dropping transactions with price = 0
    data_frame.drop(data_frame[data_frame["price"] == 0].index, axis=0, inplace=True)
    data_frame.reset_index(inplace=True, drop=True)

    # Grouping the data by customer and stock code to get the transactions with their returns
    invoice_list = data_frame.groupby(["customer_id", "stock_code"]).agg(
        {"invoice": list, "quantity": "sum"}
    )
    invoice_list = invoice_list[
        data_frame.groupby(["customer_id", "stock_code"])["quantity"].sum() <= 0
    ].reset_index()

    # getting the index of the returned transactions
    invoice_idx = []
    [invoice_idx.extend(ids) for ids in invoice_list["invoice"]]

    # Assigning returns whose order is inside the time interval of the dataset
    returns = data_frame[data_frame["invoice"].isin(invoice_idx)]

    # Dataset without returns with order is inside the time interval of the dataset
    online_trans = data_frame.drop(returns.index, axis=0).reset_index()

    # The negative values on the remaining data are considered return whose transactions were done outside the time interval of the data
    retunr_wt_trans = online_trans[online_trans["quantity"] <= 0]

    # Dropping returned data without transaction on the time interval of the dataframe
    online_trans.drop(retunr_wt_trans.index, axis=0, inplace=True)

    # Changing the name of the index column to stress that it is the index of the data with returns
    online_trans.rename(columns={"index": "old_index"}, inplace=True)

    # Recalculating total_order_value
    online_trans["total_order_value"] = online_trans["price"] * online_trans["quantity"]

    # Changing invoice_date type to datetime
    online_trans["invoice_date"] = pd.to_datetime(online_trans["invoice_date"])

    # Setting up monthly, yearly, daily data
    invoice_date = online_trans["invoice_date"]
    online_trans["invoice_year"] = invoice_date.dt.year
    online_trans["invoice_month"] = invoice_date.dt.month
    online_trans["invoice_day"] = invoice_date.dt.day
    online_trans["invoice_weekday"] = invoice_date.dt.dayofweek
    online_trans["invoice_dayname"] = invoice_date.dt.day_name()

    return online_trans
