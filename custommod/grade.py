import aiohttp
import asyncio
import pandas as pd
import json
from bs4 import BeautifulSoup

async def spider(account,password,mode):
	with open('custommod/dic.json', 'r', encoding='utf-8') as j:
		menu = json.load(j)
	modedic = {'所有考試排名':2,'所有科目成績':1,'出勤狀況統計':1,'出勤詳細日期':2}
	# 先找出登入畫面所要求的參數，我們需要對login.aspx進行解析
	login_url = 'https://svrsql.tnfsh.tn.edu.tw/SCORESTD/Login.aspx'
	# 先建表，這些是從login.aspx中payload獲取的，這些是我們登入時所需帶的資訊（submix.x and y使用預設值'0'即可）
	payload = {
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'__VIEWSTATE': '',
		'__VIEWSTATEGENERATOR': '',
		'__EVENTVALIDATION': '',
		'Login_UserId': account,
		'Login_Passwd': password,
		'Login_Submit.x': '0',
		'Login_Submit.y': '0'}
	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
	# 建立一個session，session有許多功用，諸如自動處理並共享cookie
	async with aiohttp.ClientSession(headers=headers) as session:	# 異步上下文管理器
		async with await session.get(login_url) as resp:
			# http不正常時直接拋出AssertionError
			assert resp.status == 200	
			# 使用異步aiohttp需要對resp做read()才能分析html
			html_login = await resp.read()
			# 使用BeautifulSoup分析html
			html_login = BeautifulSoup(html_login, "html.parser")
			# 登入所需參數的html標籤都是input，使用bs4的查找功能把它們抓出來塞進payload裡
			view_state = html_login.find('input', {'name': '__VIEWSTATE'})['value']
			view_state_generator = html_login.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
			event_validation = html_login.find('input',{'name': '__EVENTVALIDATION'})['value']
			payload['__VIEWSTATE'] = view_state
			payload['__VIEWSTATEGENERATOR'] = view_state_generator
			payload['__EVENTVALIDATION'] = event_validation
			# 關鍵來了，向login_url發送請求，並提交payload實現登入操作，我們登入後的數據會保存在session裡，之後就可以透過session訪問需要認證的網頁
			await session.post(login_url, data=payload, headers=headers)
			# 釋放記憶體
			del html_login
			# 配合前端所撰寫的條件式爬蟲
			if mode == '所有科目成績' or mode == '所有考試排名':
				response = await session.get(url='https://svrsql.tnfsh.tn.edu.tw/SCORESTD/' + menu['學期考查成績'])
				html = await response.read()
				html = BeautifulSoup(html, 'html.parser')
				table = html.find_all('table', {'width': "100%", 'border': "0", 'id': None})
				# table[1] df[3] 所有科目成績
				# table[2] df[2] 所有考試排名
				df = pd.read_html(table[modedic[mode]].prettify(), encoding="utf-8")
				return df
			
			elif mode == '出勤狀況統計' or mode == '出勤詳細日期':
				response = await session.get(url='https://svrsql.tnfsh.tn.edu.tw/SCORESTD/' + menu['學期出勤狀況'])
				html = await response.read()
				html = BeautifulSoup(html, 'html.parser')
				table = html.find_all('table', {'width': "100%", 'border': "0", 'id': None})
				# table[1] df[2] 出勤狀況統計
				# table[2] df[2] 出勤詳細日期
				df = pd.read_html(table[modedic[mode]].prettify(), encoding="utf-8")
				return df

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop=loop)
	ht = loop.run_until_complete(spider(*list(map(str,input().split()))))
	print(ht[2])
