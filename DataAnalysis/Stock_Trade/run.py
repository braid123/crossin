from datetime import timedelta

import configuration
import data_process
import update_strategy
import visualization

# 载入启动条件，如果需要修改这一部分的参数，请直接在 [configuration.py] 文件中进行
# 载入项包括：起始资金 / 起始日期 / 终止日期 / 股票名称 / 数据文件名称
initial_investment = configuration.initial_investment
start_date = configuration.start_date
end_date = configuration.end_date
stocks = configuration.stocks
file_name = configuration.file_name

# 资金初始情况，全部为现金，无持有股票
currency = initial_investment
held_stocks = {}

for stock in stocks:
    held_stocks[stock] = 0


# 读取并清洗原始股票数据，具体过程可以在 [data_process.py] 文件中添加/修改函数
# 清洗过程封装，保证此处返回的是含有所有股票数据和日期索引的DataFrame即可
# 如果需要使用[Tushare]等第三方接口，可以将这部分自行改写
current_all_stock_data = data_process.read_and_resample_data(file_name, configuration.frequency)


# 从大表中抽取需要进行模拟的股票的数据
configuration.stock_data = current_all_stock_data[stocks]
# 全局日期变量设定
configuration.current_date = start_date
# 交易策略设定，可以在 [update_strategy.py] 中添加/修改自定义交易策略
strategy = update_strategy.alpaca_strategy

# 绘图所用数据，以list存储
currency_record = []
assets_record = []

# 模拟交易过程
while configuration.current_date <= end_date:
    # 使用交易策略进行当天的交易
    today_record = strategy(currency, held_stocks)
    # 当天无交易的情况
    if today_record is None:
        # 首日无交易
        if configuration.current_date == configuration.start_date:
            configuration.current_date = configuration.current_date + timedelta(1)
            continue
        # 交易日且无交易
        elif configuration.current_date in configuration.stock_data.index:
            # 记录现金与资产数据
            if len(currency_record) == 0:
                currency_record.append(configuration.initial_investment)
                assets_record.append(configuration.initial_investment)
            else:
                currency_record.append(currency_record[-1])
                assets_record.append(assets_record[-1])
            configuration.current_date = configuration.current_date + timedelta(1)
            continue
        else:
            configuration.current_date = configuration.current_date + timedelta(1)
            continue
    currency = today_record[0]
    total_assets = today_record[1]
    # 记录现金与资产数据
    currency_record.append(currency)
    assets_record.append(total_assets)
    # 输出当前资产统计，如果有其他输出需求，可以在 [visualization.py] 中添加/修改
    visualization.display_assets(currency, held_stocks, total_assets)
    configuration.current_date = configuration.current_date + timedelta(1)


# 绘制现金与资产变化情况
visualization.display_change_of_currency_and_assets(currency_record, assets_record, configuration.frequency)
# 绘制股票买入卖出情况
for stock in held_stocks:
    visualization.display_stock_trade(stock, configuration.frequency)


print("Done.")
