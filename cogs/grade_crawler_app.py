import discord
from discord import app_commands
from discord.ext import commands
from core.classes import Cog_Extension
from tabulate import tabulate
import asyncio, time, pandas
import wcwidth # 解決tabulate中文對齊問題

import custommod.grade as gd

class view(discord.ui.View):
	def __init__(self, account, password, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.account = account
		self.password = password
	@discord.ui.select(placeholder='選擇一項類別',options=[discord.SelectOption(label='所有科目成績',description='所有科目成績'),discord.SelectOption(label='所有考試排名', description='所有考試排名'),discord.SelectOption(label='出勤狀況統計',description='出勤狀況統計'),discord.SelectOption(label='出勤詳細日期',description='出勤詳細日期')])
	async def callback(self, interaction: discord.Interaction,select: discord.ui.Select):
		await interaction.response.defer(ephemeral=True)
		select.disabled = True
		await interaction.edit_original_response(view=self)
		if select.values[0] == '所有考試排名':
			try:
				start = time.time()
				dataframe = await gd.spider(self.account, self.password, '所有考試排名')
				dataframe = dataframe[2]
				print(f'成績查詢完畢 花費{time.time()-start}秒')
				account = self.account
				password = self.password
				class exam2_view(discord.ui.View):
					def __init__(self, dataframe, *args, **kwargs):
						super().__init__(*args, **kwargs)
						self.dataframe = dataframe
						self.account = account
						self.password = password
					@discord.ui.select(placeholder='選擇一項考試',options=[*[discord.SelectOption(label=f"{dataframe[i][0]}",description=f"{dataframe[i][0]}")for i in range(1, 9)],discord.SelectOption(label='返回',description='back')])
					async def callback(self, interaction: discord.Interaction,select: discord.ui.Select):
						if select.values[0] == '返回':
							the_view = view(self.account,self.password)
							await interaction.response.edit_message(content='選擇你要查詢的類別',view=the_view,embed=None)
						else:
							col_index = self.dataframe.loc[0].eq(select.values[0]).idxmax()
							embed = discord.Embed(title="成績查詢系統",description="所有考試排名",color=0x00ff00)
							field_value = "\n".join([f"{self.dataframe[0][j]}：{self.dataframe[col_index][j]}"for j in range(1, self.dataframe.shape[0])])
							embed.add_field(name=f"{self.dataframe[col_index][0]}",value=field_value,inline=True)
							await interaction.response.edit_message(embed=embed)
				the_exam2_view = exam2_view(dataframe)
				await interaction.edit_original_response(content='選擇你要查詢的考試',view=the_exam2_view)
			except:
				await interaction.edit_original_response(content='帳號或密碼錯誤，或網頁目前不可用',view=None)
				print('成績查詢失敗')
		elif select.values[0] == '所有科目成績':
			try:
				start = time.time()
				dataframe = await gd.spider(self.account, self.password, '所有科目成績')
				dataframe = dataframe[3]
				print(f'成績查詢完畢 花費{time.time()-start}秒')
				account = self.account
				password = self.password
				class exam2_view(discord.ui.View):
					def __init__(self, dataframe, *args, **kwargs):
						super().__init__(*args, **kwargs)
						self.dataframe = dataframe
						self.account = account
						self.password = password
					@discord.ui.select(placeholder='選擇一項科目',options=[*[discord.SelectOption(label=f"{dataframe[i][0]}",description=f"{dataframe[i][0]}")for i in range(1, 13)],discord.SelectOption(label='返回',description='back')])
					async def callback(self, interaction: discord.Interaction,select: discord.ui.Select):
						if select.values[0] == '返回':
							the_view = view(self.account,self.password)
							await interaction.response.edit_message(content='選擇你要查詢的類別',view=the_view,embed=None)
						else:
							col_index = self.dataframe.loc[0].eq(select.values[0]).idxmax()
							embed = discord.Embed(title="成績查詢系統",description="所有科目成績",color=0x00ff00)
							field_value = "\n".join([f"{self.dataframe[0][j]}：{self.dataframe[col_index][j]}"for j in range(1, self.dataframe.shape[0])])
							embed.add_field(name=f"{self.dataframe[col_index][0]}",value=field_value,inline=True)
							await interaction.response.edit_message(embed=embed)
				the_exam2_view = exam2_view(dataframe)
				await interaction.edit_original_response(content='選擇你要查詢的考試',view=the_exam2_view)
			except:
				await interaction.edit_original_response(content='帳號或密碼錯誤，或網頁目前不可用',view=None)
				print('成績查詢失敗')
		elif select.values[0] == '出勤狀況統計':
			try:
				start = time.time()
				dataframe = await gd.spider(self.account, self.password, '出勤狀況統計')
				dataframe = dataframe[2].fillna(0)
				print(f'出缺勤查詢完畢 花費{time.time()-start}秒')
				account = self.account
				password = self.password
				class attend_view(discord.ui.View):
					def __init__(self, *args, **kwargs):
						super().__init__(*args, **kwargs)
						self.account = account
						self.password = password
					@discord.ui.select(placeholder='返回',options=[discord.SelectOption(label='返回',description='back')])
					async def callback(self, interaction: discord.Interaction,select: discord.ui.Select):
						if select.values[0] == '返回':
							the_view = view(self.account,self.password)
							await interaction.response.edit_message(content='選擇你要查詢的類別',view=the_view,embed=None)
				embed = discord.Embed(title='學期出勤狀況',description="出勤狀況統計",color=0x00ff00)
				for i in range(dataframe.shape[1]):
					embed.add_field(name=dataframe[i][0],value=dataframe[i][1])
				await interaction.edit_original_response(embed=embed,view=attend_view())
			except:
				await interaction.edit_original_response(content='帳號或密碼錯誤，或網頁目前不可用',view=None)
				print('成績查詢失敗')
		elif select.values[0] == '出勤詳細日期':
			try:
				start = time.time()
				dataframe = await gd.spider(self.account, self.password, '出勤詳細日期')
				dataframe = dataframe[2].fillna('－－')
				print(f'出缺勤查詢完畢 花費{time.time()-start}秒')
				account = self.account
				password = self.password
				class attend_view(discord.ui.View):
					def __init__(self, *args, **kwargs):
						super().__init__(*args, **kwargs)
						self.account = account
						self.password = password
					@discord.ui.select(placeholder='返回',options=[discord.SelectOption(label='返回',description='back')])
					async def callback(self, interaction: discord.Interaction,select: discord.ui.Select):
						if select.values[0] == '返回':
							the_view = view(self.account,self.password)
							await interaction.response.edit_message(content='選擇你要查詢的類別',view=the_view,embed=None)
				embed = discord.Embed(title='學期出勤狀況',description="出勤詳細日期",color=0x00ff00)
				table = tabulate(dataframe[1:5], headers=[dataframe[i][0] for i in range(13)], tablefmt='plain')
				await interaction.edit_original_response(content=f'```{table}```',view=attend_view())
			except:
				await interaction.edit_original_response(content='帳號或密碼錯誤，或網頁目前不可用',view=None)
				print('成績查詢失敗')

class grade(Cog_Extension):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.dataframe = None
	@commands.Cog.listener()
	async def on_ready(self):
		print('grade_crawler_app.py is working')
	@app_commands.command(name='grade', description='高中校務成績查詢系統')
	async def grade(self, interaction: discord.Interaction, account: str,password: str):
		the_view = view(account, password)
		await interaction.response.send_message(content='選擇你要查詢的類別',view=the_view,ephemeral=True)

async def setup(bot):
	global grade_crawler_app_dataframe
	# grade_crawler_app_dataframe = await gd.spider()
	await bot.add_cog(grade(bot))
