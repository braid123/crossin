def getWeekOfFirstDay(year):
    # 已知2017年1月1日是星期日
    i = 2017
    week=6
    days=0
    while i < year:
        if i % 400 == 0 or (i % 4 == 0 and i % 100 != 0):
            days += 366
        else:
            days += 365
        i += 1
    # 得到当年第一天的星期
    return (days+week) % 7


def getBlackFriday(year):
    # 遍历12个月
    if year < 2017:
        print('输入年份应大于或等于2017')
        return
    days = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]
    week = getWeekOfFirstDay(year)
    flag = 0
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        flag = 1
    day = 0
    for i in range(0, 12):
        # 判断每个月13号是否是黑色星期五
        if (day + 12 + week) % 7 == 4:
            if i != 11:
                print("%d-%d-13" % (year, i+1))
            elif i == 11:
                print("%d-12-13" % (year))
        day += days[flag][i]

search_year = int(input('查询年份：'))
print('符合日期:')
getBlackFriday(search_year)