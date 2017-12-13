import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
from random import shuffle
import sys
#from mutagen.mp3 import MP3
bot = commands.Bot(command_prefix=['!µsic ','!music ','!Music '], descriptio='I love Ramen and Kayo-chin')
songList=os.listdir("./music/")

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('opus')



songs=['```']

for song in songList:
	if len(songs[-1])>1800:
		songs[-1]+='```'
		songs.append('```')
	if '.mp3' in song:
		songs[-1]+=song.replace('.mp3','')
		songs[-1]+='\n'
songs[-1]+='```'



@bot.event
@asyncio.coroutine 
def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
	yield from bot.change_presence(game=discord.Game(type=1,name='Type \"!music start\" to start music'))
	global requests
	requests=[]


@bot.command()
@asyncio.coroutine
def restart():
	"""reboot the bot, run if bot refuses to play"""
	sys.exit(0)

@bot.command(pass_context=True)
@asyncio.coroutine
def request(ctx,*,message):
	global requests
	potential=[]
	bot.send_typing(ctx.message.channel)
	for song in songList:
		if message.lower()+'.mp3'==song.lower():
			requests.append(song)
			yield from bot.say("added")
			return 0
		elif song.lower().startswith(message.lower()):
			potential.append(song)
	if len(potential)==0:
		yield from bot.say("song not found")
	elif len(potential)==1:
		yield from bot.say("added")
		requests.append(potential[0])
	else:
		response="```these are potential matches, try being more specific version"
		x=0
		for song in potential:
			response+='\n'
			response+=song
		response+='```'
		yield from bot.say(response)


@bot.command()
@asyncio.coroutine
def sleep(*,sleepytime):
	"""currently disabled"""
	global voice
	global sleep
	#sleep=int(sleepytime)
	#yield from bot.say("Rin is going to take a quick {} second catNyap!".format(sleep))

@bot.command(pass_context=True)
@asyncio.coroutine
def list(ctx):
	for songName in songs:
		yield from bot.send_message(ctx.message.author,songName)

@asyncio.coroutine
def play():
	global message
	yield from bot.wait_until_ready()
	global mode
	global voice
	global sleep
	global current
	global requests
	localmode=mode
	sleep = 0
	ch=bot.get_channel('280954773346320387')
	voice = yield from bot.join_voice_channel(ch)
	songs=shuff()
	current=songs.pop(0)
	player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
	yield from bot.change_presence(game=discord.Game(type=2,name=current))
	player.start()
	while True:
		if message==-1:
			player.stop()
			sys.exit(0)
			break
		elif message==5 or mode!=localmode:
			message=1
			player.stop()
			if len(songs)<1 or mode!=localmode:
				songs=shuff()
				localmode=mode
			if len(requests)>0:
				current=requests.pop(0)
			else:
				current=songs.pop(0)
			yield from bot.change_presence(game=discord.Game(type=2,name=current))
			player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
			player.start()
		elif sleep!=0:
			print ("about to sleep\n")
			player.stop()
			yield from bot.change_presence(game=discord.Game(type=2,name="quick {} second nap!".format(sleep)))
			yield from voice.disconnect()
			yield from asyncio.sleep (sleep)
			sleep = 0
			voice=yield from bot.join_voice_channel(ch)
			if len(songs)<1:
				songs=shuff()
			if len(requests)>1:
				current=requests.pop(0)
			else:
				current=songs.pop(0)
			player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
			player.start()
		elif player.is_playing():
			yield from asyncio.sleep(5)
		else:
			if len(songs)<1:
				songs=shuff()
			if len(requests)>0:
				current=requests.pop(0)
			else:
				current=songs.pop(0)
			yield from bot.change_presence(game=discord.Game(type=2,name=current))
			player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
			player.start()



def shuff():
	global mode
	songList=os.listdir(mode)
	shuffle(songList)
	return songList

@bot.command(pass_context=True)
@asyncio.coroutine
def skip(self):
	"""skips song"""
	global message
	message=5


@bot.command(pass_context=True)
@asyncio.coroutine
def forever(self):
	"""stops music (for now)"""
	global message
	message=-1
	yield from bot.change_presence(game=discord.Game(type=1,name='Type \"!music start\" to start music'))

@bot.command(pass_context=True)
@asyncio.coroutine
def start(self):
	"""starts music"""
	global mode
	mode="./music/"
	global message
	if message!=2:
		message=1
		bot.loop.create_task(play())

@bot.command(pass_context=True)
@asyncio.coroutine
def rin(self):
	"""sets to only play rin solos"""
	global mode
	mode="./music/rin/"

@bot.command(pass_context=True)
@asyncio.coroutine
def all(self):
	"""sets to play all love live music (includes rin solos"""
	global mode
	mode="./music/"

global message
message=0
bot.run('Mzc3Mjk0MzUxODQxMjMwODQ4.DOK2Rg.N8ZRkqDJt1oP7f3uTbEftvPKNJE')
