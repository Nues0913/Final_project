import bs4
import aiohttp
import asyncio

async def studentnews():
	result = []
	href = []
	tem_result = []
	tem_href = []
	for page in range(5):
		url = "https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19,,,,,,,," + str(page)
		async with aiohttp.ClientSession(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0"}) as session:
			async with await session.get(url) as resp:
				assert resp.status == 200
				data = await resp.read()
				web = bs4.BeautifulSoup(data, "html.parser")
				root1 = web.find('ul', {'class': 'list list_type'})
				root2 = root1.find_all('a', href=True, title=True)
				#五個為一組進行分配，自動檢測不足跳出
				for i in root2:
					tem_result.append(i.text)
					tem_href.append(i['href'])
	for i in range(0, len(tem_result), 5):
		tem1 = []
		tem2 = []
		for j in range(5):
			try:
				tem1.append(tem_result[i + j])
				tem2.append(tem_href[i + j])
			except:
				pass
		result.append(tem1)
		href.append(tem2)
	return result, href

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop=loop)
	result, href = loop.run_until_complete(studentnews())
	for i in range(len(result)):
		for j in range(len(result[i])):
			print(result[i][j], href[i][j])