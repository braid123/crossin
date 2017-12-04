# -*- coding: utf-8 -*-
def ExtractionData(filename):
    report = []
    with open(filename,'r', encoding='utf-8') as f:
        for line in f:
            tmp = line.split()
            report.append([tmp[0]] + [int(i) for i in tmp[1:]])
    return report


# 计算一个人的总分和平均分并排序
def CaculateScore(report):
    for i in range(len(report)):
        report[i].append(sum(report[i][1:]))
    num = len(report[0])
    for line in report:
        tmp = 0
        for i in range(1, num - 1):
            tmp = tmp + line[i]
        line.append(round(tmp / (num - 2), 1))
    return sorted(report, key=lambda x: x[10], reverse=True)


# 计算各科目平均分
def AverageOfEvery(report):
    average = [0 for i in range(len(report[0]))]

    for score in report:
        for i in range(1, len(score)):
            average[i] += score[i]
    tmp = [int(i / len(report)) for i in average[0:-1]]
    tmp.append(round(average[-1] / len(report), 1))
    tmp.pop(0)
    return tmp


# 替换不及格分数

def ReplaceNum(report):
    for line in report:
        for i in range(1, len(line) - 2):
            if line[i] < 60:
                line[i] = '不及格'
    return report


# 打印分数
def PrintScore(report, average):
    sum = 1
    first = ['  名次', '  姓名', '语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '总分', '平均分']
    with open('result.txt', 'w', encoding='utf-8') as f:
        for i in first:
            f.write('%s\t' % str(i))
        f.write('\n')
        average.insert(0, '平均')
        average.insert(0, 0)
        for i in average:
            f.write('%4s\t' % str(i))
        f.write('\n')

        for line in report:
            f.write('%4s\t' % sum)
            for i in line:
                f.write('%4s\t' % str(i))
            sum += 1
            f.write('\n')


if __name__ == "__main__":
    result = ExtractionData('report.txt')
    report_tmp = CaculateScore(result)
    average = AverageOfEvery(report_tmp)
    report = ReplaceNum(report_tmp)
    PrintScore(report, average)
