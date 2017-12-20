from datetime import datetime


# 起始资金设置
initial_investment = 100000

# 交易模拟起始日期，yyyy-mm-dd格式
start_date_string = "2006-01-01"
start_date = datetime.strptime(start_date_string, "%Y-%m-%d")

# 交易模拟终止日期，yyyy-mm-dd格式
end_date_string = "2006-12-31"
end_date = datetime.strptime(end_date_string, "%Y-%m-%d")

# 重采样频率设定
frequency = 'B'

# 股票数据文件，若未将数据文件放置于当前目录下，需要设置为完整路径
file_name = "stock_px.csv"

# 需要进行交易的股票名称，字符串类型，存储于列表
stocks = ["AA", "AAPL", "GE", "JNJ", "MSFT", "PEP", "IBM", "SPX", "XOM"]

####################################
# 分割线，以上为用户参数，根据需要自行设置 #
####################################

# 交易过程控制用全局变量（一般情况下不作改动）
current_date = start_date
stock_data = None
purchase_dates = {}
sell_dates = {}

# 羊驼策略所用初始化参数
number_of_change = 1
number_of_stocks = 3
period = 5
