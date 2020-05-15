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
    await ctx.send("May 13th version.")
	
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
	cornerCells = "╔╗╚╝"
	midCells = "═║╝╚╗╔╩╠╦╣╬"
	topCells = "═╗╔╦"
	bottomCells = "═╝╚╩"
	l_to_rd = "╦╗═"
	lr_to_d = "╦═"
	urd = "╠╚║╔"
	uld = "╣╝║╗"
	rul = "╩╝═╚"
	rdl = "╦╗═╔"
	width = int(width)
	height = int(height)
	outputArray = []
	for row in range(height):
		holderArray = []
		for column in range(width):
			holderArray.append(str(column))
		if(row == 0):
			holderArray[0] = cornerCells[0]
			holderArray[width-1] = cornerCells[1]
			for entry in range(1, width-1):
				holderArray[entry] = "0"
				if(holderArray[entry-1] == "╔" or holderArray[entry-1] == "═" or holderArray[entry-1] == "╦"):
					holderArray[entry] = random.choice(l_to_rd)
					if(holderArray[entry+1] == "╗"):
						holderArray[entry] = random.choice(lr_to_d)
				else:
					holderArray[entry] = "╔"
		if(row == height-1):
			holderArray[0] = cornerCells[2]
			holderArray[width-1] = cornerCells[3]
		print("".join(holderArray))
		outputArray.append("".join(holderArray))
		outputArray.append("\n")
	await ctx.send("```" + "".join(outputArray)+ "```")
bot.run(TOKEN)