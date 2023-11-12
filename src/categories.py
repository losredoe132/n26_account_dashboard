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
    Salary = 11
    Household = 12
    Persons = 13
    Ignore = 14


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
            self.salary_0,
            self.household_0,
            self.ignore_0,
            self.persons_0,
        ]

    @staticmethod
    def shopping_0(d: pd.Series):
        if re.match(".*(h&m|snipes|saturn|media|sport|amazon).*", d.receiver.lower()):
            return Classes.Shopping
        if re.match(".*(mode|amzn|ebay|schuh|globetrotter).*", d.receiver.lower()):
            return Classes.Shopping
        if re.match(".*(tedi|p & c|peek & clopp|manufactum).*", d.receiver.lower()):
            return Classes.Shopping
        if re.match(".*(heart.*sole|equipment).*", d.receiver.lower()):
            return Classes.Shopping

    @staticmethod
    def investment_0(s):
        if re.match(".*(trade).*", s.receiver.lower()):
            return Classes.Investing

    @staticmethod
    def vacation_0(s):
        if re.match(".*(vacation|travel|air|wings|ski|baeder).*", s.receiver.lower()):
            return Classes.Vacation
        if re.match(".*(hofgut|super 8|hotel|huette).*", s.receiver.lower()):
            return Classes.Vacation
        if re.match(".*(haus|wet|camping|dancenter).*", s.receiver.lower()):
            return Classes.Vacation

    @staticmethod
    def grocery_0(s):
        if re.match(".*(edeka|penny|lidl|aldi|dm|budni|bio).*", s.receiver.lower()):
            return Classes.Grocery
        if re.match(".*(knolle|kaufland|neukauf|mueller|apoth).*", s.receiver.lower()):
            return Classes.Grocery
        if re.match(".*(rossmann|spar |rewe|sehne|netto).*", s.receiver.lower()):
            return Classes.Grocery
        if re.match(".*(tee.*gschwendner|udo timmer|billa).*", s.receiver.lower()):
            return Classes.Grocery
        if re.match(".*(zettle|backstube|e-center|albert heijn).*", s.receiver.lower()):
            return Classes.Grocery

    @staticmethod
    def household_0(s):
        if re.match(".*(bauhaus|kammerjager|hagebau|butlers).*", s.receiver.lower()):
            return Classes.Household
        if re.match(".*(nanu nana|sostrene grene|hema|vodafone).*", s.receiver.lower()):
            return Classes.Household
        if re.match(".*(ikea|obi).*", s.receiver.lower()):
            return Classes.Household

    @staticmethod
    def restaurant_0(s):
        if re.match(".*(steak|restaur|cafe|brauhaus|gastst).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(kebab|schatzkiste|eis|ice|coffee).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(hans|brot|selecta|kamps|mcdonald).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(bakery|bäcker|backhus|baeck|nur hier).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(b(ae|ä)renschl|espresso|burger|sultans).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(hopfen|backwerk|sumup|mutter|braeu).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(pokkez|peter pane|subway|dean & david).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(le crobag|konditorei|suessholz|yormas).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(bistro|kebap|yormas|keim|wurst).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(cuccis|sofabar|pallas|mexiko).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(pommes|bräu|wohnzimmer|allwoerden).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(tarhan|togoodto|crepes|platzhirsch).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(mata hari|vegi|uzr|gardener|e-aktiv).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(mövenpick|kumpir|sonja merz|asian).*", s.receiver.lower()):
            return Classes.Restaurant
        if re.match(".*(ditsch|dominos|brownies).*", s.receiver.lower()):
            return Classes.Restaurant

    @staticmethod
    def cash_0(s):
        if re.match(".*(sparkasse|baden|bank|vr|cash).*", s.receiver.lower()):
            return Classes.Cash

    @staticmethod
    def transportation_0(s):
        if re.match(".*(ssb|db|auto|fahr|verkehr|hvv|shell).*", s.receiver.lower()):
            return Classes.Transportation
        if re.match(".*(jet|bahn|abellio|aral|lim*|bike).*", s.receiver.lower()):
            return Classes.Transportation
        if re.match(".*(rad|esso|bolt).*", s.receiver.lower()):
            return Classes.Transportation

    @staticmethod
    def entertainment_0(s):
        if re.match(".*(prime|museum|jpc|theater|apple).*", s.receiver.lower()):
            return Classes.Entertainment
        if re.match(".*(buch|osiander|thomann|kopf und steine).*", s.receiver.lower()):
            return Classes.Entertainment
        if re.match(".*(komoot|wunderland|sprung|mojo).*", s.receiver.lower()):
            return Classes.Entertainment
        if re.match(".*(eventim|tixforgs|tickets|club|pier).*", s.receiver.lower()):
            return Classes.Entertainment
        if re.match(".*(steam).*", s.receiver.lower()):
            return Classes.Entertainment

    @staticmethod
    def fixed_costs_0(s):
        if re.match(".*(congstar|miete|ganguly|schmadalla|axa).*", s.receiver.lower()):
            return Classes.FixedCosts
        if re.match(".*(krankenkasse|dav|telekom).*", s.receiver.lower()):
            return Classes.FixedCosts

    @staticmethod
    def paypal_0(s):
        if re.match(".*(paypal).*", s.receiver.lower()):
            return Classes.FixedCosts

    @staticmethod
    def salary_0(s):
        if re.match(".*(lohn|gehalt).*", s.receiver.lower()):
            return Classes.Salary
        if re.match(".*(bosch|arena|trumpf).*", s.receiver.lower()):
            return Classes.Salary

    @staticmethod
    def ignore_0(s):
        if re.match(".*(monat nach hauptkonto).*", s.receiver.lower()):
            return Classes.Ignore
        if re.match(".*(hauptkonto nach monat).*", s.receiver.lower()):
            return Classes.Ignore

    @staticmethod
    def persons_0(s):
        if re.match(".*(anne|jonas|uwe|janne|niklas|jannik|ben).*", s.receiver.lower()):
            return Classes.Persons
        if re.match(".*(clond|verena|klaus roth|max|hannah).*", s.receiver.lower()):
            return Classes.Persons
        if re.match(".*(patrick|nicole|anni|katharina|patricia).*", s.receiver.lower()):
            return Classes.Persons
        if re.match(".*(wiebke|mara|lena|michel|laura).*", s.receiver.lower()):
            return Classes.Persons


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
            mask = self.get_boolean_mask(rule(d))
            masks.append(mask)
        mask = np.array(masks).sum(axis=0)

        # If no rule was applied, select not matched
        if mask.sum() == 0:
            mask = self.get_boolean_mask(Classes.NotMatched)

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

    # Create direction
    df["direction"] = np.where(df.amount > 0, "incoming", "spending")

    # Casting types
    df.date = pd.to_datetime(df.date)
    df.receiver = df.receiver.astype(str)
    df.purpose = df.purpose.astype(str)

    df.drop(df[df["purpose"] == "Von Hauptkonto nach Sparen"].index, inplace=True)
    df.drop(df[df["purpose"] == "Von Sparen nach Hauptkonto"].index, inplace=True)
    df.drop(df[df["purpose"] == "Von Monat nach Hauptkonto"].index, inplace=True)
    df.drop(df[df["purpose"] == "Von Hauptkonto nach Monat"].index, inplace=True)
    df.drop(
        df[df["purpose"] == "space.transfer.referencetext.description"].index,
        inplace=True,
    )

    # Match classes
    cm = CategoryMatcher()
    df_match = df.apply(cm.match, axis="columns", result_type="expand")
    df = pd.concat([df, df_match.idxmax(axis=1).rename("matched_class")], axis=1)

    # df_vis = df[[c for c in df.columns if "match" in c]]
    # df_unmatched = df_vis.loc[np.logical_not(np.any(df_vis, axis=1))]
    # df_unmatched.set_index(
    #     df.loc[np.logical_not(np.any(df_vis, axis=1))]["receiver"], inplace=True
    # )

    # df.resample('M').sum()

    # df=df.resample(rule='M', on='date').sum()

    # Visualize
    # df_vis.set_index(df["receiver"], inplace=True)
    fig = px.bar(
        df,
        x="date",
        y="amount",
        color="matched_class",
        hover_data=["date", "amount", "receiver", "purpose", "matched_class"],
    )

    fig.show()
