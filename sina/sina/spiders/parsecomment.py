import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from nlptencentparse import SelectDataFromMysql


def snowanalysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)
        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("test")
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    plt.show()


if __name__ == '__main__':
    textlist = SelectDataFromMysql()
    snowanalysis(textlist)
