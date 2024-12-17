import pickle
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class Meal(MenuItem):
    def __init__(self, number, name, price, description, is_combo=True):
        super().__init__(name, price)
        self.number = number
        self.description = description
        self.is_combo = is_combo
        self.size = "medium"

    def __str__(self):
        combo_text = "Combo" if self.is_combo else "Single"
        return (f"#{self.number} {self.name} ({combo_text}) - {self.size.capitalize()} "
                f"- ${self.price:.2f}\n    {self.description}")


class Order:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

    def remove_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                self.total -= item.price
                return True
        return False

    def apply_discount(self, percentage):
        discount = self.total * (percentage / 100)
        self.total -= discount
        return discount

    def save_order(self, file_path="order.pkl"):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load_order(file_path="order.pkl"):
        with open(file_path, "rb") as file:
            return pickle.load(file)

    def clear_order(self):
        self.items = []
        self.total = 0.0


class WhataburgerMenu:
    def __init__(self):
        self.meals = [
            Meal(1, "Whataburger", 9.59, "Classic Whataburger with fries and drink"),
            Meal(2, "Double Meat Whataburger", 10.79, "Two beef patties, fries, and drink"),
            Meal(3, "Triple Meat Whataburger", 12.29, "Three beef patties, fries, and drink"),
            Meal(4, "Jalapeño & Cheese Whataburger", 10.19, "Whataburger with jalapeños, cheese, fries, and drink"),
            Meal(5, "Bacon & Cheese Whataburger", 10.89, "Whataburger with bacon, cheese, fries, and drink"),
            Meal(6, "Avocado Bacon Burger", 10.99, "Cheese and creamy pepper sauce on Texas Toast"),
            Meal(7, "Whataburger Jr.", 6.99, "Smaller Whataburger with fries and drink"),
            Meal(8, "Double Meat Whataburger Jr.", 7.99, "Double meat smaller burger, fries, and drink"),
            Meal(9, "Whatachick’n Sandwich", 9.59, "Crispy chicken sandwich, fries, and drink"),
            Meal(10, "Grilled Chicken Sandwich", 10.49, "Grilled chicken sandwich, fries, and drink"),
            Meal(11, "Spicy Chicken Sandwich", 9.79, "Spicy chicken sandwich, fries, and drink"),
            Meal(12, "Whatachick’n Strips (3-piece)", 8.99, "Three crispy chicken strips, fries, and drink"),
        ]
        self.burgers = [
            MenuItem("S Whataburger", 5.99),
            MenuItem("S Double Meat Whataburger", 7.19),
            MenuItem("S Triple Meat Whataburger", 8.69),
            MenuItem("S Jalapeño & Cheese Whataburger", 7.29),
            MenuItem("S Bacon & Cheese Whataburger", 7.29),
            MenuItem("S Avocado Bacon Burger", 7.49),
            MenuItem("S Double Meat Whataburger Jr.", 4.59),
            MenuItem("S Whataburger Jr.", 3.69),
            MenuItem("S Whatachick'n Sandwich", 5.99),
            MenuItem("S Grilled Chicken Sandwich", 6.89),
            MenuItem("S Spicy Chicken Sandwich", 6.29),
            MenuItem("S Whatachick'n Strips (3-piece)", 5.39),
        ]
        self.sides = [
            MenuItem("French Fries", 2.59),
            MenuItem("Onion Rings", 3.79),
            MenuItem("Apple Slices", 1.69),
        ]
        self.desserts = [
            MenuItem("Hot Apple Pie", 1.79),
            MenuItem("Chocolate Chip Cookie", 1.89),
            MenuItem("Cinnamon Roll", 2.99),
        ]
        self.salads = [
            MenuItem("Apple & Cranberry Chicken Salad", 8.99),
            MenuItem("Cobb Salad", 7.59),
        ]
        self.shakes = [
            MenuItem("Chocolate Shake", 3.99),
            MenuItem("Vanilla Shake", 3.99),
            MenuItem("Strawberry Shake", 3.99),
        ]

    def get_all_items(self):
        return self.meals + self.burgers + self.sides + self.desserts + self.salads + self.shakes


