import pickle
import tkinter as tk


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class Meal(MenuItem):
    def __init__(self, number, name, price, calories, description, is_combo=True):
        super().__init__(name, price)
        self.number = number
        self.description = description
        self.is_combo = is_combo
        self.size = "medium"
        self.calory = calories

    def __str__(self):
        combo_text = "Combo" if self.is_combo else "Single"
        return (f"#{self.number} {self.name} ({combo_text}) - {self.size.capitalize()} "
                f"- ${self.price:.2f} ({self.calory} Calories)\n    {self.description}")


class Burger(MenuItem):
    def __init__(self, name, price, calories, patty_count=1):
        super().__init__(name, price)
        self.patty_count = patty_count
        self.calory = calories


    def __str__(self):
        return f"{self.name} - {self.patty_count} patty - {self.price:.2f} ({self.calory} Calories)"

class Side(MenuItem):
    def __init__(self, name, price, calories, portion_count=1):
        super().__init__(name, price)
        self.calories = calories
        self.portion_count = portion_count

    def __str__(self):
        portion_text = f"{self.portion_count} Portion{'s' if self.portion_count > 1 else ''}"
        return f"{self.name} - ${self.price:.2f} ({self.calories} Cal per portion, {portion_text})"


class Dessert(MenuItem):
    def __init__(self, name, price, calories, serving_count=1):
        super().__init__(name, price)
        self.calories = calories
        self.serving_count = serving_count

    def add_serving(self):
        self.serving_count += 1
        self.price += 1.50

    def __str__(self):
        serving_text = f"{self.serving_count} Serving{'s' if self.serving_count > 1 else ''}"
        return f"{self.name} - ${self.price:.2f} ({self.calories} Cal per serving, {serving_text})"


class Salad(MenuItem):
    def __init__(self, name, price, calories, serving_count=1):
        super().__init__(name, price)
        self.calories = calories
        self.serving_count = serving_count

    def __str__(self):
        serving_text = f"{self.serving_count} Serving{'s' if self.serving_count > 1 else ''}"
        return f"{self.name} - ${self.price:.2f} ({self.calories} Cal per serving, {serving_text})"


class Shake(MenuItem):
    def __init__(self, name, price, calories):
        super().__init__(name, price)
        self.calories = calories

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} ({self.calories} Calories)"


class WhataburgerMenu:
    def __init__(self):
        self.meals = [
            Meal(1, "Whataburger Meal", 9.59,  860,"Classic Whataburger with fries and drink"),
            Meal(2, "Double Meat Whataburger Meal", 10.79, 1000, "Two beef patties, fries, and drink"),
            Meal(3, "Triple Meat Whataburger Meal", 12.29, 1340, "Three beef patties, fries, and drink"),
            Meal(4, "Jalapeño & Cheese Whataburger Meal", 10.19, 950, "Whataburger with jalapeños, cheese, fries, and drink"),
        ]
        self.burgers = [
            Burger("Whataburger", 5.99, 590, patty_count=1),
            Burger("Double Meat Whataburger", 7.19, 830, patty_count=2),
            Burger("Triple Meat Whataburger", 8.69, 1070, patty_count=3),
        ]
        self.sides = [
            Side("French Fries", 2.59, 270),
            Side("Onion Rings", 3.79, 300),
            Side("Apple Slices", 1.69, 30),
        ]
        self.desserts = [
            Dessert("Hot Apple Pie", 1.79, 270),
            Dessert("Chocolate Chip Cookie", 1.89, 330),
            Dessert("Cinnamon Roll", 2.99, 580),
        ]
        self.salads = [
            Salad("Apple & Cranberry Chicken Salad", 8.99, 390),
            Salad("Apple Salad", 8.99, 390)

        ]
        self.shakes = [
            Shake("Chocolate Shake", 3.99, 500),
            Shake("Vanilla Shake", 3.99, 450),
            Shake("Strawberry Shake", 3.99, 480),
        ]

    def display_menu(self):
        print("\n===== Whataburger Menu =====")
        print("\nCombo Meals:")
        for meal in self.meals:
            print(meal)
        print("\nBurgers:")
        for burger in self.burgers:
            print(burger)
        print("\nSides:")
        for side in self.sides:
            print(side)
        print("\nDesserts:")
        for dessert in self.desserts:
            print(dessert)
        print("\nSalads:")
        for salad in self.salads:
            print(salad)
        print("\nShakes:")
        for shake in self.shakes:
            print(shake)


