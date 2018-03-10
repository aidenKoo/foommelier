# coding: utf-8

# In[13]:


# -*-coding: utf-8
import csv
import matplotlib.pyplot as plt
from math import sqrt
from matplotlib import font_manager, rc  # 한글이 나오게

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

# In[7]:


#########몇 줄 있는지 보게
f = open('return.csv', 'r', encoding='EUC-KR')
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
with open('return.csv') as fr:
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

# for p in dict_list:
#     print(p)
#     print(dict_list.get(p))
#     print('-----------------------------------')


# In[25]:

# 사용자 냉장고 데이터
d_list = {}
d_list.update({
    '돼지고기': 5.0, '코다리': 5.0, '바지락': 5.0, '고등어': 5.0, '간장': 2.5, '양파': 2.5, '마늘': 2.5, '후추': 2.5,
    '참기름': 2.5, '대파': 2.5, '고추장': 2.5, '김치': 2.5, '된장': 2.5, '두부': 2.5, '계란': 2.5})
dict_list['사용자'] = d_list


# for p in dict_list:
#    print(p)
#    print(dict_list.get(p))
#    print('-----------------------------------')


# In[14]:


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


# In[27]:


top_match(dict_list, '사용자')



# In[28]:

print('가장 잘 맞는 음식은? ')
print('사용자 : ', dict_list.get('사용자'))
print('----------------------------------------------------------')
print('두부두루치기 : ', dict_list.get('두부두루치기'))

