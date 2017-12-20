# 一维随机行走过程 / 醉汉问题
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np

# python内置模块实现单次1000步随机漫步
import random

position = 0
walk_path = [position]
step_record = []
steps = 1000

for i in range(steps):
    current_step = random.choice([-1, 1])
    step_record.append(current_step)
    position += current_step
    walk_path.append(position)

# numpy实现5000次1000步随机漫步
walk_times = 5000
number_of_steps = 1000
each_step = np.random.randint(0, 2, size=(walk_times, number_of_steps))
each_step = np.where(each_step > 0, 1, -1)
walk_path = each_step.cumsum(1)

# 离出发点最远的距离
max_distance = np.abs(walk_path).max()
# 最远距离的平均值
average_max_distance = np.abs(walk_path).max(axis=1).mean()
# 最终位置距出发点的平均距离
destination_distance = np.abs(walk_path[:, -1]).mean()
# 第一次达到距原点10距离的平均时间
time_to_10 = (np.abs(walk_path >= 10)).argmax(axis=1).mean()
# 穿过出发点的平均次数
times_to_origin = np.where(walk_path == 0, 1, 0).sum(axis=1).mean()
# 改变方向的次数
change_count = []
for i in range(len(each_step)):
    single_count = 0
    for j in range(1, len(each_step[i])):
        if each_step[i][j] != each_step[i][j - 1]:
            single_count += 1
    change_count.append(single_count)
change_count = np.array(change_count)
change_count_average = change_count.mean()
# 到达距离出发点超过30的次数
hit_30 = (np.abs(walk_path) >= 30).any(1)
hit_30_count = hit_30.sum()

# 输出统计信息
print("醉汉走出的最远距离: ", max_distance)
print("醉汉走出的最远距离平均值: ", average_max_distance)
print("醉汉的最终位置平均距出发点距离: ", destination_distance)
print("醉汉第一次到达距离出发点为10处花费的时间单位平均值: ", time_to_10)
print("醉汉平均经过出发点的次数: ", times_to_origin)
print("醉汉平均改变方向的次数: ", change_count_average)
print("醉汉在%d次模拟中到达了距离出发点大于等于30处" % hit_30_count)


# 抽取单次模拟过程，绘制醉汉行走的位置曲线
plt.figure(1)
font = FontProperties(fname="./SimHei.ttc", size=10)
plt.plot(np.arange(1, 1001, dtype=int), walk_path[0], color='red', linestyle='-', label="walk_path")
plt.legend(loc='upper left', prop=font)
plt.xlabel(u'步数', fontproperties=font)
plt.ylabel(u'距离', fontproperties=font)

plt.show()
