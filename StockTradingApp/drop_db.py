import sqlite3,Config

connection = sqlite3.connect(Config.DB_PATH)
    
cursor = connection.cursor()
cursor.execute("""
    DROP TABLE stock_price
""")
cursor.execute("""
    DROP TABLE stock
""")
connection.commit()