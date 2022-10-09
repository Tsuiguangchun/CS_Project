# encoding:utf-8
# @CreateTime: 2022/6/15 18:19
# @Author: Xuguangchun
# @FlieName: get_data.py
# @SoftWare: PyCharm


import yaml, os, json

# 找到当前项目的根路径
# rootpath = os.path.abspath("..")
# yaml.load_all方法读取文件中的多个文档（---）时，返回的是一个迭代器对象，需要使用list转换为列表

currentPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(currentPath)[0]

print(currentPath)
print(rootPath)


class ReadAndWrite:

    def load_data(self, filePath):
        filePath = os.path.join(rootPath, filePath)
        if not os.path.exists(filePath):
            raise FileNotFoundError("请确保需要读取配置文件的是否存在")
        with open(filePath, 'r', encoding='utf-8') as f:
            data = list(yaml.load_all(f, Loader=yaml.FullLoader))
            if len(data) != 0:
                return data[0]
            # else:
            #     return None

            elif len(data) == 0:
                num = 0
                while num < 3:
                    num += 1
                    with open(filePath, 'r', encoding='utf-8') as f:
                        data = list(yaml.load_all(f, Loader=yaml.FullLoader))
                        if len(data) != 0:
                            return data[0]
                            break
            else:
                return None

    def write_data(self, filePath, needWriteData):
        filePath = os.path.join(rootPath, filePath)
        with open(filePath, 'a', encoding='utf-8') as f:
            writeData = yaml.dump(needWriteData, f, allow_unicode=True)
            f.close()
            return writeData

    def clear_data(self, filePath, headline=False, needWriteData=None):         # headline防止数据被清空后驱动数据初始化越界报错,写入占位空数据结构
        filePath = os.path.join(rootPath, filePath)
        if not os.path.exists(filePath):
            raise FileNotFoundError("请确保需要读取配置文件的是否存在")
        with open(filePath, 'w', encoding='utf-8') as f:
            if not headline:
                f.truncate()
            if headline:
                f.truncate()
                self.write_data(filePath, needWriteData=needWriteData)


#
if __name__ == '__main__':
    justDo = ReadAndWrite()

    #     token = {
    #         'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuY29pbnNreS5haSIsImF1ZCI6IjUzOGEwNGQ0LThmZWItMzE1Yi1iOWZkLTQzOTg1ZmY4MDhiYyIsImlhdCI6MTY1OTcyMDMzMywibmJmIjoxNjU5NzIwMzM1LCJleHAiOjE2NTk3NjM1MzMsImRhdGEiOnsidXVpZCI6IjUzOGEwNGQ0LThmZWItMzE1Yi1iOWZkLTQzOTg1ZmY4MDhiYyIsImFwcF9rZXkiOiI2NGIzYzgxMDQ4NGExMWVjOTEwYzQwYjA3NjYyN2E0MCIsImNsaWVudCI6IkFuZHJvaWQiLCJsYW5nIjoiRU4iLCJpcCI6IjYzLjIyMi4xOC4xNTAifX0.FfIksC7zs6GtnauMsNpsQ5b3yu0Z2_EDf3ifjLxfCFA',
    #         'expire_in': 43200}
    #     data = justDo.load_data(filePath=r'data\responseTime_Over3s.yaml')
    #     new_data = list(set(data[0]))
    # #     print(new_data)
    data = justDo.load_data(filePath=r'data\coinsPrice_chart_duration.yaml')
    # data = justDo.clear_data(filePath=r'data\gasReport.yaml',headline=True)
    print(json.dumps(data, indent=4))
    # print(data)
