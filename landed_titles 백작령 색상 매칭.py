import os
import re
import csv


#### 코드 설명
#### definition.csv를 열고 색상정보를 가져와서 province.txt를 읽고 백작령 코드 가져와서 landed titles에 자동으로 매칭시켜주는 코드임
#### 사용법: Fallen-Skyscraper 폴더, Readme 있는 모드 최상위폴더에 넣고 실행하면 됨. 지금 넣어놓은 위치.


#### definition.csv에서 백작령의 이름과 color를 가져옴
#### [백작령id, R, G, B, 이름, x]
temp_file = open('./Falen/map/definition.csv')
province_data = csv.reader(temp_file, delimiter=';')
province_data = list(province_data)
temp_file.close()


#### provinces.txt에서 백작령 코드를 비교해서 리스트에 추가함.
#### [백작령id, R, G, B, 이름, x, 백작령 코드]
match_title = re.compile('title ?= ?c_[a-zA-Z0-9_]+')		# 'title = c_~'찾는 정규식
for (path, dir, files) in os.walk('./Falen/history/provinces'):
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
							if tuple[0] == '265':		# 중복지명 예외처리
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


#### landed_titles.txt의 color를 찾아 바꿈.
match_title_code_or_color = re.compile('#|^[bcdke]_[a-zA-Z0-9_]+|[ \t][bcdke]_[a-zA-Z0-9_]+|^color[ \t]?=[ \t]?\{[^}]+\}|[ \t]color[ \t]?=[ \t]?\{[^}]+\}')	 # 칼라나 코드가 들어있는지 확인
match_title_code = re.compile('[bdke]_[a-zA-Z0-9_]+')		# 타이틀 코드 확인
match_count_code = re.compile('c_[a-zA-Z0-9_]+')		# 백작령 코드 찾는 정규식
match_color = re.compile('color ?= ?\{[^}]+\}')		# color 찾는 정규식
for (path, dir, files) in os.walk('./Falen/common/landed_titles'):
	for filename in files:
		ext = os.path.splitext(filename)[-1]
		if ext == '.txt':
			try:
				temp_file = open(path+'/'+filename, 'r', encoding='UTF-8')
				data = temp_file.read().split('\n')		# 입력받은 데이터를 라인별로 자름.
				temp_file.close()
				
				find_color = False
				title_code = None
				for i in range(len(data)):		# 데이터를 한라인 입력받음
					m = match_title_code_or_color.findall(data[i])		# 입력받은 데이터에 타이틀이나 칼라가 있는지 확인
					if m != None:		# 타이틀 코드가 들어있으면
						for token in m:		# 토큰단위로 입력받아서
							token = token.strip()		# 전처리
							
							if token == '#':		# 주석이면 무시하고
								break
							elif find_color == True and match_color.match(token) != None:		# 칼라 찾고있었고 토큰에 칼라가 들어있으면 칼라넣음
								for tuple in province_data:
									if len(tuple) == 7 and tuple[6] == title_code:
										data[i] = re.sub('color[ \t]?=[ \t]?\{[^}]+\}', 'color = { '+tuple[1]+' '+tuple[2]+' '+tuple[3]+' }', data[i])
										find_color = False
										tuple.append('1')		# 테스트용
										break
								find_color = False
							elif find_color == True and match_title_code.match(token) != None:		# 백작령이 아닌 타이틀 코드인데 칼라찾고 있었으면 이제 칼라 안찾음.
								print(title_code+'의 color를 찾을 수 없습니다.')
								find_color = False
							elif find_color == True and match_count_code.match(token) != None:		# 백작령 타이틀 코드인데 칼라찾고 있었으면 에러 내보내고 타이틀 코드 갱신.
								print(title_code+'의 color를 찾을 수 없습니다.')
								title_code = token
							elif find_color == False and match_count_code.match(token) != None:		# 백작령 타이틀 코드면 칼라 찾음
								title_code = token
								find_color = True
				
				if find_color == True:
					print(title_code+'의 color를 찾을 수 없습니다.')
					find_color = False
				
				temp_file = open(path+'/'+filename, 'w', encoding='UTF-8')
				temp_file.write('\n'.join(data))
				temp_file.close()
			except:
				print(path+'/'+filename+' 파일을 열 수 없거나 처리에 실패했습니다. 문의바람.')

n6 = 0
n7 = 0
n8 = 0
for tuple in province_data:
	if len(tuple) == 6:
		n6 += 1
		#print(tuple)
	if len(tuple) == 7:
		n7 += 1
		#print(tuple)
	if len(tuple) == 8:
		n8 += 1
		#print(tuple)
print(n6)
print(n7)
print(n8)
