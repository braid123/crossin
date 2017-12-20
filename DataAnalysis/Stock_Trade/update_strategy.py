from datetime import timedelta
import configuration
import visualization


##############################################
#            strategy functions              #
##############################################


def simple_test(currency, stocks):
    """
    测试用策略
    持有单只股票的情况
    股票连续上涨3天，以当前最大购买力买入
    股票连续下跌2天，将持有股票全部卖出
    """
    stock_data = configuration.stock_data
    current_date = configuration.current_date
    date_index = stock_data.index
    if current_date in date_index[:3]:
        return None
    elif current_date not in date_index:
        return None
    else:
        location = date_index.get_loc(current_date)
        total_assets = 0
        for stock in stocks.keys():
            current_stock = stock_data[stock]
            # 连续上涨3天
            if (currency >= current_stock.iloc[location] and
                    (current_stock.iloc[location] > current_stock.iloc[location - 1] >
                        current_stock.iloc[location - 2] > current_stock.iloc[location - 3])):
                amount = int(currency / current_stock.iloc[location])
                currency += purchase(stock, amount, currency, stocks)
            # 连续下跌2天
            elif (current_stock.iloc[location] < current_stock.iloc[location - 1] <
                    current_stock.iloc[location - 2]):
                amount = stocks[stock]
                currency += sell(stock, amount, stocks)
            # 计算总资产（股票部分）
            total_assets += stocks[stock] * current_stock.iloc[location]
        # 计算总资产（现金部分）
        total_assets += currency
        return currency, total_assets


def multiple_stocks_test(currency, stocks):
    """
    测试用策略
    持有多只股票的情况
    股票连续上涨2天，以当前最大购买力的10%进行买入
    股票连续下跌2天，将所持该股票全部卖出
    """
    stock_data = configuration.stock_data
    current_date = configuration.current_date
    date_index = stock_data.index
    if current_date in date_index[:2]:
        return None
    elif current_date not in date_index:
        return None
    else:
        location = date_index.get_loc(current_date)
        total_assets = 0
        for stock in stocks.keys():
            current_stock = stock_data[stock]
            # 连续上涨2天
            if (currency >= current_stock.iloc[location] and
                    (current_stock.iloc[location] > current_stock.iloc[location - 1] >
                        current_stock.iloc[location - 2])):
                amount = int(currency * 0.1 / current_stock.iloc[location])
                currency += purchase(stock, amount, currency * 0.1, stocks)
            # 连续下跌2天
            elif (current_stock.iloc[location] < current_stock.iloc[location - 1] <
                    current_stock.iloc[location - 2]):
                amount = stocks[stock]
                currency += sell(stock, amount, stocks)
            # 计算总资产（股票部分）
            total_assets += stocks[stock] * current_stock.iloc[location]
        # 计算总资产（现金部分）
        total_assets += currency
        return currency, total_assets


def alpaca_strategy(currency, stocks):
    """
    羊驼策略
    初始购入一定的股票数number_of_stocks
    每天固定的替换股票数number_of_change
    收益率计算所用天数period，收益率 = 现在的价格 / period天之前的价格
    将股票池内的股票按照收益率排序，买入收益率最高的number_of_stocks只股票
    之后的每天都将所有股票按收益率排序，并卖掉收益率最低的number_of_change只，
    再买入余下的股票中收益率最高的number_of_change只，以当前购买力的10%买入
    """
    number_of_stocks = configuration.number_of_stocks
    number_of_change = configuration.number_of_change
    period = configuration.period
    current_date = configuration.current_date
    stock_data = configuration.stock_data
    date_index = stock_data.index
    total_assets = 0
    # 非交易日
    if current_date not in date_index:
        return None
    # 策略所需判断时间不足
    if current_date in date_index[:period]:
        return None
    # 将所有股票的收益率按照从低到高排序
    stock_pool = sorted(list(stocks.keys()), key=yield_rate)
    # 如果还未持有股票，则将排名前number_of_stocks只股票分别按购买力最大的10%购入
    if not_holding_stocks(stocks):
        i = 0
        while i < number_of_stocks:
            temp_stock = stock_pool.pop()
            temp_stock_price = stock_data[temp_stock].loc[current_date]
            amount = int(0.1 * currency / temp_stock_price)
            i += 1
            # 若股价过高，无法购买时，购买下一只股票
            if amount == 0:
                i -= 1
                continue
            currency += purchase(temp_stock, amount, currency * 0.1, stocks)
            # 计算总资产（股票部分）
            total_assets += amount * temp_stock_price
        # 计算总资产（现金部分）
        total_assets += currency
        return currency, total_assets
    # 如果已经持有股票，则卖掉收益率最低的number_of_change只股票
    # 再买入余下的股票中收益率最高的number_of_change只股票
    else:
        # 将股票池分为已持有股票与未持有股票
        holding = []
        not_holding = []
        while len(stock_pool) > 0:
            stock = stock_pool.pop(0)
            if stocks[stock] != 0:
                holding.append(stock)
            else:
                not_holding.append(stock)
        # 若持有的股票中的收益最低者不低于未持有的股票中的收益最高者，不进行交易
        if yield_rate(holding[0]) >= yield_rate(not_holding[-1]):
            return None
        else:
            for i in range(number_of_change):
                temp_stock = holding[i]
                amount = stocks[temp_stock]
                currency += sell(temp_stock, amount, stocks)

            not_holding = sorted((not_holding + holding[:number_of_change]), key=yield_rate)

            i = 0
            while i < number_of_change:
                temp_stock = not_holding.pop()
                temp_stock_price = stock_data[temp_stock].loc[current_date]
                amount = int(0.1 * currency / temp_stock_price)
                i += 1
                # 若股价过高，无法购买时，购买下一只股票
                if amount == 0:
                    i -= 1
                    continue
                currency += purchase(temp_stock, amount, currency * 0.1, stocks)

            # 计算总资产（股票部分）
            for stock in stocks:
                stock_price = stock_data[stock].loc[current_date]
                amount = stocks[stock]
                total_assets += amount * stock_price
            # 计算总资产（现金部分）
            total_assets += currency
            return currency, total_assets


