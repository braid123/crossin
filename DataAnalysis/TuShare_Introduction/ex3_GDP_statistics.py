# 练习题
# 利用TuShare接口，获取近5年的GDP信息，绘制柱状图。
# 再抓取这5年的单季度GDP，绘制折线图。

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import tushare as ts

# 获取年度gdp信息
gdp_years = ts.get_gdp_year().head(5)
# 绘制年度gdp图片所用数据存储
years = []
year_gdps = []
# 保存最近5年的GDP数据
for i in range(5):
	years.append(int(gdp_years.iloc[i]['year']))
	year_gdps.append(int(gdp_years.iloc[i]['gdp']))

# 查询季度GDP记录
gdp_quarters = ts.get_gdp_quarter().head(25)
quarters = []
quarter_gdps = []

# 保存最近5年的GDP的季度信息
for i in range(25):
	quarter_information = gdp_quarters.iloc[i]
	# 剔除掉超出这5年内的信息
	if int(quarter_information.quarter) > years[0]:
		continue
	elif int(quarter_information.quarter) < years[-1]:
		break
	quarters.append(quarter_information.quarter)
	quarter_gdps.append(quarter_information.gdp)

# 为后续绘图方便，整理数据
years.reverse()
year_gdps.reverse()
quarters.reverse()
quarter_gdps.reverse()

print(year_gdps)
print(quarter_gdps)

# 季度的GDP是累计的，到第四季度时记录就是全年的GDP，为了绘制单季度的曲线，对数据进行处理
quarter_copy = quarter_gdps.copy()
for i in range(len(quarter_gdps)):
	if i % 4 != 0:
		quarter_gdps[i] -= quarter_copy[i-1]

# 开始绘图
plt.figure(1)
font = FontProperties(fname="./SimHei.ttc", size=10)
# 图层分为2行1列，绘制第1张子图
plt.subplot(211)
# 绘制柱状图
plt.bar(years, year_gdps)
# 设定坐标，标题
plt.xticks(years)
plt.ylabel(u'年度GDP', fontproperties=font)
plt.title(u'近五年GDP比较', fontproperties=font)

# 绘制第2张子图
plt.subplot(212)
# 循环处理，绘制5年的4季度GDP曲线
for i in range(0, 20, 4):
	plt.plot(np.arange(1, 5), quarter_gdps[i:i+4], linestyle='dashed', marker='o', label=years[i//4])
plt.legend(loc='upper left')
# 设定坐标，标题
plt.xticks([i for i in range(1, 5)])
plt.xlabel(u'季度', fontproperties=font)
plt.ylabel(u'单季度GDP', fontproperties=font)
plt.title(u'近五年单季度GDP走势', fontproperties=font)
# 显示图片
plt.show()
