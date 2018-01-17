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
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!µsic ','!music ','!Music '), descripton='I love Ramen, Kayo-chin, and being a School Idol!')
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

#@bot.command(pass_context=True)
#@asyncio.coroutine
#def iam(ctx,*,role):
#	Role=discord.utils.get(ctx.message.server.roles,name="super cool role")
	#if "" in role.lower():
#	print ("something")
#	yield from bot.add_roles(ctx.message.author,Role)


@bot.command()
@asyncio.coroutine
def restart():
	"""Say this if Rin-chan is misbehaving :3"""
	sys.exit(0)

@bot.command(pass_context=True)
@asyncio.coroutine
def request(ctx,*,message):
	"""Request Rin-chan to play a song! If you only know some of the name that's fine, I'll help"""
	global requests
	potential=[]
	bot.send_typing(ctx.message.channel)
	for song in songList:
		if message.lower()+'.mp3'==song.lower():
			requests.append(song)
			#yield from bot.say("added")
			yield from bot.add_reaction(ctx.message,discord.utils.get(ctx.message.server.emojis, name="rinok"))
			return 0
		elif (message.lower()) in song.lower():
			potential.append(song)
	if len(potential)==0:
		yield from bot.say("song not found")
	elif len(potential)==1:
		#yield from bot.say("added")
		yield from bot.add_reaction(ctx.message,discord.utils.get(ctx.message.server.emojis, name="rinok"))
		requests.append(potential[0])
	else:
		response="```these are potential matches, try being more specific version"
		x=0
		for song in potential:
			response+='\n'
			response+=song
		response+='```'
		yield from bot.say(response)


#@bot.command()
#@asyncio.coroutine
#def sleep(*,sleepytime):
#	"""currently disabled"""
#	global voice
#	global sleep
	#sleep=int(sleepytime)
	#yield from bot.say("Rin is going to take a quick {} second catNyap!".format(sleep))

@bot.command(pass_context=True)
@asyncio.coroutine
def list(ctx):
	"""I can message you all the songs I know!"""
	for songName in songs:
		yield from bot.send_message(ctx.message.author,songName)

@bot.command()
@asyncio.coroutine
def update():
	"""Sometimes I forget when I learn new songs~"""
	global songList
	global songs
	songList=os.listdir("./music/")
	songs=['```']
	for song in songList:
		if len(songs[-1])>1800:
			songs[-1]+='```'
			songs.append('```')
		if '.mp3' in song:
			songs[-1]+=song.replace('.mp3','')
			songs[-1]+='\n'
	songs[-1]+='```'

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
	channel=open("channel.txt","r")
	ch=bot.get_channel(channel.read().strip())
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
				if ".mp3" not in current:
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
				if ".mp3" not in current:
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
				if ".mp3" not in current:
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
	"""If you want me to play another song"""
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
	"""Let's start the music!"""
	global mode
	mode="./music/"
	global message
	if message!=2:
		message=1
		bot.loop.create_task(play())

@bot.command(pass_context=True)
@asyncio.coroutine
def rin(self):
	"""If you only want to hear me singing"""
	global mode
	mode="./music/rin/"

@bot.command(pass_context=True)
@asyncio.coroutine
def all(self):
	"""If you like all Love Live Music!"""
	global mode
	mode="./music/"

global message
message=0
file_object=open("key.txt","r")
bot.run(file_object.read().strip())
