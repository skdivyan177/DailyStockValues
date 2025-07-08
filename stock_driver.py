import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_top_5_most_active():
    url = "https://finance.yahoo.com/markets/stocks/most-active"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")[:5]
        most_active = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 7:
                continue
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            price = cols[2].text.strip()
            change = cols[3].text.strip()
            percent_change = cols[4].text.strip()
            volume = cols[5].text.strip()
            avg_volume = cols[6].text.strip()

            most_active.append({
                "Symbol": symbol,
                "Name": name,
                "Price": price,
                "Change": change,
                "% Change": percent_change,
                "Volume": volume,
                "Avg Volume": avg_volume
            })

        return most_active

    finally:
        driver.quit()


class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Top 5 Most Active Stocks")
        self.geometry("900x300")

        self.tree = ttk.Treeview(self, columns=("Symbol", "Name", "Price", "Change", "% Change", "Volume", "Avg Volume"), show='headings')

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        refresh_button = ttk.Button(self, text="Refresh Data", command=self.load_data)
        refresh_button.pack(pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        stocks = get_top_5_most_active()

        for stock in stocks:
            self.tree.insert("", tk.END, values=(
                stock['Symbol'],
                stock['Name'],
                stock['Price'],
                stock['Change'],
                stock['% Change'],
                stock['Volume'],
                stock['Avg Volume']
            ))


if __name__ == "__main__":
    app = StockApp()
    app.mainloop()
