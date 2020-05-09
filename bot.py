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
    await ctx.send("May 9th version.")
	
@bot.command(name='rslookup')
async def RSlookup(ctx, *name):
	skillNames= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
	username = ' '.join([str(word) for word in name]) 
	await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
	try:
		data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
	except:
		await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
	split_rle = data.read().decode(data.headers.get_content_charset("utf-8")).split("-1,-1")[0].split("\n")
	split_rle.insert(0, "shouldntbeseen,Level,Experience")
	spacer_one = "═".ljust(len(max(skillNames, key = len)), "═")
	spacer_two = "═".ljust(len(split_rle[0].split(",")[1]), "═")
	spacer_three = "═".ljust(len(split_rle[0].split(",")[2]), "═")
	top_spacer =  "╔"+spacer_one+"╦,"+spacer_two+"╦,"+spacer_three+"╗"
	middle_spacer = "╔"+spacer_one+"╦,"+spacer_two+"╦,"+spacer_three+"╗"
	bottom_spacer = "╔"+spacer_one+"╦,"+spacer_two+"╦,"+spacer_three+"╗"
	output = ""
	inner_width = len(output)
	exptotal = 0
	for index in range (len(split_rle)-1):
		holder = split_rle[index].split(",")
		if(index>1):
			exptotal += min(13034431, int(holder[2]))
		cellOne = skillNames[index].ljust(len(spacer_one))
		try:
			cellTwo = holder[1].rjust(len(spacer_two))
		except: 
			await ctx.send("Error connecting to the API, wait a bit and try again.")
		cellThree = holder[2].rjust(len(spacer_three))
		experienceholder = holder[2]+ "experience\n"
		output = output + " ║ " + cellOne + " ║ " + cellTwo + " ║ " + cellThree + " ║\n"
	exptotal = int(exptotal)
	percent_to_99s = round(100*exptotal/299791913, 2)
	zeroth_horizontal_line= " ╔═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╗\n"
	username_line =         " ║ "+"Stats for " + username + "║".rjust(len(zeroth_horizontal_line)-len(" ║ "+"Stats for " + username)-1)+"\n"
	first_horizontal_line = " ╠═"+spacer_one+"═╦═"+spacer_two+"═╦═"+spacer_three+"═╣\n"
	second_horizontal_line= " ╠═"+spacer_one+"═╬═"+spacer_two+"═╬═"+spacer_three+"═╣\n"
	third_horizontal_line = " ╠═"+spacer_one+"═╩═"+spacer_two+"═╩═"+spacer_three+"═╣\n"
	adjusted_total_exp_line=" ║ Adjusted total EXP = " + str(exptotal) + "║".rjust(len(zeroth_horizontal_line)-len(" ║ Adjusted total EXP = " + str(exptotal))-1)+"\n"
	percent_to_all_99_line= " ║ " + str(percent_to_99s) + "% of the way to all skills 99" + "║".rjust(len(zeroth_horizontal_line)-len(" ║ " + str(percent_to_99s) + "X of the way to all skills 99")-1)+"\n"
	fourth_horizontal_line= " ╚═"+spacer_one+"═══"+spacer_two+"═══"+spacer_three+"═╝\n"
	second_spacer_position = output.find("\n") + 1
	output = output[:second_spacer_position] + second_horizontal_line + output[second_spacer_position:]	
	await ctx.send("```" + zeroth_horizontal_line + username_line + first_horizontal_line +  output + third_horizontal_line + adjusted_total_exp_line + percent_to_all_99_line +  fourth_horizontal_line + "```" )

bot.run(TOKEN)