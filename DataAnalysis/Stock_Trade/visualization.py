import configuration
import matplotlib.pyplot as plt
import pandas as pd


def display_assets(currency, stocks, total_assets):
    """
    资产输出函数，用于显示日期和当前资产结构
    包括现金额以及所持有股票数量
    """
    current_date = configuration.current_date
    print("当日资产小结")
    print("日期:  %s" % current_date.strftime("%Y-%m-%d"))
    print("现金:  %d" % currency)
    print("股票: ")

    for stock in stocks.keys():
        print("\t", stock, ": ", stocks[stock])

    print("总计:  %d" % total_assets)
    print("=" * 50)
    print()


def show_trade_detail(stock, amount, action):
    """
    交易行为输出函数，用于显示交易细节
    """
    current_date = configuration.current_date
    stock_data = configuration.stock_data
    date_index = stock_data.index
    location = date_index.get_loc(current_date)
    if action == 'b':
        print("---购买记录")
        print("---日期: %s" % current_date.strftime("%Y-%m-%d"))
        print("---购买股票: %s" % stock)
        print("---数量: %d" % amount)
        print("---现金: -%.2f" % (amount * stock_data[stock].iloc[location]))
    elif action == 's':
        print("+++出售记录")
        print("+++日期: %s" % current_date.strftime("%Y-%m-%d"))
        print("+++售出股票: %s" % stock)
        print("+++数量: %d" % amount)
        print("+++现金: +%.2f" % (amount * stock_data[stock].iloc[location]))
    print("\n\n")


def display_change_of_currency_and_assets(currency, assets, frequency):
    """
    交易结果展示函数，用于输出整个交易过程中的现金与总资产变化曲线
    """
    dates = pd.date_range(configuration.start_date_string, configuration.end_date_string, freq=frequency)
    asset_data = pd.DataFrame({'Currency': currency, 'Assets': assets}, index=dates)
    asset_data.plot()
    plt.savefig('image/assets.png', format='png')
    plt.show()


def display_stock_trade(stock, frequency):
    """
    股票交易展示函数，标记买入与卖出行为
    """
    stock_price = configuration.stock_data[stock]

    purchase = None
    if configuration.purchase_dates.get(stock, 0) != 0:
        purchase = configuration.purchase_dates[stock]

    sell = None
    if configuration.sell_dates.get(stock, 0) != 0:
        sell = configuration.sell_dates[stock]

    dates = pd.date_range(configuration.start_date_string, configuration.end_date_string, freq=frequency)
    price_data = pd.DataFrame({stock: stock_price}, index=dates)
    price_data.plot()
    # 标记股票购买日期
    if purchase is not None:
        for date in purchase:
            plt.scatter(date, stock_price.loc[date], c="red", marker='^')
    # 标记股票售出日期
    if sell is not None:
        for date in sell:
            plt.scatter(date, stock_price.loc[date], c="blue", marker='v')
    plt.savefig('image/%s.png' % stock, format='png')
    plt.show()
