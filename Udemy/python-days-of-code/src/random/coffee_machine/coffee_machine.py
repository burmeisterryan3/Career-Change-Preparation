"""Define a coffee machine interaction."""

import json
from os import system
from typing import Literal, Optional

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt, PrivateAttr

OPTIONS = (
    "help",
    "report",
    "prices",
    "off",
    "espresso",
    "latte",
    "cappuccino",
)
LOGO = r"""                                                  
 _____     ___ ___            _____         _   _         
|     |___|  _|  _|___ ___   |     |___ ___| |_|_|___ ___ 
|   --| . |  _|  _| -_| -_|  | | | | .'|  _|   | |   | -_|
|_____|___|_| |_| |___|___|  |_|_|_|__,|___|_|_|_|_|_|___|                                                         
"""


class Ingredients(BaseModel):
    """Ingredients class."""

    water: NonNegativeInt
    milk: Optional[NonNegativeInt] = 0
    coffee: NonNegativeInt


class MenuItem(BaseModel):
    """Menu items class."""

    name: str
    ingredients: Ingredients
    cost: NonNegativeFloat


class Inventory(BaseModel):
    """Inventory class."""

    water: NonNegativeInt
    milk: NonNegativeInt
    coffee: NonNegativeInt


class CoffeeMachine(BaseModel):
    """Define the coffee machine class."""

    _menu_items: dict[str, MenuItem] = PrivateAttr({})
    _supplies: Inventory = PrivateAttr(None)
    _funds: NonNegativeFloat = PrivateAttr(0)

    def __init__(self):
        """Power on the machine."""
        super().__init__()
        system("clear")
        print(f"{LOGO}\n\n")
        print("Coffee machine is waking up and heating the water.")
        # sleep(3)
        print("The coffee machine is ready for use!\n")
        self._initialize_supplies_and_prices()

    def _initialize_supplies_and_prices(self):
        f = open("shop.json")
        data = json.load(f)

        for item in data["menu"]:
            self._menu_items[item["name"]] = MenuItem(
                name=item["name"],
                ingredients=Ingredients(**item["ingredients"]),
                cost=item["cost"],
            )

        self._supplies = Inventory(**data["resources"])

    def power_off(self) -> None:
        """Power off the machine."""
        print()
        print("Thanks for using the coffee machine.")
        print("Goodbye!")

    def prompt_user(self) -> str:
        """Ask the user what they would like."""
        selection = ""
        while selection not in OPTIONS:
            selection = input(
                "Would you like an espresso, latte, or cappuccino? "
            )

        return selection

    def help(self) -> None:
        """Print a help message for the user."""
        print()
        print("Select a drink from the options provided.")
        print(
            "Insert sufficient coinage to ensure you can purchase the drink."
        )
        print(
            "If not enough supplies are available, the drink is unavailable."
        )
        print()

    def report(self) -> None:
        """Print a report of the current status."""
        print()
        print(f"Water: {self._supplies.water}ml")
        print(f"Milk: {self._supplies.milk}ml")
        print(f"Coffee: {self._supplies.coffee}g")
        print(f"Money: ${self._funds:0.2f}")
        print()

    def prices(self) -> None:
        """Print the prices for all items on the menu."""
        print()
        for _, item in self._menu_items.items():
            print(f"{getattr(item, "name")}: ${getattr(item, "cost"):0.2f}")
        print()

    def sufficient_resources(
        self, selection=Literal["latte", "cappuccino", "espresso"]
    ) -> None:
        """Check whether the inventory can support the ingredients required by the chosen drink."""
        sufficient_resources = True
        insufficient_ingredients = []
        for ingredient in ["milk", "coffee", "water"]:
            if getattr(self._supplies, ingredient) < getattr(
                self._menu_items[selection].ingredients, ingredient
            ):
                insufficient_ingredients.append(ingredient)
                sufficient_resources = False

        if not sufficient_resources:
            print(
                f"Sorry, we don't have enough of the following ingredients: {", ".join(insufficient_ingredients)}."
            )
        return sufficient_resources

    def process_payment(self, selection) -> bool:
        """Process payment for the drink selection."""
        num_quarters = int(input("How many quarters? "))
        num_dimes = int(input("How many dimes? "))
        num_nickels = int(input("How many nickels? "))
        num_pennies = int(input("How many pennies? "))

        payment = (
            0.25 * num_quarters
            + 0.1 * num_dimes
            + 0.05 * num_nickels
            + 0.01 * num_pennies
        )

        cost = self._menu_items[selection].cost
        if payment < cost:
            print(
                f"Insufficient funds. A {selection} costs ${cost:0.2f}, and you provided ${payment:0.2f}."
            )
            return False
        else:
            cm._funds += cost
            if payment > cost:
                print(
                    f"Thank you! Here is ${payment-cost:0.2f} back in change."
                )
            return True

    def make_coffee(self, selection):
        """Update the inventory based on the selection."""
        for k in self._supplies.__dict__.keys():
            self._supplies.__dict__[k] -= getattr(
                self._menu_items[selection].ingredients, k
            )

        print(f"Here is your {selection}! Have a great day!")


if __name__ == "__main__":
    cm = CoffeeMachine()

    while True:
        selection = cm.prompt_user()

        if selection == "off":
            break
        elif selection == "help":
            cm.help()
        elif selection == "report":
            cm.report()
        elif selection == "prices":
            cm.prices()
        elif selection in ["espresso", "latte", "cappuccino"]:
            if cm.sufficient_resources(selection):
                if cm.process_payment(selection):
                    cm.make_coffee(selection)
        else:
            continue

    cm.power_off()
