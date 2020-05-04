#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import json

con = pymysql.connect(host='localhost', user='g4eng', password='1234', db='planb')
value, name, state, origin, changed, category, classify = [], '', 0, 0, 0, 0, 0
try:
	with open('./modify1.json') as json_file:
		json_data = json.load(json_file)

		license = json_data['시험']
		license_list = list(license[0].keys())

		for i in license:
			for j in license_list:
				i_j = i[j]
				for k in range(len(i_j)):
					arr = list(i_j[k].keys())
					for l in arr:
						v = i_j[k][l]
						for m in v[0]:
							res = v[0][m]
							res = res.split(',')
							if res[0] != 'x':
								if res[0] == '진행':
									tmp = ((l+' ('+m+')', res[0], res[1], 0, 0, 0))
								elif res[0] == '연기':
									tmp = ((l+' ('+m+')', res[0], 0, res[1], 0, 0))
								value.append(tmp)

		toeic = json_data['토익']
		for i in toeic[0]:
			tmp = toeic[0][i]
			tmp = tmp.split(',')
			value.append(('토익 ' +  i, tmp[0], tmp[1], 0, 1, 0))

		teps = json_data['텝스']
		for i in teps[0]:
			tmp = teps[0][i]
			tmp = tmp.split(',')
			value.append(('텝스 ' +  i, tmp[0], tmp[1], 0, 2, 0))

		edu = json_data['학사일정']
		edu_list = list(edu[0].keys())
		for i in edu_list:
			leng = edu[0][i]
			if len(leng) == 1:
				for j in leng[0]:
					res = leng[0][j]
					res = res.split(',')
					if len(res) == 2:
						value.append((j, res[0], res[1], 0, 3, 0))
					else:
						value.append((j, res[0], res[1], res[2], 3, 0))
					
		sight = json_data['관광지']
		for i in sight:
			for j in i:
				l = i[j][0]
				if len(l) != 1:
					for n in range(len(l)):
						tmp = l.popitem()
						t = tmp[1].split(',')
						if len(t) == 1:
							value.append((tmp[0], t[0], 0, 0, 4, j))
						elif len(t) == 2:
							if t[1] == '미정':
								value.append((tmp[0], t[0], 0, 0, 4, j))
							else:	
								value.append((tmp[0], t[0], 0, t[1], 4, j))
						elif len(t) == 3:
							value.append((tmp[0], t[0], t[1], t[2], 4, j))
		
		festa = json_data['축제공연행사']
		for i in festa:
			for j in i:
				l = i[j][0]
				if len(l) != 1:
					for n in range(len(l)):
						tmp = l.popitem()
						t = tmp[1].split(',')
						if len(t) == 1:
							value.append((tmp[0], t[0], 0, 0, 5, j))
						elif len(t) == 2:
							if t[0] == '진행':
								value.append((tmp[0], t[0], t[1], 0, 5, j))
							else:
								if t[1] == '미정':
									value.append((tmp[0], t[0], 0, 0, 5, j))
								else:
									value.append((tmp[0], t[0], 0, 1, 5, j))
						else:
							value.append((tmp[0], t[0], t[1], t[2], 5, j))
				else:
					tmp = l.popitem()
					t = tmp[1].split(',')
					value.append((tmp[0], t[0], 0, t[1], 5, j))	

		concert = json_data['콘서트']
		for i in concert[0]:
			tmp = concert[0][i].split(',')
			value.append((i, tmp[0], tmp[1], 0, 6, 0))

	with con.cursor() as cur:
		for i in value:
			#print(i)
			name = i[0]
			state = i[1]
			if state == '취소':
				state = 0
			elif state == '진행':
				state = 1
			else:
				state = 2
			origin = i[2]
			changed = i[3]
			category = i[4]
			classify = i[5]
			query = 'insert into plan (Name, State, Origin, Changed, Category, Classifiy) values (%s, %s, %s, %s, %s, %s)'
			cur.execute(query, (name, state, origin, changed, category, classify))
			con.commit()
		query = 'select * from plan'
		cur.execute(query)
		res = cur.fetchall()

		for i in res:
			print(i)
			#pass

finally:
	con.close()