##############################################
#             help functions                 #
##############################################


def purchase(stock, amount, investment, stocks):
    """
    股票购买函数，会检查当前现金是否充足以及是否为交易日
    返回值是该笔交易中的现金额变化
    若所持现金不足，则按设定金额的最大购买力买入
    若非交易日，则直接返回
    """
    stock_data = configuration.stock_data
    current_date = configuration.current_date
    currency_change = 0
    # 非交易日
    if current_date not in stock_data.index:
        print("\t\t***************")
        print("\t\tNo market day")
        return currency_change
    # 购买数量为0
    if amount == 0:
        return currency_change
    price = stock_data[stock].loc[current_date]
    # 正常购买
    if investment >= amount * price:
        currency_change = -1 * amount * price
    # 资金不足
    else:
        print("\t\t***************")
        print("\t\t", end='')
        print(current_date)
        print("\t\tNo enough money")
        print("\t\t***************")
        amount = int(investment / price)
        currency_change = -amount * price
    stocks[stock] += amount
    # 显示当日交易明细
    visualization.show_trade_detail(stock, amount, "b")
    # 记录交易日期
    if configuration.purchase_dates.get(stock, 0) == 0:
        configuration.purchase_dates[stock] = [current_date]
    else:
        configuration.purchase_dates[stock].append(current_date)
    return currency_change


def sell(stock, amount, stocks):
    """
    股票卖出函数，会检查当前持有股票是否充足以及是否为交易日
    返回值是该笔交易中的现金额变化
    若所持股票不足，则将该支股票全部卖出
    若非交易日，则直接返回
    """
    stock_data = configuration.stock_data
    current_date = configuration.current_date
    currency_change = 0
    # 非交易日
    if current_date not in stock_data.index:
        print("\t\t***************")
        print("\t\tNo market day")
        return currency_change
    # 卖出数量为0
    if amount == 0:
        return currency_change
    price = stock_data[stock].loc[current_date]
    # 正常出售
    if amount <= stocks[stock]:
        stocks[stock] -= amount
        currency_change = amount * price
    # 持有股票数量不足
    else:
        print("***************")
        print(current_date)
        print("No enough stock")
        amount = stocks[stock]
        stocks[stock] = 0
        currency_change = amount * price
    # 显示当日交易明细
    visualization.show_trade_detail(stock, amount, "s")
    # 记录交易日期
    if configuration.sell_dates.get(stock, 0) == 0:
        configuration.sell_dates[stock] = [current_date]
    else:
        configuration.sell_dates[stock].append(current_date)
    return currency_change


def not_holding_stocks(stocks):
    """
    检查当前是否未购入股票
    """
    for stock in stocks:
        if stocks[stock] != 0:
            return False
    return True


def yield_rate(stock):
    """
    计算当前股票在period时间段内的收益率
    收益率 = 现在的价格 / period天之前的价格
    """
    current_date = configuration.current_date
    stock_data = configuration.stock_data[stock]
    date_index = stock_data.index
    current_price = stock_data[current_date]

    # 检查在period时间段之前的日期是否为交易日，如果不是的话就向前迭代
    former_date = current_date - timedelta(configuration.period)
    while former_date not in date_index:
        former_date = former_date - timedelta(1)

    former_price = stock_data[former_date]
    return current_price / former_price
