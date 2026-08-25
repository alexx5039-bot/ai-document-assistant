
def best_time(prices: list):


    min_price = prices[0]
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        profit = price - min_price
        max_profit = max(max_profit, profit)
    return max_profit





if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print(best_time(prices))