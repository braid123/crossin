# pandas入门项目1 —— nba球队数据的简单统计

from pandas import Series, DataFrame
import numpy as np
import pandas as pd

# DataFrame读取nba2016-2017赛季的球队数据统计
df = pd.read_csv('./nba16-17.csv')
# print(df)

# 检查是否有数据缺失
print(df.isnull())

# 将含有缺失数据的行删除
team_data = df.dropna()
# print(team_data)

# 输出当前DataFrame的index和columns，查看该表统计项
print(team_data.index)
print(team_data.columns)

# 将该DataFrame根据每一项统计单项从高到底进行排序，将单项第一的倒数第一的数据存储，并最终整理为一个字典
best_and_worst = {}

for data in team_data.columns[3:]:
    temp_data = team_data.sort_values(by=data, ascending=False)

    best_team_index = temp_data.index[0]
    worst_team_index = temp_data.index[-1]
    
    best_team = temp_data.loc[best_team_index, 'Team']
    best_score = temp_data.loc[best_team_index, data]
    worst_team = temp_data.loc[worst_team_index, 'Team']
    worst_score = temp_data.loc[worst_team_index, data]
    
    best_and_worst[data] = {'best_team': best_team, 'best_score': best_score, 
                           'worst_team': worst_team, 'worst_score': worst_score}

# 从记录了单项统计表现最好和表现最差的球队的dictionary中生成新的DataFrame
best_and_worst_statistics = pd.DataFrame(best_and_worst).T
print("\n\n")
print(best_and_worst_statistics)

# 得到联盟中单项第一次数最多和单项倒数第一最多的球队各自的名称
print("\n\n")
single_statistics_best = best_and_worst_statistics['best_team'].value_counts()
print("得到联盟中单项第一次数最多的球队是%s, 有%d项数据第一" % (single_statistics_best.index[0], single_statistics_best[0]))
single_statistics_worst = best_and_worst_statistics['worst_team'].value_counts()
print("得到联盟中单项倒数第一次数最多的球队是%s, 有%d项数据垫底" % (single_statistics_worst.index[0], single_statistics_worst[0]))

# 找出联盟中5只3分球出手数最多的球队，生成一个关于球队名称，3分球出手数，3分球命中数，3分球命中率的DataFrame
print("\n\n")
top5_of_3PA = team_data.sort_values(by='3PA', ascending=False).head(5)
# print(top5_of_3PA)
best_3PA = pd.DataFrame([top5_of_3PA['Team'], top5_of_3PA['3P'], top5_of_3PA['3PA'], top5_of_3PA['3P%']]).T
print("联盟中最爱投3分球的5只球队的3分球技术统计")
print(best_3PA)

# 找出联盟中5只3分球出手数最少的球队，生成一个关于球队名称，3分球出手数，3分球命中数，3分球命中率的DataFrame
print("\n\n")
last5_of_3PA = team_data.sort_values(by='3PA', ascending=False).tail(5)
# print(last5_of_3PA)
worst_3PA = pd.DataFrame([last5_of_3PA['Team'], last5_of_3PA['3P'], last5_of_3PA['3PA'], last5_of_3PA['3P%']]).T
print("联盟中最不爱投3分球的5只球队的3分球技术统计")
print(worst_3PA)

# 3分球高出手球队与低出手球队（各5支）在3分球总出手数上的差值
difference_on_3PA = best_3PA.sum()['3PA'] - worst_3PA.sum()['3PA']
# 3分球高出手球队与低出手球队（各5支）在3分球命中数上的差值
difference_on_3P = best_3PA.sum()['3P'] - worst_3PA.sum()['3P']
# 平均每支3分球高出手球队与每支3分球低出手球队在3分球得分上的差值
difference_on_points_due_to_3P = difference_on_3P / 5 * 3
# 3分球高出手球队与低出手球队（各5支）平均3分球命中率的差值
difference_on_3P_hit_rate = best_3PA['3P%'].mean() - worst_3PA['3P%'].mean()

# 3分球球队间差值统计数据汇总
print("\n\n")
print("联盟中最爱投3分球的5只球队比联盟中最不爱投3分球的5只球队")
print("单场多出手了%d记3分球, 多命中了%d记3分球" % (difference_on_3PA, difference_on_3P))
print("单场平均每支爱投3分球的球队在3分球上多得%.2f分" % difference_on_points_due_to_3P)
print("两种球队在3分球命中率上的差值是%.2f%%" % (difference_on_3P_hit_rate * 100))
