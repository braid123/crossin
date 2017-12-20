# 练习题
# 利用TuShare的接口，获取股票列表基本信息。
# 得到当日排行前10的股票的信息后，为其增加一列数据 —— 这些股票连续上涨的天数。
# 该列数据用riseDays表示，如果处于下跌中则记为0。
# 最后将所得数据写入一个csv文件。

import tushare as ts

# 获取股票大盘列表信息
total_stock_information = ts.get_stock_basics()
# pandas的DataFrame类型数据
print(total_stock_information)
# 截取排行前10的股票信息
stocks = total_stock_information.head(10)
# 为所有股票增加名为riseDays的列，默认设置为0
stocks['riseDays'] = 0

# 循环获取股票代码，并找寻该股票的历史数据
for i in range(10):
	current_stock = stocks.iloc[i]
	code = current_stock.name
	history = ts.get_hist_data(code)
	# 如果该股票昨日处于下跌，则认为连续上涨天数为0
	if history.iloc[0]['price_change'] < 0:
		continue
	else:
		rising_day = 0
		for j in range(len(history.index)):
			# 股票上涨，则上涨天数+1并继续检查；股票下跌则终止检查
			if history.iloc[j]['price_change'] > 0:
				rising_day += 1
			else:
				break
		# 注意索引的写法，如果不正确的话可能会在副本上进行修改，甚至抛出KeyError
		stocks.loc[(code, 'riseDays')] = rising_day

# 对照一下连续上涨天数是否已经加入
print(stocks)
# 输出到csv文件，注意编码格式
stocks.to_csv('stocks_infos.csv', encoding='gbk')
