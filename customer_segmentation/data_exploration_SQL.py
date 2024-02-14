import os
import sys
import boto3
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from src.functions import connect_to_redshift

# removing warning messages
warnings.filterwarnings("ignore")

# Loading my .env file
load_dotenv()

# defining redshift credentials
dbname = os.getenv("dbname")
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")

# establishing redshift connection
rs_connection = connect_to_redshift(dbname, host, port, user, password)

query = """select *
           from bootcamp.online_transactions_cleaned
        """

online_transaction = pd.read_sql(query, rs_connection)
online_transaction.to_csv("online_transactions.csv")
