# pandas入门项目2 —— 成绩统计
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

# 读取文本文件，载入学生姓名与成绩
name = np.loadtxt('name.txt', delimiter='\n', dtype=str)
score1 = np.loadtxt('score1.txt', delimiter='\n', dtype=int)
score2 = np.loadtxt('score2.txt', delimiter='\n', dtype=int)
score3 = np.loadtxt('score3.txt', delimiter='\n', dtype=int)

# 设定划分面元
bins = [0] + list(range(60, 101, 10))

# 将姓名与成绩封装成为3个Series对象
score_series1 = Series(score1, index=name)
score_series2 = Series(score2, index=name)
score_series3 = Series(score3, index=name)

# 统计单科最高分，最低分，平均分
print(score_series1.describe())
print(score_series2.describe())
print(score_series3.describe())

# 统计单科在各成绩区间上的人数
cuts1 = pd.cut(score_series1, bins, right=False)
print(pd.value_counts(cuts1))
cuts2 = pd.cut(score_series2, bins, right=False)
print(pd.value_counts(cuts2))
cuts3 = pd.cut(score_series3, bins, right=False)
print(pd.value_counts(cuts3))

# 连接各Series对象，拼接成为记录三科成绩的大表
total_score = pd.concat([score_series1, score_series2, score_series3], axis=1)
# print(total_score)
# 重命名列名
total_score.rename(columns={0: 'literature', 1: 'mathematics', 2: 'english'}, inplace=True)
# print(total_score)

# 自定义等第划分函数
def score_to_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# 根据三科成绩，为单个元素进行函数映射，输出对应的等第
total_score['literature_grade'] = total_score['literature'].map(score_to_grade)
total_score['mathematics_grade'] = total_score['mathematics'].map(score_to_grade)
total_score['english_grade'] = total_score['english'].map(score_to_grade)
# 计算单人总得分, 平均分
total_score['personal_total'] = total_score.sum(axis=1)
total_score['personal_average'] = total_score['personal_total'] / 3

# 指定列顺序，重新排列
total_score = total_score.reindex(columns=['literature', 'literature_grade', 'mathematics', 
    'mathematics_grade', 'english', 'english_grade', 'personal_total', 'personal_average'])

# 输出大表详细信息
print(total_score)
# 输出大表基本统计概述
print(total_score.describe())

# # 输出到csv文件
# total_score.to_csv('score.csv')

# 制作分级表
score_level_data = total_score.loc[:, 'literature':'english_grade']
# print(score_level_data)

# 设定分层索引
score_level_data.columns = [
    ['literature', 'literature', 'mathematics', 'mathematics', 'english', 'english'], 
    ['score', 'grade', 'score', 'grade', 'score', 'grade']
]
# print(score_level_data)

# 同上，添加单人总得分, 平均分
score_level_data['personal_total'] = score_level_data.sum(axis=1)
score_level_data['personal_average'] = score_level_data['personal_total'] / 3

# 对该表进行排序
score_level_data = score_level_data.sort_values(by='personal_total', ascending=False)

# 输出大表详细信息
print(score_level_data)
# 输出大表基本统计概述
print(score_level_data.describe())

# 输出到csv文件
score_level_data.to_csv('score_level_data.csv')
