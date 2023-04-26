import discord
from discord import app_commands
from discord.ext import commands
from core.classes import Cog_Extension  #直接core引入類別
import asyncio, time, datetime, random
import custommod.tnfsh as sp


#沒想到你可以到二樓來呢！不過就到這裡為止了，接下來由我物件導向來做你的對手!
#請去補足Class和物件導向基礎觀念，不然你連個雞巴都看不懂
class common(Cog_Extension):  #繼承Cog的功能

	#這跟@bot.event的功用差不多，但注意裝飾器在cog中的區別
	@commands.Cog.listener()  #cog中bot.event的寫法
	async def on_ready(self):
		print('testcommand.py is working')

	

	
	#表情符號用
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if user == self.bot.user:
			return
		if reaction.emoji == '👍' or reaction.emoji == '👎':
			channel = reaction.message.channel
			print(f'[{time.asctime(time.localtime(time.time()))}] {user} 在 {channel.name} 給了個讚 ')

			await reaction.remove(user)
			await channel.send("還敢按讚啊")

	#這大串49行拿來做關鍵字互動(注意不是帶有前綴的指令(!help))
	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author == self.bot.user: return

		# 普通互動區-----{

		#嵌入式訊息測試
		if ctx.content.startswith('hello'):
			embed = discord.Embed(title="Hello!",description="喔是喔真的假的",color=0x00ff00,timestamp=datetime.datetime.now())
			embed.add_field(name="欄位 1", value="555555555", inline=False)
			embed.add_field(name="欄位 2", value="這是欄位 2 的內容", inline=False)
			embed.set_footer(text="test",icon_url="https://cdn.discordapp.com/attachments/1045891061928701973/1090186662568529940/IMG_4204.gif")
			msg = await ctx.channel.send(embed=embed)
			await msg.add_reaction('👍')
			await msg.add_reaction('👎')

		#test
		if ctx.content == 'test':
			print('[' + time.asctime(time.localtime(time.time())) + '] ' +ctx.author.name + ' 在 ' + ctx.channel.name + ' 觸發了 test ')
			print(ctx.content)
			await asyncio.sleep(1)
			await ctx.channel.send(' 123\n456')
			await ctx.channel.send("<@" + str(ctx.author.id) + ">")

		#test1
		if ctx.content == '!test':
			#發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
			tmpmsg = await ctx.channel.send('問就是爆炸了')
			#停頓1秒
			await asyncio.sleep(1)
			#刪除訊息
			await tmpmsg.delete()
			await ctx.channel.send('123\n456')
			await ctx.channel.send({str(ctx.author.mention)})

		#校網爬蟲
		#笑死這段好像是我們的主專案
		if ctx.content == "新聞":
			await ctx.channel.send('[' + time.asctime(time.localtime(time.time())) +'] ')
			embed1 = discord.Embed(title="學店公告", description='News', color=0x00ff00)
			embed1.set_image(url="https://bang-phinf.pstatic.net/a/31faf5/7_0jgUd018bnghjtcj9l5w1zb_1gvolz.jpg")
			news = await sp.studentnews()
			i = 0
			for r2 in news[1]:
				i += 1
				embed1.add_field(name="消息" + str(i), value=r2, inline=False)
			await ctx.channel.send(embed=embed1)

	#接下來都是帶有前綴prefix='!'的指令
	#say指令
	@commands.command()
	async def say(self, ctx):
		print(f'[{time.asctime(time.localtime(time.time()))}] {ctx.author.name}  在 {ctx.channel} 觸發了 !say ')
		print(f'{ctx.author.name} 說 {ctx.message.content}')
		await asyncio.sleep(1)
		tmp = ctx.message.content.split(" ", 2)
		if len(tmp) == 1:
			await ctx.channel.send("八嘎ㄋㄡˊㄋㄡˊ 巴say巴say？")
		else:
			await ctx.channel.send(tmp[1])

	#dice指令
	@commands.command()
	async def dice(self, ctx):
		print(f'[{time.asctime(time.localtime(time.time()))}] {ctx.author.name} 在 {ctx.channel.name} 觸發了 !dice ')
		tmp = ctx.message.content.split(" ", 2)
		number, side = tmp[1].split("d", 2)
		number = int(number)
		side = int(side)
		dealer = 0
		player = 0
		for x in range(number):
			dealer = dealer + random.randint(1, side)
			player = player + random.randint(1, side)
		if dealer >= player:
			await ctx.channel.send(f'莊家點數 : {dealer}\n' +f'{str(ctx.author.mention)}的點數 : {player}\n' +'你輸了哈哈')
		else:
			await ctx.channel.send(f'莊家點數 : {dealer}\n' +f'{str(ctx.author.mention)}的點數 : {player}\n' + '你贏了')

	#test指令
	@commands.command()
	async def test(self, ctx):
		print(f'[{time.asctime(time.localtime(time.time()))}] {ctx.author.name} 在 {ctx.channel.name} 觸發了 test ')
		await asyncio.sleep(1)
		await ctx.channel.send(' 123\n456')
		await ctx.channel.send(ctx.author.mention)


async def setup(bot):
	await bot.add_cog(common(bot))
