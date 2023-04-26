import discord
from discord import app_commands
from discord.ext import commands
from core.classes import Cog_Extension  #直接core引入類別
import asyncio


class slashcommand(Cog_Extension):  #繼承Cog的功能

	@commands.Cog.listener()  #cog中bot.event的寫法
	async def on_ready(self):
		print('slashcommand.py is working')
		#await self.bot.tree.sync()

	@app_commands.command(name='指令名稱', description='指令描述')
	async def test(self, interaction: discord.Interaction):
		#需先對interaction做一次response，否則客戶端會卡該申請未受回應
		await interaction.response.send_message('開發範例1')
		await interaction.followup.send('開發範例2')  #followup會提及上一則response
		await asyncio.sleep(2)
		await interaction.channel.send('開發範例3')  #另一種無提及的寫法



	#get channel command
	# @app_commands.command(name='get_channel',
	#                       description='get channel where you are')
	# async def get_channel(self, interaction: discord.Interaction):
	# 	channelname = interaction.channel.name
	# 	channelid = interaction.channel.id
	# 	await interaction.response.send_message(
	# 	 content=f'name :{channelname}\nID :{channelid}')


async def setup(bot):
	await bot.add_cog(slashcommand(bot))
