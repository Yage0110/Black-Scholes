![Stock_Img](https://www.stockdaddy.in/_next/image?url=https%3A%2F%2Femt-stockdaddy-prod.s3.ap-south-1.amazonaws.com%2FPUBLIC%2FASSETS%2F1698211669953Black%2520Scholes%2520Model%2520what%2520is%2520it%252C%2520formula%252C%2520calculator%2520-%2520stockdaddy.jpg&w=1920&q=75)




# Project Title: Option Pricing Application with Black-Scholes Model

## Description:

This project implements an options pricing application based on the Black-Scholes model. It includes modules for calculating option prices and managing option pricing data. The application allows users to compute Call and Put prices, deltas, and gamma for options. It also provides a graphical user interface (GUI) for interacting with the pricing tool, storing historical runs in a database, and visualizing PnL (Profit and Loss).

## Features:

 -  ### Black-Scholes Model:
  
    - Calculates option prices (Call, Put) and Greeks (Delta, Gamma).
    - Computes profit and loss (PnL) for Call and Put options.
 -  ### Database Integration:
    - Stores option parameters and results into an SQLite database.
    - Manages historical pricing data.
 -  ### GUI Interface:
    - User-friendly interface for inputting option parameters.
    - Visualizes PnL results.
## Installation:

1. Clone the repository.
2. Install dependencies
```
pip install numpy scipy sqlite3 matplotlib seaborn tkinter
```

3. Run the main application:
```
python OptionsPricingApp.py
```

## Usage:

- Launch the application.
- Input Option Parameters:
  - The following fields in the GUI need inputs for the parameters of the option pricing calculation:
  - Current Price (Spot Price): Enter the current price of the stock.
  - Strike Price: Enter the price where the option can be done.
  - Volatility (as a percentage): Enter the volatility (how much the stock price fluctuates) as a percentage. Ex. if the volatility is 20%, enter 0.20.
  - Interest Rate (as a percentage): Enter the risk-free interest rate as a decimal. Ex. enter 0.05 for 5%.
  - Time to Maturity (in years): Input the time remaining until the option expires. Ex. if the option has 6 months left, enter 0.5.
  - Optional (Purchase Prices for PnL):
    - Call Purchase Price: If you purchased a call option, enter the price.
    - Put Purchase Price: If you purchased a put option, enter the price.

- Click "Calculate PnL" to Compute Prices and Profit/Loss:
- Generate a Heatmap for a visual:
  - The "Generate Heatmap" button will create a visual representation of the option pricing based on the provided inputs.
  - The heatmap will be made based on a range of volatility and stock price values, to visualize how option prices change as stock price and volatility fluctuate.

- View historical records from the database with "View Previous Runs".
    - To retrieve previous calculations, click the "View Previous Runs" button.

## Dependencies:

- Python 3.x
- Numpy
- Scipy
- Tkinter (for the GUI)
- SQLite3 (for the database)


For a more in-depth look at the design, look at my [System Design Document](https://docs.google.com/document/d/1ZupAnSloM9hm8ZZ2mRDj3UfhuCembD_-dElhVstxKeo/edit?usp=sharing)
