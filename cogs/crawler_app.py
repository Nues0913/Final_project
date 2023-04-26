import discord
from discord import app_commands
from discord.ext import commands
from core.classes import Cog_Extension
import custommod.tnfsh as sp
import time, datetime


async def spider():
	sp_original_news, sp_original_href = await sp.studentnews()
	embed_news = []
	for x in range(len(sp_original_news)):
		embed1 = discord.Embed(title="臺南第一高級中學-學生公告",description='最新公告',color=0x00ff00,timestamp=datetime.datetime.now())
		embed1.set_thumbnail(url="https://i.imgur.com/nBjAjix.png")
		# embed1.set_image(url="https://i.imgur.com/rjeRPkT.png")
		i = 0
		for y in range(len(sp_original_news[x])):
			i += 1
			embed1.add_field(name="消息" + str(i), value=f'[{sp_original_news[x][y]}](https://www.tnfsh.tn.edu.tw/latestevent/{sp_original_href[x][y]})',inline=False)
		q = x + 1
		embed1.set_footer(text=str(q) + "/" + str(len(sp_original_news)),icon_url="https://cdn.discordapp.com/attachments/1045891061928701973/1090186662568529940/IMG_4204.gif")
		embed_news.append(embed1)
	return embed_news


class crawler(Cog_Extension):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.news_flag = False

	@commands.Cog.listener()
	async def on_ready(self):
		self.bot.add_view(news())
		self.news_flag = True
		print('crawler.py is working')
		start = time.time()
		self.embed_news = await spider()
		print(f'爬蟲執行完畢，執行時間：{time.time()-start}')
		global global_news
		global_news = self.embed_news

	@app_commands.command(name='news', description='台南一中學生訊息')
	async def news_func(self, interaction: discord.Interaction):
		if self.news_flag == False:
			await interaction.response.send_message('爬蟲中，請稍後!')
			start = time.time()
			self.embed_news = await spider()
			print(f'爬蟲執行完畢，執行時間：{time.time()-start}')
			global global_news
			global_news = self.embed_news
			await interaction.edit_original_response(content=None,embed=self.embed_news[0],view=news())
			self.news_flag = True
		elif self.news_flag == True:
			try:
				await interaction.response.send_message(content=None,embed=self.embed_news[0],view=news())
			except:
				await interaction.response.send_message('尚未啟用!')


class news(discord.ui.View):

	def __init__(self):
		super().__init__(timeout=None)
		self.flag = 0

	@discord.ui.button(label='⬅上一頁',custom_id="button-left",style=discord.ButtonStyle.success)
	async def left(self, interaction: discord.Interaction,button: discord.ui.Button):
		# Message = interaction.channel.last_message
		# await Message.delete()
		if self.flag > 0:
			self.flag -= 1
		await interaction.response.edit_message(embed=global_news[self.flag],view=self)

#await interaction.response.send_message('active',view=news())

	@discord.ui.button(label='下一頁➡',custom_id="button-right",style=discord.ButtonStyle.success)
	async def right(self, interaction: discord.Interaction,button: discord.ui.Button):
		# Message = interaction.channel.last_message
		# await Message.delete()
		if self.flag < len(global_news) - 1:
			self.flag += 1
		await interaction.response.edit_message(embed=global_news[self.flag],view=self)

	@discord.ui.button(label='🔄刷新',custom_id="button-refresh",disabled=False,style=discord.ButtonStyle.success)
	async def refresh(self, interaction: discord.Interaction,button: discord.ui.Button):
		global global_news
		await interaction.response.defer()
		button.disabled = True
		await interaction.message.edit(embed=global_news[self.flag], view=self)
		print('user refresh the news')
		start = time.time()
		global_news = await spider()
		print(f'爬蟲執行完畢，執行時間：{time.time()-start}')
		button.disabled = False
		await interaction.message.edit(embed=global_news[self.flag], view=self)


#test類別裡定義的button
class test(discord.ui.View):

	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(label='test')
	async def button_test(self, interaction: discord.Interaction,button: discord.ui.Button):

		await interaction.response.send_message('active')

	@discord.ui.button(label='test1')
	async def button_test1(self, interaction: discord.Interaction,button: discord.ui.Button):
		await interaction.response.send_message('not active')


async def setup(bot):
	await bot.add_cog(crawler(bot))
