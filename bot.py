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
    await ctx.send("May 16th version.")
	
@bot.command(name='rslookup')
async def RSlookup(ctx, *name):
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
	split_rle = data.read().decode(data.headers.get_content_charset("utf-8")).split("-1,-1")[0].split("\n")
	#Takes each entry in the previous list, splits into the 3 parts, and assigns each to the appropriate column (discarding rank)
	for index in range (len(split_rle)-1):
		holder = split_rle[index].split(",")
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
	for index in range(len(skillName)-1):
		if(index>0):
			#loops through adding one formatted row at a time to the output list
			outputList.append(" ║ " + skillName[index].ljust(len(spacer_one)) + " ║ " + skillLevel[index].rjust(len(spacer_two)) + " ║ " + skillExperience[index].rjust(len(spacer_three)) + " ║\n")
	await ctx.send("```" + header+"".join(outputList)+footer + "```")

@bot.command(name='maze')
async def MazeGenerator(ctx, width, height):
	# random.seed(1)
	charset = "╔╦╗╠╬╣╚╩╝═║"
	width = int(width)
	height = int(height)
	outputArray = outputArray = [[row for column in range(width)] for row in range(height)]

	for row in range(height):
		for column in range(width):
			if(row == 0):
				#left side
				if(column == 0):
					outputArray[row][column] = "╔"
				#and left open
				elif(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
					#if not right side
					if(column < width-1):
						outputArray[row][column] = random.choice("╦╗═")
					#if right side
					else:
						outputArray[row][column] = "╗"
				#and left closed
				elif(outputArray[row][column-1] in "╗╣╝║"):
					#if not right side
					if(column < width-1):
						outputArray[row][column] = random.choice("╔")
					#if right side
					else:
						outputArray[row][column-1] = "╦"
						outputArray[row][column] = "╗"
			# if(row==0 and 0<column<width-1):
			# 	if(outputArray[row][column-1] == "╔" or outputArray[row][column-1] == "═" or outputArray[row][column-1] == "╦" and outputArray[row][column+1] == "╗"):
			# 		outputArray[row][column] = random.choice("╦═")
			# 	elif(outputArray[row][column-1] == "╔" or outputArray[row][column-1] == "═" or outputArray[row][column-1] == "╦"):
			# 		outputArray[row][column] = random.choice("╦═╗")
			# 	else:
			# 		outputArray[row][column] = "╔"
			# if(row<(height-1)):
			# 	outputArray[row][0] = random.choice("╠║")
			# 	outputArray[row][width-1] = random.choice("╣║")
			# 	if(column<width-1):
			# 		#top row

			# 		#above open
			# 		elif(outputArray[row-1][column] in "╔╦╗╠╬╣║"):
			# 			#and left open
			# 			if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
			# 				outputArray[row][column] = random.choice("╬╣╝")
			# 			#and left closed
			# 			elif(outputArray[row][column-1] in "╗╣╝║"):
			# 				outputArray[row][column] = random.choice("╠╚║")
			# 		#above closed
			# 		elif(outputArray[row-1][column] in "╚╩╝═"):
			# 			#and left open
			# 			if(outputArray[row][column-1] in "╔╦╠╬╚╩═"):
			# 				outputArray[row][column] = random.choice("╦╗")
			# 			#and left closed
			# 			elif(outputArray[row][column-1] in "╗╣╝║"):
			# 				outputArray[row][column] = random.choice("╔")
			# if(row==height-1 and 0<column<width-1):
			# 	if(outputArray[row][column-1] == "╚" or outputArray[row][column-1] == "═" or outputArray[row][column-1] == "╩" and outputArray[row][column+1] == "╝"):
			# 		outputArray[row][column] = random.choice("╩═")
			# 	if(outputArray[row][column-1] == "╚" or outputArray[row][column-1] == "═" or outputArray[row][column-1] == "╩"):
			# 		outputArray[row][column] = random.choice("╩═╝")
			# 	else:
			# 		outputArray[row][column] = "╚"
	outputHolder = []
	for row in outputArray:
		outputHolder.append("".join(map(str, row)))
		outputHolder.append("\n")
	print("".join(outputHolder))
	await ctx.send("```" + "".join(outputHolder)+ "```")

bot.run(TOKEN)