class Order:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price
        print(f"{item.name} added to your order!")

    def remove_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                self.total -= item.price
                print(f"{item.name} removed from your order!")
                return
        print(f"Item '{item_name}' not found in your order.")

    def view_order(self):
        if not self.items:
            print("Your order is empty!")
        else:
            print("\n===== Current Order =====")
            for item in self.items:
                print(item)
            print(f"Total: ${self.total:.2f}")

    def save_order(self, file_path="order.pkl"):
        if not self.items:
            print("Your order is empty! Nothing to save.")
            return
        try:
            with open(file_path, "wb") as file:
                pickle.dump(self, file)
            print(f"Order saved to {file_path}!")
        except Exception as e:
            print(f"Failed to save the order: {e}")

    def load_order(file_path="order.pkl"):
        try:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f"No saved order found at {file_path}.")
        except Exception as e:
            print(f"Failed to load the order: {e}")
        return None

    def apply_discount(self, percentage):
        if not self.items:
            print("Your order is empty! No discount can be applied.")
            return
        discount = self.total * (percentage / 100)
        self.total -= discount
        print(f"Discount of {percentage}% applied. You saved ${discount:.2f}!")

    def print_receipt(self):
        if not self.items:
            print("Your order is empty! No receipt to print.")
            return
        root = tk.Tk()
        root.title("Receipt")
        title = tk.Label(root, text="Whataburger Receipt", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        for item in self.items:
            item_label = tk.Label(root, text=str(item), font=("Helvetica", 12))
            item_label.pack(anchor="w", padx=20)
        total_label = tk.Label(root, text=f"Total: ${self.total:.2f}", font=("Helvetica", 14, "bold"))
        total_label.pack(pady=10)
        close_button = tk.Button(root, text="Close", command=root.destroy)
        close_button.pack(pady=10)
        root.mainloop()

        self.items = []
        self.total = 0.0
        print("Your order has been cleared after printing the receipt.")


def display_main_menu():
    print("\n===== Whataburger Ordering System =====")
    print("1. View Menu")
    print("2. Add an Item to Your Order")
    print("3. Remove an Item from Your Order")
    print("4. View Your Current Order")
    print("5. Save Your Order")
    print("6. Load a Saved Order")
    print("7. Apply Discount")
    print("8. Print Receipt")
    print("9. Exit")


def main():
    menu = WhataburgerMenu()
    order = Order()

    while True:
        display_main_menu()
        choice = input("Please select an option: ")

        if choice == "1":
            menu.display_menu()

        elif choice == "2":
            menu.display_menu()
            item_name = input("Enter the name of the item to add: ").lower()
            found = False
            for category in [menu.meals, menu.burgers, menu.sides, menu.desserts, menu.salads, menu.shakes]:
                for item in category:
                    if item.name.lower() == item_name:
                        order.add_item(item)
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"Item '{item_name}' not found in the menu.")

        elif choice == "3":
            item_name = input("Enter the name of the item to remove: ")
            order.remove_item(item_name)

        elif choice == "4":
            order.view_order()

        elif choice == "5":
            file_path = input("Enter file name to save the order: ")
            order.save_order(file_path)

        elif choice == "6":
            file_path = input("Enter file name to load the order: ")
            loaded_order = Order.load_order(file_path)
            if loaded_order:
                order = loaded_order
                print("Order successfully loaded!")

        elif choice == "7":
            try:
                discount = float(input("Enter the discount percentage (0-100): "))
                if 0 <= discount <= 100:
                    order.apply_discount(discount)
                else:
                    print("Invalid percentage. Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        elif choice == "8":
            order.print_receipt()

        elif choice == "9":
            print("Thank you for visiting Whataburger! Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
