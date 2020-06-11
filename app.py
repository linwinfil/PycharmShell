# 导入
import os
import sys

# pykson，类似Android的Gson
from pykson import JsonObject, IntegerField, StringField, ObjectListField
from pykson import Pykson

print("开始解析")
dataList = []
dataOrder = 126
picNum = 0


class Res(JsonObject):
    info = StringField()
    proportion = StringField()
    maxPicNum = IntegerField()
    minPicNum = IntegerField()

    def __init__(self):
        super(Res, self).__init__()
        self.info = ""
        self.proportion = "square"
        self.maxPicNum = 0
        self.minPicNum = 0

    def setInfo(self, new_info):
        self.info = new_info

    def setMaxPicNum(self, new_max):
        self.maxPicNum = new_max

    def setMinPicNum(self, new_max):
        self.minPicNum = new_max


class Data(JsonObject):
    file_tracking_id = StringField()
    relatid = StringField()
    name = StringField()
    subtype = StringField()
    restype = StringField()
    restype_id = IntegerField()
    sub_restype = StringField()
    sub_restype_id = IntegerField()
    order = IntegerField()
    tracking_code = StringField()
    tj_url = StringField()
    reddot_type = StringField()
    thumb_80 = StringField()
    thumb_120 = StringField()
    size = IntegerField()
    needFontId = StringField()
    needMusicId = StringField()
    measure = StringField()
    res_arr = ObjectListField(Res)

    def __init__(self):
        super(Data, self).__init__()
        self.file_tracking_id = ""
        self.relatid = ""
        self.name = ""
        self.subtype = "normal"
        self.restype = "基础拼图"
        self.restype_id = 11
        self.sub_restype = ""
        self.sub_restype_id = 0
        self.order = 0
        self.tracking_code = ""
        self.tj_url = ""
        self.reddot_type = ""
        self.thumb_80 = ""
        self.thumb_120 = ""
        self.size = 0
        self.needFontId = ""
        self.needMusicId = ""
        self.measure = ""
        self.res_arr = []

    def setId(self, new_id):
        self.file_tracking_id = new_id

    def setName(self, new_name):
        self.name = new_name

    def setThumb80(self, new_thumb):
        self.thumb_80 = new_thumb

    def setThumb120(self, new_thumb):
        self.thumb_120 = new_thumb

    def setOrder(self, new_order):
        self.order = new_order

    def setSize(self, new_size):
        self.size = new_size

    def setResArr(self, new_res_arr=None):
        if new_res_arr is None:
            new_res_arr = []
        self.res_arr = new_res_arr


def parse(picNum: int, ratioStr, subDirPath, list=[]):
    global dataOrder
    listdir = os.listdir(subDirPath)
    for subListDir in listdir:
        name = subListDir
        subListDirPath = os.path.join(subDirPath, subListDir)  # /布局 一张 jason/16：9/BasePuzzle80635
        previewId = subListDir.replace("BasePuzzle", "", 1)  # 将BasePuzzle80635替换成80635

        data = Data()
        data.setId(previewId)
        data.setThumb80("%s" % name + "thumb.png")
        data.setThumb120("%s" % name + "thumb.png")
        # 基础拼图-202006-10-a-1:1_1张
        data.setName("基础拼图-202006-10-a-" + '%s' % ratioStr + '_' + "1张")
        dataOrder = dataOrder + 1
        data.setOrder(dataOrder)

        res = Res()
        res.setMaxPicNum(picNum)
        res.setMinPicNum(picNum)
        res.setInfo("%s" % name + ".json")  # BasePuzzle80635.json
        data.setResArr([res])

        list.append(data)
    pass


# 文件路径
root = "/Users/linmaoxin/Projects/PythonProjects/ParseDemo/layout"
dirPaths = os.listdir(root)
dirPaths.sort()

for dirPath in dirPaths:
    # /布局 一张 jason
    subPath = os.path.join(root, dirPath)
    if subPath.__contains__(".json"):
        continue
    if not os.path.exists(subPath):
        raise FileExistsError(subPath + " no exist")

    picNum = picNum + 1
    subDirPaths = os.listdir(subPath)
    subDirPaths.sort()
    for subDirPath in subDirPaths:
        ratioStr = ""
        if subDirPath.__contains__("full"):
            ratioStr = "full"
        else:
            split = subDirPath.split("：")
            ratioStr = split[0] + "比" + split[1]

        # /布局 一张 jason/16：9
        subDir = os.path.join(subPath, subDirPath)
        if not os.path.exists(subDir):
            raise FileExistsError(subDir + " no exist")
        print(subDir)
        parse(picNum, ratioStr, subDir, dataList)

# print(dataList)
json = Pykson().to_json(dataList)
print(json)

# 写json到文件夹
filePath = root + "/layout2.json"
if os.path.exists(filePath):
    os.remove(filePath)
with open(filePath, 'w') as fos:
    fos.write(json)

