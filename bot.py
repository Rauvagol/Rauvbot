#coding: utf-8
import os
import discord
import urllib
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='test', help='reports when this file was updated if I remember')
async def testcommand(ctx):
    await ctx.send("May 20th version.")

@bot.command(name='10seconds')
async def tenSeconds(ctx):
	await ctx.send("https://i.imgur.com/tnJtepM.jpg")

@bot.command(name='commands')
async def commands(ctx):
	await ctx.send("Current commands are !test, !10seconds, !commands, !rslevels, !rskc")
	
@bot.command(name='rslevels')
async def rslevels(ctx, *name):
	#Variables used in the code, each list is for a column of information.
	username = ' '.join([str(word) for word in name]) 
	skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
	skillLevel = ["Level"]
	skillExperience = ["Experience"]
	output = ""
	exptotal = 0
	#Combines and parses the url to access the OSRS highscores api page for given character name
	await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
	try:
		data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
	except:
		await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
	#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
	dataHolder = data.read().decode().split("\n")
	#Takes each entry in the previous list, splits into the 3 parts, and assigns each to the appropriate column (discarding rank)
	for index in range (len(skillName)-1):
		holder = dataHolder[index].split(",")
		skillLevel.append(holder[1])
		skillExperience.append(holder[2])
		if(index>0):
			#Adds either the exp for level 99 or the skills total exp to exptotal, to get an adjusted total value
			exptotal += min(13034431, int(holder[2]))
	#Calculates lengths of horizontal spacers between entries based on the longest entry in the corresponding list
	spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
	spacer_two = "═".ljust(len(max(skillLevel, key = len)), "═")
	spacer_three = "═".ljust(len(max(skillExperience, key = len)), "═")
	exptotal = int(exptotal)
	#Divides adjusted total by the amount of exp needed to 99 all skills, then parses to a percent
	percent_to_99s = round(100*exptotal/299791913, 2)
	#figures out the width of the entire table by adding length of the border stuff to len(spacers)
	tableWidth=12 + len(spacer_one+spacer_two+spacer_three)
	#Assembling the header and footer, could be done programatically, but immutable strings
	header = " ╔═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╗\n" + " ║ "+"Stats for " + username + "║".rjust(tableWidth-len(" ║ "+"Stats for " + username)-1)+"\n" +  " ╠═"+spacer_one+"═╦═"+spacer_two+"═╦═"+spacer_three+"═╣\n" +  " ║ " + skillName[0].ljust(len(spacer_one)) + " ║ " + skillLevel[0].rjust(len(spacer_two)) + " ║ " + skillExperience[0].rjust(len(spacer_three)) + " ║\n" + " ╠═"+spacer_one+"═╬═"+spacer_two+"═╬═"+spacer_three+"═╣\n"
	footer = " ╠═"+spacer_one+"═╩═"+spacer_two+"═╩═"+spacer_three+"═╣\n" + " ║ Adjusted total EXP = " + str(exptotal) + "║".rjust(tableWidth-len(" ║ Adjusted total EXP = " + str(exptotal))-1)+"\n" + " ║ " + str(percent_to_99s) + "% of the way to all skills 99" + "║".rjust(tableWidth-len(" ║ " + str(percent_to_99s) + "X of the way to all skills 99")-1)+"\n" + " ╚═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╝\n"
	outputList = []
	for index in range(len(skillName)):
		if(index>0):
			#loops through adding one formatted row at a time to the output list
			outputList.append(" ║ " + skillName[index].ljust(len(spacer_one)) + " ║ " + skillLevel[index].rjust(len(spacer_two)) + " ║ " + skillExperience[index].rjust(len(spacer_three)) + " ║\n")
	await ctx.send("```" + header+"".join(outputList)+footer + "```")

@bot.command(name="rskc")
async def rskc(ctx, *name):
	username = ' '.join([str(word) for word in name]) 
	kcName = ["Name","Unknown1","Unknown2","Unknown3","Clue Scrolls","Beginner Clues","Easy Clues","Medium Clues","Hard Clues","Elite Clues","Master Clues",
				"Unknown4","Abyssal Sire","Hydra","Barrows","Unknown7","Unknown8","Cerberus","Unknown9","Unknown10","Unknown11","Unknown12","Unknown13",
				"Unknown14","Unknown15","Unknown16","Dagganoth Rex","Unknown17","Unknown18","Unknown19","Unknown20","Unknown21","Hespori","Kalphite Queen",
				"Unknown23","Kraken","Unknown24","K'ril","Unknown25","Unknown26","Unknown27","Unknown28","Unknown29","Skotizo","Unknown30","Unknown31",
				"Unknown32","Thermonuclear","Unknown33","Unknown34","Unknown35","Unknown36","Vorkath","Wintertodt","Zalcano","Zulrah"]
	kcCount = ["Kills"]
	numSkills = 23
	output = ""
	outputList = []
	await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
	try:
		data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
	except:
		await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
	#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
	dataHolder = data.read().decode().split("\n")
	for index in range (numSkills+1, len(dataHolder)-1):
		holder = dataHolder[index].split(",")
		kcCount.append(holder[1])
	spacer_one = "═".ljust(len(max(kcName, key = len)), "═")
	spacer_two = "═".ljust(len(max(kcCount, key = len)), "═")
	tableWidth=9 + len(spacer_one+spacer_two)
	header = " ╔═"+spacer_one+"═══"+spacer_two+"═╗\n" + " ║ "+"KC for " + username + "║".rjust(tableWidth-len(" ║ "+"KC for " + username)-1)+"\n" +  " ╠═"+spacer_one+"═╦═"+spacer_two+"═╣\n" +  " ║ " + kcName[0].ljust(len(spacer_one)) + " ║ " + kcCount[0].rjust(len(spacer_two)) + " ║\n" + " ╠═"+spacer_one+"═╬═"+spacer_two+"═╣\n"
	footer = " ╚═"+spacer_one+"═╩═"+spacer_two+"═╝\n"
	for index in range (len(kcName)):
		if(index>0 and int(kcCount[index])>0):
			outputList.append(" ║ " + kcName[index].ljust(len(spacer_one)) + " ║ " + kcCount[index].rjust(len(spacer_two)) + " ║\n")
	await ctx.send("```" + header + "".join(outputList) + footer + "```")

