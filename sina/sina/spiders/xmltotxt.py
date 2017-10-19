# coding=utf-8
import os
import xml.dom.minidom
import glob


def findallxml(path):
    # 判断路径是否存在
    if os.path.exists(path):
        # 得到该文件夹路径下下的所有xml文件路径
        f = glob.glob(path + '\\*.xml')
        for file in f:
            print(file)
            # 打开xml文档
            dom = xml.dom.minidom.parse(file)
            # 得到文档元素对象
            sentences = dom.getElementsByTagName('sentence')
            pos_file = open("pos.txt", 'a', encoding="utf-8")
            neg_file = open("neg.txt", 'a', encoding="utf-8")
            for sentence in sentences:
                if sentence.hasAttribute("polarity"):
                    print("polarity: %s" % sentence.getAttribute("polarity"))
                    comments = sentence.childNodes[0].data
                    print("comments: %s" % comments)
                    if sentence.getAttribute("polarity") == "POS":
                        pos_file.write(comments + "\n")
                    elif sentence.getAttribute("polarity") == "NEG":
                        neg_file.write(comments + "\n")
            pos_file.close()
            neg_file.close()
    else:
        print("路径有误")


if __name__ == '__main__':
    path = r'C:\Users\lenovo\PycharmProjects\ScrapyProject\sina\sina\spiders\测试数据'
    findallxml(path)