import discord
from discord.ext import commands
import asyncio, json, os, matplotlib
print(matplotlib.__file__)
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# 調用 event 函式庫
@bot.event
# 當機器人完成啟動時
async def on_ready():
	game = discord.Game('校網翻頁爬蟲佐成績查詢拌籤運拉霸博弈DC BOT for 24hr V1.0')
	# discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
	synced = await bot.tree.sync()  #這行程式碼的功能要讓 Bot 的斜線指令可以同步到 Discord 上
	await bot.change_presence(status=discord.Status.online, activity=game)
	print('目前登入身份：', bot.user)
	print(f'application command has synced {len(synced)} commands')


#做cogs裡的所有檔案讀取
async def cogs():
	for filename in os.listdir("./cogs"):
		if filename.endswith("py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")


asyncio.run(cogs())


#這是在啟動bot區的slash command寫法，跟cog裡的差別只在裝飾器而已(cog中使用app_commands.command())
#然後這裡是在做reload，在做動態測試可以用到
@bot.tree.command(name='reload', description='reload all commands')
async def reload(interaction: discord.Interaction):
	for filename in os.listdir("./cogs"):
		if filename.endswith("py"):
			await bot.reload_extension(f"cogs.{filename[:-3]}")
	await interaction.response.send_message('重新載入指令完畢')
	print('user used reload')



#開token.json，詳細用法上網查
with open('token.json', 'r', encoding='UTF-8') as j:
	Token = json.load(j)
bot.run(Token["token"])
