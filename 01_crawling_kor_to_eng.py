import os
import pandas as pd
import requests                        # HTTP 요청을 보내는 모듈
from bs4 import BeautifulSoup
from tqdm import tqdm                 # 진행률 프로세스 바
import time

def get_sub(word):
    url = f'https://en.dict.naver.com/#/search?query={word}'
    r = requests.get(url)                         # 서버에 요청을 보내는 것 200으로 응답하면 잘 처리 되었다는 의미
    html = r.text                                 #  r.text의 경우엔 HTTP Request를 보낸 URL에서 readable한 내용을 가져올 때 사용
    soup = BeautifulSoup(html, 'html.parser')     # 수프를 이용해서 원하는 태그를 선택할 수 있음

    try:
        sent = soup.select('p')[4].text           # 'p'의 구역에 해당하는 글을 텍스트로 가져온다.
    except:
        return None
    replace = replace_all(sent, replace_list)
    final = replace.split('[명사]')
    # final = replace.split('[명사]')[1].split('1.')[1].split('.')[0]
    return final

def get_verb(word, mode=None):
    url = f'https://en.dict.naver.com/#/search?query={word}'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        sent = soup.select('p.mean')[4].text
    except:
        return None
    replace = replace_all(sent, replace_list)
    final = replace.split('[형용사]')
    # 형용사가 존재하면 길이가 2 
    if not len(final) ==2:
        print(final)
        final = final[0].split('[동사]')
    # final = replace.split('[명사]')[1].split('1.')[1].split('.')[0]
    return final

def replace_all(text, remove_list):
    for i, j in remove_list:
        text = text.replace(i, j)
    return text
replace_list = [('\t',''), ('\r',''),('\t',''), ('\n','')]
# \t : 문자열 사이에 탭 간격을 줄 때 사용, \r : 캐리지 리턴(줄 바꿈 문자, 현재 커서를 가장 앞으로 이동), \n : 문자열 안에서 줄을 바꿀때 사용

# noun first
base_path = '/Volumes/♡혠니♥/Dev_lina/Project/Final_Project/Reference/final-project-level3-nlp-03-main/data/'
path_lists = ['NNG','NNP']
import os, sys
for path in path_lists:
    name = base_path+path + '.csv'
    nouns = pd.read_csv(name)

    data_dict = {'word':[], 'type':[],'v1':[]}
    for w_idx in tqdm(range(len(nouns[path]))):
        # print(nouns.NNG[w_idx])
        out = get_sub(nouns[path][w_idx])
        data_dict['word'].append(nouns[path][w_idx])
        data_dict['word'].append(path)
        if out is None:
            out = ['NA']
            print(w_idx, nouns[path][w_idx], out[0])
        try:
            data_dict['v1'].append(out[1])
        except:
            data_dict['v1'].append('Not noun')
    df = pd.DataFrame(data_dict)
    df.to_csv(f'./crawling_{path}.csv')

path_lists = ['VA', 'VV']
for path in path_lists:
    name = base_path+path + '.csv'
    
    verb = pd.read_csv(name).drop(columns=['Unnamed: 0'])
    data_dict = {'v1':[]}
    for w_idx in tqdm(range(len(verb[path]))):
        # print(nouns.NNG[w_idx])
        out = get_verb(verb[path][w_idx]) #한번에..
        data_dict['word'].append(verb[path][w_idx])
        data_dict['word'].append(path)

        if out is None:
            out = ['NA']
            print(w_idx, verb[path][w_idx], out[1])
        try:
            data_dict['v1'].append(out[1])
        except:
            print(verb[path][w_idx], out)
            data_dict['v1'].append('Not verb')
    df = pd.DataFrame(data_dict)
    name = path.split('/')[1]
    df.to_csv(f'./crawling_{path}.csv')

    


