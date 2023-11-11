import re
import numpy as np
from enum import Enum, auto
import pandas as pd
from typing import Callable
import plotly.express as px


class Classes(Enum):
    NotMatched = 0
    Shopping = 1
    Investing = 2
    Vacation = 3
    Grocery = 4
    Restaurant = 5
    Cash = 6
    Transportation = 7
    Entertainment = 8
    FixedCosts = 9
    Paypal = 10


class RuleSet:
    """
    Every function returns a voting for one or more classes if matched and None if not.
    """

    def get_callables(self) -> list[Callable]:
        return [
            self.shopping_0,
            self.investment_0,
            self.vacation_0,
            self.cash_0,
            self.grocery_0,
            self.restaurant_0,
            self.transportation_0,
            self.fixed_costs_0,
            self.entertainment_0,
            self.paypal_0,
        ]

    @staticmethod
    def shopping_0(d: pd.Series):
        if re.match(
            ".*(h&m|snipes|saturn|media|sport|amazon|mode|amzn|ebay|schuh).*",
            d.receiver.lower(),
        ):
            return Classes.Shopping

    @staticmethod
    def investment_0(s):
        if re.match(".*(trade).*", s.receiver.lower()):
            return Classes.Investing

    @staticmethod
    def vacation_0(s):
        if re.match(".*(vacation|travel|air|wings|ski).*", s.receiver.lower()):
            return Classes.Vacation

    @staticmethod
    def grocery_0(s):
        if re.match(
            ".*(edeka|penny|lidl|aldi|dm|budni|bio|rewe|spar|rossmann|kaufland|neukauf|mueller|apoth).*",
            s.receiver.lower(),
        ):
            return Classes.Grocery

    @staticmethod
    def restaurant_0(s):
        if re.match(".*(steak|restaur|cafe|brauhaus|gastst).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(kebab|schatzkiste|eis|ice|coffee).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(hans|brot|selecta|kamps|mcdonalds).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(bakery|bäcker|backhus|baeck).*", s.receiver.lower()):
            return Classes.Restaurant

    @staticmethod
    def cash_0(s):
        if re.match(".*(sparkasse|baden|deutsche bank).*", s.receiver.lower()):
            return Classes.Cash

    @staticmethod
    def transportation_0(s):
        if re.match(
            ".*(ssb|db|auto|fahr|verkehr|hvv|shell|aral|jet).*", s.receiver.lower()
        ):
            return Classes.Transportation

    @staticmethod
    def entertainment_0(s):
        if re.match(".*(prime|museum|jpc|theater).*", s.receiver.lower()):
            return Classes.Entertainment

    @staticmethod
    def fixed_costs_0(s):
        if re.match(".*(congstar|miete|ganguly|schmadalla|axa).*", s.receiver.lower()):
            return Classes.FixedCosts

    @staticmethod
    def paypal_0(s):
        if re.match(".*(paypal).*", s.receiver.lower()):
            return Classes.FixedCosts


class CategoryMatcher:
    def __init__(
        self,
    ):
        self.rules = RuleSet().get_callables()
        self.classes = Classes
        self.indices = [f"match_{c.name.lower()}" for c in Classes]

    def match(self, d: pd.Series):
        masks = []
        for rule in self.rules:
            masks.append(self.get_boolean_mask(rule(d)))
        mask = np.array(masks).sum(axis=0)

        return pd.Series(mask, index=self.indices)

    def get_boolean_mask(self, enum_class=None):
        boolean_mask = np.zeros(len(Classes), dtype=bool)
        if enum_class:
            boolean_mask[enum_class.value] = 1
        return boolean_mask


if __name__ == "__main__":
    import seaborn as sns
    import matplotlib.pyplot as plt

    file = "/mnt/c/Users/LENOVO/Downloads/n26-csv-transactions.csv"
    df = pd.read_csv(file)
    df = df.head(1000)

    df.rename(
        {
            "Empfänger": "receiver",
            "Kontonummer": "account_id",
            "Verwendungszweck": "purpose",
            "Datum": "date",
            "Betrag (EUR)": "amount",
            "Fremdwährung": "currency",
            "Transaktionstype": "type",
        },
        axis=1,
        inplace=True,
    )
    df.drop(
        columns=["Betrag (Fremdwährung)", "Wechselkurs"],
        inplace=True,
    )

    df.date = pd.to_datetime(df.date)
    df.receiver = df.receiver.astype(str)
    df.purpose = df.purpose.astype(str)

    cm = CategoryMatcher()

    df_match = df.apply(cm.match, axis="columns", result_type="expand")

    df = pd.concat([df, df_match], axis=1)

    df_vis = df[[c for c in df.columns if "match" in c]]
    df_vis.set_index(df["receiver"], inplace=True)
    fig = px.imshow(
        df_vis.T,
        aspect="auto",
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="grey")
    fig.show()

    df
