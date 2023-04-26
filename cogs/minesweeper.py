import discord
from discord import app_commands
from discord.ext import commands
from core.classes import Cog_Extension  #直接core引入類別
import asyncio, random,datetime
import numpy as np


class minesweeper(Cog_Extension):
	pass

	@commands.Cog.listener()  #cog中bot.event的寫法
	async def on_ready(self):
		print('minesweeper.py is working')
		#await self.bot.tree.sync()

	@app_commands.command(name='minesweeper', description='踩地雷')
	async def minesweeper(self, interaction: discord.Interaction, width: int,length: int):
		
		a = np.zeros( (length, width) )
		data = {0:"||:zero:||",1 :"||:one:||",2:"||:two:||",3:"||:three:||",4:"||:four:||",5:"||:five:||",6:"||:six:||",7:"||:seven:||",8:"||:eight:||"}
		mine = random.randint(1, length+width)
		flag = mine
		for z in range(mine):
			x=random.randint(0,length-1)
			y=random.randint(0,width-1)
			if a[x,y] >= 9:
				flag-=1
			else:
				a[x,y] = 9
				if x-1>=0:
					a[x-1,y] +=1
					if y-1>=0:
						a[x-1,y-1] += 1
					if y+1 <= width-1:
						a[x-1,y+1] += 1
				if y-1>=0:
					a[x,y-1] += 1
				if y+1 <= width-1:
					a[x,y+1] += 1
				if x+1 <= length-1:
					a[x+1,y] += 1
					if y-1>=0:
						a[x+1,y-1] += 1
					if y+1 <= width-1:
						a[x+1,y+1] += 1	
		embed1 = discord.Embed(title="踩地雷",color=0x00ff00,timestamp=datetime.datetime.now())
		#embed1.set_thumbnail(url="https://i.imgur.com/nBjAjix.png")
		sweeper = ""
		
		for x in range(length):
				for y in range(width):
					if a[x,y] >= 9:
						b = "||:bomb:||"
					else:
						b=data[a[x,y]]
					sweeper = sweeper + b
				sweeper = sweeper + "\n"					
		embed1.add_field(name="地雷數量:"+ str(flag),value=sweeper, inline=False)	
		await interaction.response.send_message(embed=embed1) 


async def setup(bot):
	await bot.add_cog(minesweeper(bot))
