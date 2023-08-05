import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")

        # Create widgets for the main scene
        self.label = tk.Label(root, text="Hello, GUI!")
        self.button = tk.Button(root, text="Click Me!", command=self.on_button_click)

        # Grid layout for the main scene
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        # Data for the line graph
        self.x_data = []
        self.y_data = []

    def on_button_click(self):
        # Hide the widgets of the main scene
        self.label.grid_forget()
        self.button.grid_forget()

        # Switch to the stock exchange scene
        self.stock_exchange = StockExchange(self.root, self.back_to_main_scene, self.x_data, self.y_data)

    def back_to_main_scene(self):
        # Destroy the stock exchange scene and return to the main scene
        self.stock_exchange.destroy()
        # Restore the widgets of the main scene
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)


class StockExchange:
    def __init__(self, root, on_back_button_click, x_data, y_data):
        self.root = root
        self.on_back_button_click = on_back_button_click
        self.x_data = x_data
        self.y_data = y_data
        self.current_index = 0
        self.money = 200
        self.stocks = 0

        # Create widgets for the stock exchange scene
        self.new_label = tk.Label(self.root, text="Stock Exchange")
        self.back_button = tk.Button(self.root, text="Go Back", command=self.on_back_button_click)
        self.plot_button = tk.Button(self.root, text="Add Data Point", command=self.add_data_point)
        self.current_value_label = tk.Label(self.root, text="Current Y-Value: ")
        self.buy_button = tk.Button(self.root, text="Buy", command=self.buy_stock)
        self.sell_button = tk.Button(self.root, text="Sell", command=self.sell_stock)
        self.stocks_label = tk.Label(self.root, text="Stocks: 0")
        self.money_label = tk.Label(self.root, text="Money: $200")

        # Grid layout for the stock exchange scene
        self.new_label.grid(row=0, column=0, padx=10, pady=10)
        self.back_button.grid(row=1, column=0, padx=10, pady=10)
        self.plot_button.grid(row=2, column=0, padx=10, pady=10)
        self.current_value_label.grid(row=3, column=0, padx=10, pady=10)
        self.buy_button.grid(row=4, column=0, padx=10, pady=10)
        self.sell_button.grid(row=5, column=0, padx=10, pady=10)
        self.stocks_label.grid(row=6, column=0, padx=10, pady=10)
        self.money_label.grid(row=7, column=0, padx=10, pady=10)

        # Create the line graph
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.line, = self.ax.plot(self.x_data, self.y_data, marker='o', color='b')
        self.ax.set_xlabel("X Data")
        self.ax.set_ylabel("Y Data")

        # Create canvas to display the line graph
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=10, pady=10)

    def destroy(self):
        # Hide and destroy widgets of the stock exchange scene
        self.new_label.grid_forget()
        self.back_button.grid_forget()
        self.plot_button.grid_forget()
        self.current_value_label.grid_forget()
        self.buy_button.grid_forget()
        self.sell_button.grid_forget()
        self.stocks_label.grid_forget()
        self.money_label.grid_forget()
        self.canvas.get_tk_widget().grid_forget()

    def add_data_point(self):
        x_value = len(self.x_data) + 1
        y_value = random.randint(0, 100)

        # Add data points to the lists
        self.x_data.append(x_value)
        self.y_data.append(y_value)

        # Update the line graph
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Update the current value label
        self.current_index = len(self.x_data) - 1
        self.current_value_label.config(text=f"Current Y-Value: {self.y_data[self.current_index]}")

    def buy_stock(self):
        if self.current_index >= 0 and self.current_index < len(self.y_data):
            stock_value = self.y_data[self.current_index]
            if self.money >= stock_value:
                self.stocks += 1
                self.money -= stock_value
                self.stocks_label.config(text=f"Stocks: {self.stocks}")
                self.money_label.config(text=f"Money: ${self.money}")

    def sell_stock(self):
        if self.current_index >= 0 and self.current_index < len(self.y_data) and self.stocks > 0:
            stock_value = self.y_data[self.current_index]
            self.stocks -= 1
            self.money += stock_value
            self.stocks_label.config(text=f"Stocks: {self.stocks}")
            self.money_label.config(text=f"Money: ${self.money}")


if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
