# encoding:utf-8
# @CreateTime: 2022/8/10 22:33
# @Author: Xuguangchun
# @FlieName: get_pageNo.py
# @SoftWare: PyCharm


def get_pageNo(totalNum, pageSize):
    if totalNum % pageSize != 0:
        lengthNum = (totalNum // pageSize) + 1
    else:
        lengthNum = totalNum // pageSize
    pageList = []
    for page in range(0, lengthNum):
        page += 1
        pageNumber = {
            "page_size": pageSize,
            "page_no": page
        }
        pageList.append(pageNumber)
    return pageList
        # print(pageNumber)
