import pandas as pd
from numpy import sqrt


def loadAsCsv(fileName='dft.csv'):
    tempDf = pd.read_csv(fileName, encoding='EUC-KR')
    alist = []

    for i in tempDf.index:
        tempDic = {}
        for col in tempDf:
            tempDic[col] = tempDf.at[i, col]
        alist.append(tempDic)
    return alist

def linkNutrient(filteredList,nutData = loadAsCsv("calories.csv")):
    returnLink = []
    for fl in filteredList:
        try:
            for nd in nutData:
                if(fl==nd["음식이름"]):
                    returnLink.append(nd)
        except:
            print('에러',fl)
            continue
    return returnLink


def transList(givenList):
    returnDic = {}
    tempList = []
    for gl in givenList:
        tempList.append(gl['음식이름'])
    tempList = list(set(tempList))
    tempDic = {}
    for tl in tempList:
        for gl in givenList:
            if (tl == gl['음식이름']):
                tempDic[gl['영양성분']] = gl['함유량']
        returnDic[tl] = tempDic
        tempDic = {}


    return returnDic

def sim_pearson(data, name1, name2):
    sumX = 0  # X의 합
    sumY = 0  # Y의 합
    sumPowX = 0  # X 제곱의 합
    sumPowY = 0  # Y 제곱의 합
    sumXY = 0  # X*Y의 합
    count = 0  # 음식 개수

    for i in data[name1]:  # i = key
        if i in data[name2]:  # 같은 음식을 평가했을때만
            sumX += data[name1][i]
            sumY += data[name2][i]
            sumPowX += pow(data[name1][i], 2)
            sumPowY += pow(data[name2][i], 2)
            sumXY += data[name1][i] * data[name2][i]
            count += 1

    return (sumXY - ((sumX * sumY) / count)) / sqrt(
        (sumPowX - (pow(sumX, 2) / count)) * (sumPowY - (pow(sumY, 2) / count)))

# 딕셔너리 돌면서 상관계수순으로 정렬
def top_match(data, name, index=20, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.reverse() #내림차순
    return li[:index]
def UserloadOnData(data,userDic):
    userDic['당질'] = userDic["탄수화물"]
    data['사용자'] = userDic


import health

def main(data={},healthDict={}):
# {'bmi': 23.120623596247853, 'bmi상태': '정상', '칼로리': 2600, '단백질': 65,
#  '단백질:': 65, '나트륨': 2000, '칼륨': 3500, '칼슘': 800,
# '기초대사량': 1716.45, '활동대사량': 643.66875, '권장칼로리': 2360.11875}

    list = [174,70,27,1,2,3] #테스트 덤프
    healthDict = healthMain(list[0],list[1],list[2],list[3],list[4])
    data = [(0.03809703432192489, '겨울 샤브샤브'), (0.03739845102413832, '계란말이김밥'), (0.037229803192769, '두부두루치기'), (0.03706344527230439, '수제비'), (0.03706344527230439, '쇠고기 떡국'), (0.03706344527230439, '무초절임 쌈밥'), (0.03706344527230439, '두부 스테이크'), (0.036899325648329845, '해물 하이라이스'), (0.036899325648329845, '콩나물잡채'), (0.036899325648329845, '양배추 두부찜'), (0.036899325648329845, '무 굴국'), (0.036899325648329845, '깐쇼새우'), (0.036737394325205806, '탕국'), (0.036737394325205806, '두부전골'), (0.036737394325205806, '두부구이와 김양념장'), (0.036737394325205806, '굴국밥'), (0.036577602861251314, '해물칼국수'), (0.036577602861251314, '버섯전골'), (0.036577602861251314, '묵밥'), (0.036577602861251314, '멸치국수'), (0.036577602861251314, '매운탕'), (0.036577602861251314, '돌나물물김치'), (0.036577602861251314, '계란말이'), (0.03641990430707569, '큐브참치 주먹밥'), (0.03641990430707569, '케이준샐러드'), (0.03641990430707569, '케이준 치킨샐러드'), (0.03641990430707569, '카레라이스'), (0.03641990430707569, '참치 야채볶음'), (0.03641990430707569, '우럭매운탕'), (0.03641990430707569, '우럭 매운탕')]

    dishNameList = []
    for d in data:
        dishNameList.append(d)
    linkedList = linkNutrient(dishNameList)
    transedDic = transList(linkedList)
    transedDic['사용자'] = healthDict

    topList = top_match(transedDic,'사용자',20)
    print(topList)
    return topList
