import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
#from mutagen.mp3 import MP3
bot = commands.Bot(command_prefix=['µsic ','music '], description='Nya~')
global current
if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/opus')

#bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='A playlist example for discord.py')
#bot.add_cog(Music(bot))

@bot.event
@asyncio.coroutine 
def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

@bot.command()
async def forever():
	"""stops music"""
	global voice
	await voice.disconnect()

@bot.command()
async def playing():
	"""says what song is playing"""
	global current
	await bot.say(current)

def play(voice):
	global current
	current= random.choice(os.listdir("./music"))
	#bot.change_presence(game=discord.Game(type=0,name=current))
	global player
	player = voice.create_ffmpeg_player("./music/"+current,after=lambda:play(voice))
	player.start()
	

@bot.command(pass_context=True, no_pm=True)
async def start(self):
	"""starts music"""
	ch=bot.get_channel('377270856893857795')
	global voice
	voice = await bot.join_voice_channel(ch)
	#current=random.choice(os.listdir("./music/"))
	#player = voice.create_ffmpeg_player("./music/"+current)
	#bot.change_presence(game=discord.Game(type=0,name=current))
	#player.start()
	#audio=MP3('./music/'+current)
	#time.sleep(audio.info.length)
	print("we did something\n")
	#while True:
		#current= random.choice(os.listdir("./music"))
		#audio=MP3('./music/'+current)
	play(voice)
		#print (audio.info.length)
		#time.sleep(audio.info.length)
		
		

bot.run('Mzc3Mjk0MzUxODQxMjMwODQ4.DOK2Rg.N8ZRkqDJt1oP7f3uTbEftvPKNJE')
