# 练习题
# 利用TuShare的电影数据接口，获取电影月票房信息。
# 找到top3的电影，利用接口再次查询它们近7日的票房信息，并绘制成图片。

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
import datetime

# 默认是取上月月票房，传参传入本月
today = datetime.date.today()
today_display = str(today)
month = today_display[:7]
movie = ts.month_boxoffice(month)
# 取排行榜前3的电影
top_three = movie.head(3)

# 保存top3电影名称
movie_names = []
for i in range(3):
	movie_names.append(top_three.iloc[i]['MovieName'])
print(movie_names)

# 用于保存获取到的电影的票房信息
boxoffice_record = {}
for i in range(3):
	boxoffice_record[movie_names[i]] = []
print(boxoffice_record)

# 取每部电影最近7天的票房信息
date_record = []
for i in range(7):
	# 计算7天的日期
	current = str(today + datetime.timedelta(days=i) - datetime.timedelta(days=7))
	# 写入记录日期用的数据结构
	print(current)
	date_record.append(current)
	# 获取单日的电影票房信息
	single_day_boxoffice = ts.day_boxoffice(current)
	for j in range(len(single_day_boxoffice)):
		# 得到电影名称
		movie_name = single_day_boxoffice.iloc[j]['MovieName']
		boxoffice = single_day_boxoffice.iloc[j]['BoxOffice']
		# 当前电影为top3电影，则将其当日票房写入记录用的数据结构
		if movie_name in movie_names:
			boxoffice_record[movie_name].append(boxoffice)
	# 对当日结果的检查，如果top3中有电影在当日没有被查询到，则认为当日没有票房，记为0
	for j in range(len(movie_names)):
		movie_boxoffice = boxoffice_record[movie_names[j]]
		if movie_names[j] not in single_day_boxoffice['MovieName'].values:
			movie_boxoffice.append(0)

# 绘图
# 汇总日期与票房，方便后续绘图方便
days = np.arange(7)
boxoffices = np.array((boxoffice_record[movie_names[0]], boxoffice_record[movie_names[1]], 
	boxoffice_record[movie_names[2]]))
# 配置字体，否则无法显示中文
font = FontProperties(fname="./SimHei.ttc", size=14)
# 定制图片大小
fig = plt.figure(figsize=(10, 6))
# 将top3的票房曲线绘制出来，设置颜色，连线类型，线条宽度，标识
plt.plot(days, boxoffices[0], color='black', linestyle='-', linewidth=2.5, 
	label=movie_names[0])
plt.plot(days, boxoffices[1], color='blue', linestyle='-',  linewidth=2.5, 
	label=movie_names[1])
plt.plot(days, boxoffices[2], color='red', linestyle='-',  linewidth=2.5, 
	label=movie_names[2])
# 设定标识所在位置与字体
plt.legend(loc='upper right', prop=font)
# 设定图片标题
plt.title('%s票房top3电影近7日走势' % month, fontproperties=font)
# 设定x轴，y轴标题
plt.xlabel(u'日期', fontproperties=font)
plt.ylabel(u'单日票房', fontproperties=font)
# 将x轴的数字转换为日期
plt.xticks(days, date_record)
# 显示图片
plt.show()