@bot.command(name='maze')
async def MazeGenerator(ctx, width, height):
	# random.seed(1)
	charset = "╔╦╗╠╬╣╚╩╝═║"
	width = int(width)
	height = int(height)
	success = 0
	if(width<2 or height<2):
		success = 1
		await ctx.send("Too small, bet you hear that a lot.")
	if(width*height>1994):
		success = 1
		await ctx.send("Message length limit says no.")
	while(success == 0):
		outputArray = [["X" for column in range(width)] for row in range(height)]
		for row in range(height):
			for column in range(width):
				#top row
				if(row == 0):
					#left side
					if(column == 0):
						outputArray[row][column] = random.choice("╔ ")
					#and left open
					elif(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
						#if not right side
						if(column < width-1):
							outputArray[row][column] = random.choice("╦╗═")
						#if right side
						else:
							outputArray[row][column] = "╗"
					#and left closed
					elif(outputArray[row][column-1] in " ╗╣╝║"):
						#if not right side
						if(column < width-1):
							outputArray[row][column] = random.choice(" ╔")
						#if right side
						else:
							#if left of tile 1 to the left is open
							if(outputArray[row][column-2] in "╔╦╠╬╚╩═"):
								outputArray[row][column-1] = "╦"
							else:
								outputArray[row][column-1] = "╔"
							outputArray[row][column] = "╗"
				#middle rows
				elif(row>0 and row<height-1):
					#left side
					if(column == 0):
						#top open
						if(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
							outputArray[row][column] = random.choice("║╠╚")
						#top closed
						elif(outputArray[row-1][column] in "╚╩╝═ "):
							outputArray[row][column] = random.choice("╔ ")
					#top open
					elif(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
						#left open
						if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
							outputArray[row][column] = random.choice("╬╣╩╝")
						#left closed
						elif(outputArray[row][column-1] in "╗╣╝║ "):
							outputArray[row][column] = random.choice("╠╚║")
					#top closed
					elif(outputArray[row-1][column] in "╚╩╝═ "):
						#left open
						if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
							outputArray[row][column] = random.choice("╦╗═")
						#left closed
						elif(outputArray[row][column-1] in "╗╣╝║ "):
							outputArray[row][column] = random.choice("╔")
					#right side
					if(column == width-1):
						#top open
						if(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
							#left open
							if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
								outputArray[row][column] = random.choice("╣╝")
							#left closed
							elif(outputArray[row][column-1] in "╗╣╝║ "):
								outputArray[row][column] = random.choice("║")
						#top closed
						elif(outputArray[row-1][column] in "╚╩╝═ "):
							#left open
							if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
								outputArray[row][column] = random.choice("╗")
							#left closed
							elif(outputArray[row][column-1] in "╗╣╝║ "):
								outputArray[row][column] = random.choice(" ")
				#bottom row
				if(row == height-1):
					#left side
					if(column == 0):
						#top open
						if(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
							outputArray[row][column] = "╚"
						#top closed
						elif(outputArray[row-1][column] in "╚╩╝═ "):
							outputArray[row][column] = " "
					#top open
					if(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
						#and left open
						if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
							outputArray[row][column] = random.choice("╝╩")
						#and left closed 
						elif(outputArray[row][column-1] in "╗╣╝║ "):
							outputArray[row][column] = random.choice("╚")
					#top closed
					elif(outputArray[row-1][column] in "╚╩╝═ "):
						#and left open
						if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
							outputArray[row][column] = random.choice("═")
						#and left closed 
						elif(outputArray[row][column-1] in "╗╣╝║ "):
							outputArray[row][column] = random.choice(" ")
					#right side
					if(column == width-1):
						#top open
						if(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
							#and left open
							if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
								#good case
								outputArray[row][column] = random.choice("╝")
								success = 1
							#and left closed 
							elif(outputArray[row][column-1] in "╗╣╝║ "):
								success = 0
						#top closed
						elif(outputArray[row-1][column] in "╚╩╝═ "):
							#and left open
							if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
								success = 0
							#and left closed 
							elif(outputArray[row][column-1] in "╗╣╝║ "):
								#good case
								outputArray[row][column] = random.choice(" ")
								success = 1
	outputHolder = []
	for row in outputArray:
		outputHolder.append("".join(map(str, row)))
		outputHolder.append("\n")
	print("".join(outputHolder))
	await ctx.send("```" + "".join(outputHolder)+ "```")

bot.run(TOKEN)