class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whataburger Register System")
        self.menu = WhataburgerMenu()
        self.order = Order()

        self.build_ui()

    def build_ui(self):
        # Menu Frame
        menu_frame = tk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.menu_listbox = tk.Listbox(menu_frame, height=30, width=50)
        self.menu_listbox.pack(padx=10, pady=10)
        self.update_menu_listbox()

        tk.Button(menu_frame, text="Add to Order", command=self.add_to_order).pack(pady=5)

        # Order Frame
        order_frame = tk.LabelFrame(self.root, text="Order")
        order_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.order_listbox = tk.Listbox(order_frame, height=30, width=50)
        self.order_listbox.pack(padx=10, pady=10)

        tk.Button(order_frame, text="Remove Item", command=self.remove_from_order).pack(pady=5)
        tk.Button(order_frame, text="Apply Discount", command=self.apply_discount).pack(pady=5)
        tk.Button(order_frame, text="Save Order", command=self.save_order).pack(pady=5)
        tk.Button(order_frame, text="Load Order", command=self.load_order).pack(pady=5)
        tk.Button(order_frame, text="Print Receipt", command=self.print_receipt).pack(pady=5)

        # Total Label
        self.total_label = tk.Label(order_frame, text="Total: $0.00", font=("Arial", 14))
        self.total_label.pack(pady=10)

    def update_menu_listbox(self):
        self.menu_listbox.delete(0, tk.END)
        for item in self.menu.get_all_items():
            self.menu_listbox.insert(tk.END, f"{item.name} - ${item.price:.2f}")

    def update_order_listbox(self):
        self.order_listbox.delete(0, tk.END)
        for item in self.order.items:
            self.order_listbox.insert(tk.END, str(item))
        self.total_label.config(text=f"Total: ${self.order.total:.2f}")

    def add_to_order(self):
        selected_index = self.menu_listbox.curselection()
        if selected_index:
            selected_item = self.menu.get_all_items()[selected_index[0]]
            self.order.add_item(selected_item)
            self.update_order_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a menu item to add.")

    def remove_from_order(self):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            selected_item = self.order.items[selected_index[0]]
            self.order.remove_item(selected_item.name)
            self.update_order_listbox()
        else:
            messagebox.showwarning("Warning", "Please select an item to remove.")

    def apply_discount(self):
        discount_percentage = simpledialog.askfloat("Discount", "Enter discount percentage (0-100):")
        if discount_percentage is not None:
            discount = self.order.apply_discount(discount_percentage)
            self.update_order_listbox()
            messagebox.showinfo("Discount Applied", f"A discount of ${discount:.2f} has been applied.")

    def save_order(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            self.order.save_order(file_path)
            messagebox.showinfo("Order Saved", "The order has been saved successfully.")

    def load_order(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            loaded_order = Order.load_order(file_path)
            if loaded_order:
                self.order = loaded_order
                self.update_order_listbox()
                messagebox.showinfo("Order Loaded", "The order has been loaded successfully.")

    def print_receipt(self):
        if not self.order.items:
            messagebox.showwarning("Warning", "The order is empty!")
            return

        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_text = tk.Text(receipt_window, width=40, height=20)
        receipt_text.pack(padx=10, pady=10)

        for item in self.order.items:
            receipt_text.insert(tk.END, f"{item}\n")
        receipt_text.insert(tk.END, f"\nTotal: ${self.order.total:.2f}")

        self.order.clear_order()
        self.update_order_listbox()
        receipt_text.config(state=tk.DISABLED)

        tk.Button(receipt_window, text="Close", command=receipt_window.destroy).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterApp(root)
    root.mainloop()
