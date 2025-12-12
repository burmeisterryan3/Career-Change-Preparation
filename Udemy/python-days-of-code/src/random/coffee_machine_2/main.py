"""Day 16."""

from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine

if __name__ == "__main__":
    cm = CoffeeMaker()
    menu = Menu()
    mm = MoneyMachine()

    while True:
        selection = input(
            f"Which of the following would you like: {', '.join(menu.get_items().split('/')[:-1])}? "
        )

        if selection == "off":
            break
        elif selection == "report":
            cm.report()
            mm.report()
        else:
            drink = menu.find_drink(selection)

            if (
                drink is not None
                and cm.is_resource_sufficient(drink)
                and mm.make_payment(drink.cost)
            ):
                cm.make_coffee(drink)
