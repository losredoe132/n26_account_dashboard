import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from dotenv import load_dotenv
import argparse

load_dotenv()


def some_func():
    pass


if __name__ == "__main__":
    file = "mnt/c/Users/LENOVO/Downloads/n26-csv-transactions"

    df = pd.read_csv(file)
