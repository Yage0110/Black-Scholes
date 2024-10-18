import tkinter as tk
from tkinter import ttk
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BlackScholes import BlackScholes
from database import OptionPricingDatabase  


class OptionPricingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Option Pricing with Black-Scholes")
        self.root.geometry("900x700") 

        self.create_layout()

        # Initialize the database connection
        self.db = OptionPricingDatabase()

    def create_layout(self):
        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(7, weight=1)  # Allow dynamic row resizing
        self.root.rowconfigure(8, weight=1)  # Heatmap section

        # Add widgets for inputs
        self.current_price_var = tk.DoubleVar(value=100)
        self.strike_var = tk.DoubleVar(value=100)
        self.volatility_var = tk.DoubleVar(value=0.2)
        self.interest_rate_var = tk.DoubleVar(value=0.05)
        self.time_to_maturity_var = tk.DoubleVar(value=1)
        self.call_purchase_price_var = tk.DoubleVar(value=10)
        self.put_purchase_price_var = tk.DoubleVar(value=10)

        self.create_input_widgets()

        # Create frame for PnL results
        self.pnl_frame = ttk.Frame(self.root)
        self.pnl_frame.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky='n')

        # Add result labels
        self.create_result_labels()

        # Add buttons for actions
        self.create_buttons()

    def create_input_widgets(self):
        labels = [
            "Current Price:", 
            "Strike Price:", 
            "Volatility:", 
            "Interest Rate:", 
            "Time to Maturity:", 
            "Call Purchase Price:", 
            "Put Purchase Price:"
        ]
        variables = [
            self.current_price_var, 
            self.strike_var, 
            self.volatility_var, 
            self.interest_rate_var, 
            self.time_to_maturity_var, 
            self.call_purchase_price_var, 
            self.put_purchase_price_var
        ]

        for i, (label, var) in enumerate(zip(labels, variables)):
            ttk.Label(self.root, text=label).grid(row=i, column=0, sticky='w', padx=10)
            ttk.Entry(self.root, textvariable=var).grid(row=i, column=1, padx=10, pady=5, sticky='ew')

    def create_result_labels(self):
        self.call_pnl_label = ttk.Label(self.pnl_frame, text="Call PnL: ")
        self.put_pnl_label = ttk.Label(self.pnl_frame, text="Put PnL: ")
        self.call_pnl_label.grid(row=0, column=0, pady=5, sticky='w')
        self.put_pnl_label.grid(row=1, column=0, pady=5, sticky='w')

    def create_buttons(self):
        # Button frame centered
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)

        # Center buttons within the frame
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # PnL Calculation button
        ttk.Button(button_frame, text="Calculate PnL", command=self.calculate_pnl).grid(row=0, column=0, padx=5)

        # Heatmap generation button
        ttk.Button(button_frame, text="Generate Heatmaps", command=self.generate_heatmaps).grid(row=0, column=1, padx=5)

        # Database view button
        ttk.Button(button_frame, text="View Previous Runs", command=self.view_previous_runs).grid(row=0, column=2, padx=5)

    def view_previous_runs(self):
        # Get data from the database
        rows = self.db.view_previous_runs()

        # Display results in a new window
        result_window = tk.Toplevel(self.root)
        result_window.title("Previous Runs")

        # Create a Treeview widget for structured display
        tree = ttk.Treeview(result_window, columns=("ID", "Current Price", "Strike Price", "Volatility", "Interest Rate", "Time to Maturity", "Call Purchase Price", "Put Purchase Price", "Call PnL", "Put PnL"), show='headings')

        # Define headings
        tree.heading("ID", text="ID")
        tree.heading("Current Price", text="Current Price")
        tree.heading("Strike Price", text="Strike Price")
        tree.heading("Volatility", text="Volatility")
        tree.heading("Interest Rate", text="Interest Rate")
        tree.heading("Time to Maturity", text="Time to Maturity")
        tree.heading("Call Purchase Price", text="Call Purchase Price")
        tree.heading("Put Purchase Price", text="Put Purchase Price")
        tree.heading("Call PnL", text="Call PnL")
        tree.heading("Put PnL", text="Put PnL")

        # Adjust the column widths
        for col in ("ID", "Current Price", "Strike Price", "Volatility", 
                    "Interest Rate", "Time to Maturity", 
                    "Call Purchase Price", "Put Purchase Price", 
                    "Call PnL", "Put PnL"):
            tree.column(col, width=100)  # Adjust width as needed

        # Insert data into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Pack the treeview widget
        tree.pack(expand=True, fill='both')

    def generate_heatmaps(self):
        spot_range = np.linspace(self.current_price_var.get() * 0.8, self.current_price_var.get() * 1.2, 10)
        vol_range = np.linspace(self.volatility_var.get() * 0.5, self.volatility_var.get(), 10)

        call_prices = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))

        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_temp = BlackScholes(
                    self.time_to_maturity_var.get(),
                    self.strike_var.get(),
                    spot,
                    vol,
                    self.interest_rate_var.get()
                )
                prices = bs_temp.calculate_prices()
                call_prices[i, j] = prices['call_price']
                put_prices[i, j] = prices['put_price']

        custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", ["red", "yellow", "green"])

        # Place heatmaps side by side
        self.create_side_by_side_heatmaps(call_prices, put_prices, spot_range, vol_range, custom_cmap)

    def create_side_by_side_heatmaps(self, call_prices, put_prices, spot_range, vol_range, cmap):
        heatmap_frame = ttk.Frame(self.root)
        heatmap_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Make the frame expand
        self.root.rowconfigure(8, weight=1)

        # Plot call and put heatmaps side by side
        self.plot_heatmap(call_prices, spot_range, vol_range, 'CALL Prices', heatmap_frame, cmap, 0)
        self.plot_heatmap(put_prices, spot_range, vol_range, 'PUT Prices', heatmap_frame, cmap, 1)

    def plot_heatmap(self, data, x_range, y_range, title, container, cmap, column):
        fig, ax = plt.subplots(figsize=(7 , 4))  #Adjusted to make it wider

        sns.heatmap(
            data, 
            xticklabels=np.round(x_range, 2), 
            yticklabels=np.round(y_range, 2), 
            annot=True, 
            fmt=".2f", 
            cmap=cmap, 
            ax=ax, 
            cbar_kws={"label": title, "orientation": "vertical"},
            linewidths=.5,
            linecolor='black'
        )

        ax.set_title(title)
        ax.set_xlabel("Spot Price")
        ax.set_ylabel("Volatility")

        plt.tight_layout()

        # Place the canvas within the frame
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.get_tk_widget().grid(row=0, column=column, padx=5, pady=5, sticky='nsew')

        canvas.draw()

    def calculate_pnl(self):
        # Create a BlackScholes object for calculations
        bs_model = BlackScholes(
            self.time_to_maturity_var.get(),
            self.strike_var.get(),
            self.current_price_var.get(),
            self.volatility_var.get(),
            self.interest_rate_var.get()
        )

        # Calculate option prices
        prices = bs_model.calculate_prices()

        # Get the purchase prices
        call_purchase_price = self.call_purchase_price_var.get()
        put_purchase_price = self.put_purchase_price_var.get()

        # Calculate PnL
        call_pnl = prices['call_price'] - call_purchase_price
        put_pnl = prices['put_price'] - put_purchase_price

        # Update result labels
        self.call_pnl_label.config(text=f"Call PnL: {call_pnl:.2f}")
        self.put_pnl_label.config(text=f"Put PnL: {put_pnl:.2f}")

        # Store the run in the database
        self.db.store_run(
            self.current_price_var.get(),
            self.strike_var.get(),
            self.volatility_var.get(),
            self.interest_rate_var.get(),
            self.time_to_maturity_var.get(),
            call_purchase_price,
            put_purchase_price,
            call_pnl,
            put_pnl
        )

    def close_connection(self):
        self.db.close_connection()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptionPricingApp(root)
    root.mainloop()
