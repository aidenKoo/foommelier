import csv
from random import randint, random
import random
import matplotlib.pyplot as plt
from math import sqrt
from matplotlib import font_manager, rc  # 한글이 나오게
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

from datetime import datetime

def loadUserData(mainData, username = '동섭'):

    user_list = {}
    with open('user_ref_data.csv') as fr:
        reader = csv.DictReader(fr)

        for row in reader:
            #         print(row)
            if row['사용자'] == username:
                if row['주재료'] != '':
                    user_list.update({row['주재료']: 5.0})
                if row['부재료'] != '':
                    user_list.update({row['부재료']: 2.5})

    # 사용자 냉장고 데이터
    d_list = {}
    d_list.update(user_list)
    mainData['사용자'] = d_list
    return mainData

def loadCsv(fileName = "ref_data.csv"):

    #########몇 줄 있는지 보게
    f = open(fileName, 'r', encoding='EUC-KR')
    rdr = csv.reader(f)
    c = 0
    play = '연근조림'
    name_list = []
    mm_list = []
    sm_list = []

    for line in rdr:
        if line[0] != play:
            play = line[0]
            c += 1
            name_list.append(play)
    # print(c) ##첫번쨰거는 음식이름이 들어갓으니 뺴기
    # name_list.pop(0)
    # print(len(name_list))
    # print(name_list[1])

    # In[24]:

    s = 0
    dict_list = {
        '연근조림': {
            '연근': 1,
            '간장': 1,
            '식초': 0.3,
            '양념': 0.3,
            '물엿': 0.3,
            '식용유': 0.3,
            '설탕': 0.3,
            '참기름': 0.3
        }}

    d_list = {}
    dd_list = []

    mi_list = []
    si_list = []
    # ???????????????????????????
    ch = '연근조림'
    with open('ref_data.csv') as fr:
        reader = csv.DictReader(fr)

        for row in reader:
            #         print(row)
            if row['음식이름'] == ch:
                if row['주재료'] != '':
                    d_list.update({row['주재료']: 5.0})
                if row['부재료'] != '':
                    d_list.update({row['부재료']: 2.5})

            if row['음식이름'] != ch:
                dict_list[ch] = d_list
                s += 1
                d_list = {}
                ch = name_list[s]
                if row['주재료'] != '':
                    d_list.update({row['주재료']: 5.0})
                if row['부재료'] != '':
                    d_list.update({row['부재료']: 2.5})

            if s == 800:
                break

    return dict_list

def sim_distance(data, name1, name2):
    sum = 0
    for i in data[name1]:
        if i in data[name2]:  # 같은 영화를 봤다면
            sum += pow(data[name1][i] - data[name2][i], 2)
        else:
            sum += pow(data[name1][i], 2)

    return 1 / (1 + sqrt(sum))


# In[26]:


def top_match(data, name, index=5, sim_function=sim_distance):
    li = []
    for i in data:
        if name != i:  # 자기 자신은 제외한다
            li.append((sim_function(data, name, i), i))  # 유사도, 이름을 튜플에 묶어 리스트에 추가한다
    li.sort()  # 오름차순 정렬
    li.reverse()  # 내림차순 정렬

    return li[:index]


def getUsersRequest(healthMaterialData,requestList): # 유저가 요구한 건강 지표 정보를 받아 가져온다.
    returnDic = {}
    tempList = []
    for rl in requestList:
        if(rl=="제철음식"):
            if(3<=datetime.now().month<=5):
                rl = "봄"
            elif(5<datetime.now().month<=8):
                rl = "여름"
            elif (8<datetime.now().month<12):
                rl = "가을"
            else:
                rl = "겨울"
        tempList.append(loadUserData(healthMaterialData,rl))
    for tl in tempList:
        for thisDictKey in tl:
            returnDic["사용자"] = tl[thisDictKey]

    return returnDic

def healthCoFilter(mainData, healthMaterialData, requestList,howManyDish = 30):
    returnDic = {}
    topList = []

    userReque = getUsersRequest(healthMaterialData,requestList)
    mainData['사용자'] = userReque['사용자']
    topList = top_match(mainData,"사용자",howManyDish)

    for tl in topList:
        returnDic[tl] = mainData[tl]

    return returnDic

def loadHealthMaterailData():
    returnDict = {}
    tempDict = {}
    fileNameList = ['건강 주재료.csv','생애주기 주재료.csv','제철음식 주재료.csv','질병 주재료.csv']
    for fn in fileNameList:
        tempDict = loadCsv(fn)
    for td in tempDict:
        returnDict[td] = tempDict

    return returnDict
# -----------------------------------------------mainmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

rl = ['감기','임신부']
print(healthCoFilter(loadCsv(), loadHealthMaterailData(),rl))
