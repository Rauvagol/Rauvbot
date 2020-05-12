#coding: utf-8
import os
import discord
import urllib

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='test', help='reports when this file was updated if I remember')
async def testcommand(ctx):
    await ctx.send("May 11th version.")
	
@bot.command(name='rslookup')
async def RSlookup(ctx, *name):
	username = ' '.join([str(word) for word in name]) 
	columns = ["Skill Name", "Level", "Experience"]
	skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
	skillLevel = ["Level"]
	skillExperience = ["Experience"]
	output = ""
	exptotal = 0

	await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
	try:
		data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
	except:
		await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
	split_rle = data.read().decode(data.headers.get_content_charset("utf-8")).split("-1,-1")[0].split("\n")
	for index in range (len(split_rle)-1):
		holder = split_rle[index].split(",")
		skillLevel.append(holder[1])
		skillExperience.append(holder[2])
		if(index>0):
			exptotal += min(13034431, int(holder[2]))
	spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
	spacer_two = "═".ljust(len(max(skillLevel, key = len)), "═")
	spacer_three = "═".ljust(len(max(skillExperience, key = len)), "═")
	exptotal = int(exptotal)
	percent_to_99s = round(100*exptotal/299791913, 2)
	tableWidth=len(" ╔═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╗\n")
	header = " ╔═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╗\n" + " ║ "+"Stats for " + username + "║".rjust(tableWidth-len(" ║ "+"Stats for " + username)-1)+"\n" +  " ╠═"+spacer_one+"═╦═"+spacer_two+"═╦═"+spacer_three+"═╣\n" +  " ║ " + skillName[0].ljust(len(spacer_one)) + " ║ " + skillLevel[0].rjust(len(spacer_two)) + " ║ " + skillExperience[0].rjust(len(spacer_three)) + " ║\n" + " ╠═"+spacer_one+"═╬═"+spacer_two+"═╬═"+spacer_three+"═╣\n"
	footer = " ╠═"+spacer_one+"═╩═"+spacer_two+"═╩═"+spacer_three+"═╣\n" + " ║ Adjusted total EXP = " + str(exptotal) + "║".rjust(tableWidth-len(" ║ Adjusted total EXP = " + str(exptotal))-1)+"\n" + " ║ " + str(percent_to_99s) + "% of the way to all skills 99" + "║".rjust(tableWidth-len(" ║ " + str(percent_to_99s) + "X of the way to all skills 99")-1)+"\n" + " ╚═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╝\n"
	outputList = []
	for index in range(len(skillName)-1):
		if(index>0):
			outputList.append(" ║ " + skillName[index].ljust(len(spacer_one)) + " ║ " + skillLevel[index].rjust(len(spacer_two)) + " ║ " + skillExperience[index].rjust(len(spacer_three)) + " ║\n")
	await ctx.send("```" + header+"".join(outputList)+footer + "```")

bot.run(TOKEN)