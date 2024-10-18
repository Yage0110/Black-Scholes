from numpy import exp, sqrt, log
from scipy.stats import norm

class BlackScholes:
    def __init__(self, maturity: float, strike: float, curr_price: float, volatility: float, rate_of_interest: float):
        self.maturity = maturity
        self.strike = strike
        self.curr_price = curr_price
        self.volatility = volatility
        self.rate_of_interest = rate_of_interest

    def calculate_prices(self):
        a1 = (log(self.curr_price/self.strike) + (self.rate_of_interest + 0.5 * self.volatility ** 2) * self.maturity) / (self.volatility * sqrt(self.maturity))
        a2 = a1 - self.volatility * sqrt(self.maturity)

        call_price = self.curr_price * norm.cdf(a1) - (self.strike * exp(-self.rate_of_interest * self.maturity) * norm.cdf(a2))
        put_price = (self.strike * exp(-self.rate_of_interest * self.maturity) * norm.cdf(-a2) - self.curr_price * norm.cdf(-a1))

        call_gamma = norm.pdf(a1) / (self.curr_price * self.volatility * sqrt(self.maturity))
        put_gamma = call_gamma

        call_delta = norm.cdf(a1)
        put_delta = norm.cdf(a1) - 1

        return {
            'call_price': call_price,
            'put_price': put_price,
            'call_gamma': call_gamma,
            'put_gamma': put_gamma,
            'call_delta': call_delta,
            'put_delta': put_delta
        }
    def calculate_pnl(self, call_purchase_price: float, put_purchase_price: float):
        prices = self.calculate_prices()
        call_pnl = prices['call_price'] - call_purchase_price
        put_pnl = prices['put_price'] - put_purchase_price
        return {
            'call_pnl': call_pnl,
            'put_pnl': put_pnl
        }