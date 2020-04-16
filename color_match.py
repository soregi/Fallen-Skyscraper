import os
import re
import csv


#### 사용법: Falen 폴더, 그 왜 있잖아 common, localisation, map있는 모드 최상위폴더 거기에 넣고 실행하면 됨.
#### 왜냐? 지금 open함수의 경로를 다 그걸 기준으로 잡아놧거든. 싫으면 직접 수정하셈.


#### definition.csv에서 백작령의 이름과 color를 가져옴
#### [백작령id, R, G, B, 이름, x]
temp_file = open('./map/definition.csv')
province_data = csv.reader(temp_file, delimiter=';')
province_data = list(province_data)
temp_file.close()


#### provinces.txt에서 백작령 코드를 비교해서 리스트에 추가함.
#### [백작령id, R, G, B, 이름, x, 백작령 코드]
match_title = re.compile('title ?= ?c_[a-zA-Z0-9_]+')   # 'title = '찾는 정규식
for (path, dir, files) in os.walk('./history/provinces'):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.txt':
            try:
                temp_file = open(path+'/'+filename+ext)
                data = temp_file.read()
                title_name = filename.split('-')[1].strip()
                title_code = match_title.findall(data)
                if len(title_code):
                    title_code = title_code[0].replace(' ', '').replace('title=', '')
                    for tuple in province_data:
                        if tuple[4] == title_name and len(tuple) == 6:
                            if tuple[0] == '265':        # 중복지명 처리
                                tuple.append('c_yeonsan')
                                break
                            elif tuple[0] == '374':
                                tuple.append('c_yeonsa')
                                break
                            elif tuple[0] == '57':
                                tuple.append('c_gwangju')
                                break
                            elif tuple[0] == '162':
                                tuple.append('c_k_gwangju')
                                break
                            elif tuple[0] == '284':
                                tuple.append('c_eunsan')
                                break
                            elif tuple[0] == '307':
                                tuple.append('c_unsan')
                                break
                            elif tuple[0] == '174':
                                tuple.append('c_jangphung')
                                break
                            elif tuple[0] == '342':
                                tuple.append('c_pungsan')
                                break
                            elif tuple[0] == '187':
                                tuple.append('c_ongjin')
                                break
                            elif tuple[0] == '241':
                                tuple.append('c_n_ongjin')
                                break
                            else:
                                tuple.append(title_code)
                                break
                temp_file.close()
            except:
                print(path+'/'+filename+ext+' 파일을 열 수 없거나 처리에 실패했습니다. 문의바람.')


#for tuple in province_data:    # 테스트용
#    if len(tuple) < 7:
#        print(tuple)
#    elif len(tuple) == 7:
#        print(tuple)
#    elif len(tuple) > 7:
#        print(tuple)


#### landed_titles.txt의 color를 찾아 바꿈.
match_code = re.compile('[^#]+[ \t](c_[a-zA-Z0-9_]+)')    # 백작령 코드 찾는 정규식 
match_color = re.compile('[^#]+[ \t]color ?= ?\{[^}]+\}')    # 백작령 칼라 찾는 정규식
for (path, dir, files) in os.walk('./common/landed_titles'):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt':
            try:
                temp_file = open(path+'/'+filename, 'r', encoding='UTF-8')
                data = temp_file.read().split('\n')
                temp_file.close()
                
                find_color = False
                title_code = None
                for i in range(len(data)):
                    if find_color:
                        for tuple in province_data:
                            if len(tuple) == 7 and tuple[6] == title_code:
                                data[i] = re.sub('color[ \t]?=[ \t]?\{[^}]+\}', 'color = { '+tuple[1]+' '+tuple[2]+' '+tuple[3]+' }', data[i])
                                find_color = False
                                break
                    else:
                        m = match_code.search(data[i])
                        if m != None:
                            title_code = m[1]
                            find_color = True
                temp_file = open(path+'/'+filename, 'w', encoding='UTF-8')
                temp_file.write('\n'.join(data))
                temp_file.close()
            except:
                print(path+'/'+filename+' 파일을 열 수 없거나 처리에 실패했습니다. 문의바람.')
