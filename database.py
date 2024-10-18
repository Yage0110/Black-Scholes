# database.py
import sqlite3

class OptionPricingDatabase:
    def __init__(self, db_name='option_pricing.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY,
                current_price REAL,
                strike_price REAL,
                volatility REAL,
                interest_rate REAL,
                time_to_maturity REAL,
                call_purchase_price REAL,
                put_purchase_price REAL,
                call_pnl REAL,
                put_pnl REAL
            )
        ''')
        self.conn.commit()

    def store_run(self, current_price, strike_price, volatility, interest_rate, time_to_maturity, call_purchase_price, put_purchase_price, call_pnl, put_pnl):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO runs (
                current_price, 
                strike_price, 
                volatility, 
                interest_rate, 
                time_to_maturity, 
                call_purchase_price, 
                put_purchase_price, 
                call_pnl, 
                put_pnl
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            current_price,
            strike_price,
            volatility,
            interest_rate,
            time_to_maturity,
            call_purchase_price,
            put_purchase_price,
            call_pnl,
            put_pnl
        ))
        self.conn.commit()

    def view_previous_runs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM runs')
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()
