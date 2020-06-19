#coding: utf-8
import os
import discord
import urllib
import random
import math

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



bot = commands.Bot(command_prefix='!')

@bot.command(name='test', help='for testing')
async def testcommand(ctx):
	print("running")
	await ctx.send("Running")

@bot.command(name='10seconds', help='for when you envy the you of 10 seconds ago')
async def tenSeconds(ctx):
	await ctx.send("https://i.imgur.com/tnJtepM.jpg")




class RunescapeCommands:

	@bot.command(name='rslookup', help = 'takes osrs username as a parameter and gives stats on levels and kill count')
	async def rslookup(ctx, *name):
		skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
		skillLevel = ["Level"]
		skillExperience = ["Experience"]
		kcName = ["Name","Unknown1","Unknown2","Unknown3","Clue Scrolls","Beginner Clues","Easy Clues","Medium Clues","Hard Clues","Elite Clues","Master Clues",
					"Unknown4","Abyssal Sire","Hydra","Barrows","Unknown7","Unknown8","Cerberus","Unknown9","Unknown10","Unknown11","Unknown12","Unknown13",
					"Unknown14","Unknown15","Unknown16","Dagganoth Rex","Dagganoth Supreme","Unknown18","Graardor","Unknown20","Unknown21","Hespori","Kalphite Queen",
					"Unknown23","Kraken","Unknown24","K'ril","Mimic","Unknown26","Unknown27","Sarachnis","Unknown29","Skotizo","Unknown30","Unknown31",
					"Unknown32","Thermonuclear","Unknown33","Unknown34","Unknown35","Unknown36","Vorkath","Wintertodt","Zalcano","Zulrah"]
		kcCount = ["Kills"]
		output = ""
		exptotal = 0
		levels_outputList = []
		killcount_outputList = []
		#Variables used in the code, each list is for a column of information.
		username = ' '.join([str(word) for word in name]) 
		#Combines and parses the url to access the OSRS highscores api page for given character name
		await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
		try:
			data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
		except:
			await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
		#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
		dataHolder = data.read().decode().split("\n")
		#Takes each entry in the previous list, splits into the 3 parts, and assigns each to the appropriate column (discarding rank)
		for index in range (len(dataHolder)-1):
			holder = dataHolder[index].split(",")
			if(index>0 and index<len(skillName)-1):
				#Adds either the exp for level 99 or the skills total exp to exptotal, to get an adjusted total value
				exptotal += min(13034431, int(holder[2]))
			if(index<len(skillName)-1):
				skillLevel.append(holder[1])
				skillExperience.append(holder[2])
			else:
				kcCount.append(holder[1])
		#Calculates lengths of horizontal spacers between entries based on the longest entry in the corresponding list
		level_spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
		level_spacer_two = "═".ljust(len(max(skillLevel, key = len)), "═")
		level_spacer_three = "═".ljust(len(max(skillExperience, key = len)), "═")
		exptotal = int(exptotal)
		#Divides adjusted total by the amount of exp needed to 99 all skills, then parses to a percent
		percent_to_99s = round(100*exptotal/299791913, 2)
		#figures out the width of the entire table by adding length of the border stuff to len(spacers)
		level_tableWidth=12 + len(level_spacer_one+level_spacer_two+level_spacer_three)
		#Assembling the header and footer, could be done programatically, but immutable strings
		level_header = " ╔═"+level_spacer_one+"═══"+level_spacer_two+"═══"+level_spacer_three+"═╗\n" + " ║ "+"Stats for " + username + "║".rjust(level_tableWidth-len(" ║ "+"Stats for " + username)-1)+"\n" +  " ╠═"+level_spacer_one+"═╦═"+level_spacer_two+"═╦═"+level_spacer_three+"═╣\n" +  " ║ " + skillName[0].ljust(len(level_spacer_one)) + " ║ " + skillLevel[0].rjust(len(level_spacer_two)) + " ║ " + skillExperience[0].rjust(len(level_spacer_three)) + " ║\n" + " ╠═"+level_spacer_one+"═╬═"+level_spacer_two+"═╬═"+level_spacer_three+"═╣\n"
		level_footer = " ╚═"+level_spacer_one+"═╩═"+level_spacer_two+"═╩═"+level_spacer_three+"═╝\n"
		for index in range(len(skillName)):
			if(index>0):
				#loops through adding one formatted row at a time to the output list
				levels_outputList.append(" ║ " + skillName[index].ljust(len(level_spacer_one)) + " ║ " + skillLevel[index].rjust(len(level_spacer_two)) + " ║ " + skillExperience[index].rjust(len(level_spacer_three)) + " ║\n")
		killcount_dataHolder = data.read().decode().split("\n")
		for index in range (len(skillName)+1, len(killcount_dataHolder)-1):
			holder = killcount_dataHolder[index].split(",")
			kcCount.append(holder[1])
		killcount_spacer_one = "═".ljust(len(max(kcName, key = len)), "═")
		killcount_spacer_two = "═".ljust(len(max(kcCount, key = len)), "═")
		killcount_tableWidth=9 + len(killcount_spacer_one+killcount_spacer_two)
		killcount_header = " ╔═"+killcount_spacer_one+"═══"+killcount_spacer_two+"═╗\n" + " ║ "+"KC for " + username + "║".rjust(killcount_tableWidth-len(" ║ "+"KC for " + username)-1)+"\n" +  " ╠═"+killcount_spacer_one+"═╦═"+killcount_spacer_two+"═╣\n" +  " ║ " + kcName[0].ljust(len(killcount_spacer_one)) + " ║ " + kcCount[0].rjust(len(killcount_spacer_two)) + " ║\n" + " ╠═"+killcount_spacer_one+"═╬═"+killcount_spacer_two+"═╣\n"
		killcount_footer = " ╚═"+killcount_spacer_one+"═╩═"+killcount_spacer_two+"═╝\n"
		for index in range (len(kcName)):
			if(index>0 and int(kcCount[index])>0):
				killcount_outputList.append(" ║ " + kcName[index].ljust(len(killcount_spacer_one)) + " ║ " + kcCount[index].rjust(len(killcount_spacer_two)) + " ║\n")
		await ctx.send("```" + level_header+"".join(levels_outputList)+level_footer + killcount_header + "".join(killcount_outputList) + killcount_footer + "```")
		
	@bot.command(name='rslevels', help = 'takes osrs username as a parameter and gives stats on levels')
	async def rslevels(ctx, *name):
		experienceForLevel = [-1, 0]
		skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
		skillLevel = ["Level"]
		skillExperience = ["Experience"]
		skillMissingExperience = ["Missing Experience", "Irrelevantlol"]
		output = ""
		exptotal = 0
		outputList = []
		for index in range(2, 100):
			experienceForLevel.append(experienceForLevel[index-1] + (math.floor(index-1+300*2**((index-1)/7))/4))
		for index in range(len(experienceForLevel)):
			experienceForLevel[index] = math.floor(experienceForLevel[index])
		#Variables used in the code, each list is for a column of information.
		username = ' '.join([str(word) for word in name]) 
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
				skillMissingExperience.append(13034431 - min(13034431, int(holder[2])))
		#Calculates lengths of horizontal spacers between entries based on the longest entry in the corresponding list
		level_spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
		level_spacer_two = "═".ljust(len(max(skillLevel, key = len)), "═")
		level_spacer_three = "═".ljust(len(max(skillExperience, key = len)), "═")
		exptotal = int(exptotal)
		#Divides adjusted total by the amount of exp needed to 99 all skills, then parses to a percent
		percent_to_99s = round(100*exptotal/299791913, 2)
		#figures out the width of the entire table by adding length of the border stuff to len(spacers)
		tableWidth=12 + len(level_spacer_one+level_spacer_two+level_spacer_three)
		#Assembling the header and footer, could be done programatically, but immutable strings
		header = " ╔═"+level_spacer_one+"═══"+level_spacer_two+"═══"+level_spacer_three+"═╗\n" + " ║ "+"Stats for " + username + "║".rjust(tableWidth-len(" ║ "+"Stats for " + username)-1)+"\n" +  " ╠═"+level_spacer_one+"═╦═"+level_spacer_two+"═╦═"+level_spacer_three+"═╣\n" +  " ║ " + skillName[0].ljust(len(level_spacer_one)) + " ║ " + skillLevel[0].rjust(len(level_spacer_two)) + " ║ " + skillExperience[0].rjust(len(level_spacer_three)) + " ║\n" + " ╠═"+level_spacer_one+"═╬═"+level_spacer_two+"═╬═"+level_spacer_three+"═╣\n"
		footer = " ╠═"+level_spacer_one+"═╩═"+level_spacer_two+"═╩═"+level_spacer_three+"═╣\n" + " ║ Adjusted total EXP = " + str(exptotal) + "║".rjust(tableWidth-len(" ║ Adjusted total EXP = " + str(exptotal))-1)+"\n" + " ║ " + str(percent_to_99s) + "% of the way to all skills 99" + "║".rjust(tableWidth-len(" ║ " + str(percent_to_99s) + "X of the way to all skills 99")-1)+"\n" + " ╚═"+level_spacer_one+"═══"+level_spacer_two+"═══"+level_spacer_three+"═╝\n"
		for index in range(len(skillName)):
			if(index>0):
				#loops through adding one formatted row at a time to the output list
				outputList.append(" ║ " + skillName[index].ljust(len(level_spacer_one)) + " ║ " + skillLevel[index].rjust(len(level_spacer_two)) + " ║ " + skillExperience[index].rjust(len(level_spacer_three)) + " ║\n")
		await ctx.send("```" + header+"".join(outputList)+footer + "```")

	@bot.command(name='rs99', help = 'takes osrs username as a parameter and gives stats on levels')
	async def rs99(ctx, *name):
		def expcalc(missingExperience, skillID):
			def recursivecalc(activityBrackets, experienceBrackets, experienceRateBrackets, loops, remainingTime, totalRemainingTime):
				while(loops>0):
					remainingTime = remainingTime + str(round((experienceBrackets[len(experienceBrackets)-loops] - experienceBrackets[len(experienceBrackets)-(loops+1)])/experienceRateBrackets[len(experienceRateBrackets)-loops],2)) + activityBrackets[len(experienceBrackets)-loops]
					totalRemainingTime = totalRemainingTime + round((experienceBrackets[len(experienceBrackets)-loops] - experienceBrackets[len(experienceBrackets)-(loops+1)])/experienceRateBrackets[len(experienceRateBrackets)-loops],2)
					loops = loops-1
					recursivecalc(activityBrackets, experienceBrackets, experienceRateBrackets, loops, remainingTime, totalRemainingTime)
				# remainingTime = remainingTime + " For a total of " + str(totalRemainingTime) + " hours."
				return remainingTime
			skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
			for index in range(2, 100):
				experienceForLevel.append(experienceForLevel[index-1] + (math.floor(index-1+300*2**((index-1)/7))/4))
			for index in range(len(experienceForLevel)):
				experienceForLevel[index] = math.floor(experienceForLevel[index])
			currentLevel = 0
			remainingBrackets = 0
			for index in range(len(experienceForLevel)):
				if(experienceForLevel[index+1] > experienceForLevel[99]-missingExperience):
					currentLevel = index
					break
			experienceBracketsLazy = []
			if(skillID < 7):
				activityBracketsLazy = [" ", " ammonite crab kills."]
				levelBracketsLazy = [1, 99]
				experienceRateBracketsLazy = [400]				
				if(skillID == 5):
					experienceRateBracketsLazy = [133.33]				
			elif(skillID == 7):
				activityBracketsLazy = [" ", " hours of offering Big Bones at the Gilded Altar."]
				levelBracketsLazy = [1, 99]
				experienceRateBracketsLazy = [133875]
			elif(skillID == 8):
				activityBracketsLazy = [" ", " hours of Lvl-1 enchanting and ", " hours of Lvl-2 enchanting and ", " hours of Lvl-3 enchanting and ", " hours of High Alching."]
				levelBracketsLazy = [1, 27, 49, 55, 99]
				experienceRateBracketsLazy = [28000, 59200, 94400, 78000]
			elif(skillID == 9):
				activityBracketsLazy = [" ", " hours of cooking shrimp and ", " hours of cooking trout and ", " hours of cooking salmon and ", " hours of cooking karambwan."]
				levelBracketsLazy = [1, 15, 25, 35, 99]
				experienceRateBracketsLazy = [35000, 85000, 110000, 250000]
			elif(skillID == 10):
				activityBracketsLazy = [" ", " hours of normal trees and ", " hours of oaks and ", " hours of willows and ", " hours of unmanipulated teaks."]
				levelBracketsLazy = [1,  15, 30, 35, 99]
				experienceRateBracketsLazy = [10000, 40000, 40000, 90000]
			elif(skillID == 11):
				activityBracketsLazy = [" ", " hours of Arrow Shafts and ", " hours of Unstrung Longbows and ", " hours of Unstrung Oak Shortbows and ", " hours of Unstrung Oak Longbows and ", " hours of Unstrung Willow Shortbows and ", " hours of Unstrung Willow Longbows and ", " hours of Unstrung Maple Shortbows and ", " hours of Unstrung Maple Longbows and ", " hours of Unstrung Yew Shortbows and ", " hours of Unstrung Yew Longbows and ", " hours of Unstrung Magic Shortbows and ", " hours of Unstrung Magic Longbows"]
				levelBracketsLazy = [1, 10, 20, 25, 35, 40, 50, 55, 65, 70, 80, 85, 99]
				experienceRateBracketsLazy = [9000, 17000, 28050, 42500, 56525, 70550, 85000, 99025, 114750, 127500, 141100, 155550]
			elif(skillID == 12):
				activityBracketsLazy = [" ", " hours of Shrimp fishing, and ", " hours of Trout fly fishing, and ", " hours of Drift Net fishing."]
				levelBracketsLazy = [1, 20, 47, 99]
				experienceRateBracketsLazy = [1500, 25000, 75000]
			elif(skillID == 13):
				activityBracketsLazy = [" ", " hours of burning normal logs and ", " hours of burning oak logs and ", " hours of burning willow logs and ", " hours of burning maple logs."]
				levelBracketsLazy = [1, 15, 30, 45, 99]
				experienceRateBracketsLazy = [59400, 89100, 133650, 200475]
			elif(skillID == 14):
				activityBracketsLazy = [" ", " hours of making leather gloves and ", " hours of making leather chaps and ", " hours of cutting sapphires and ", " hours of cutting emeralds and ", " hours of cutting rubies and ", " hours of cutting diamonds and ", " hours of making fire battlestaffs and ", " hours of making air battlestaffs and ", " hours of making red d'hide bodies and ", " hours of making black d'hide bodies."]
				levelBracketsLazy = [1, 18, 20, 27, 34, 43, 62, 66, 77, 84, 99]
				experienceRateBracketsLazy = [26000, 50000, 145000, 175000, 230000, 290000, 306000, 336000, 386000, 425000]
			elif(skillID == 15):
				activityBracketsLazy = [" ", " hours of forging bronze daggers and ", " hours of forging bronze scimitars and ", " hours of forging bronze warhammers and ", " hours of forging bronze platebodies and ", " hours of forging iron warhammers and ", " hours of forging iron platebodies and ", " hours of forging steel warhammers and ", " hours of making gold bars in the blast furnace." ]
				levelBracketsLazy = [1, 5, 9, 18, 24, 33, 39, 40, 99]
				experienceRateBracketsLazy = [13900, 25700, 36200, 52100, 72300, 104200, 108500, 300000]
			elif(skillID == 16):
				activityBracketsLazy = [" ", " hours of mining copper or tin ore and ", " hours of mining iron ore and ", " hours of Motherlode Mine."]
				levelBracketsLazy = [1, 15, 30, 99]
				experienceRateBracketsLazy = [5000, 45000, 40000]
			elif(skillID == 17):
				activityBracketsLazy = [" ", " hours of making attack potions and ", " hours of making guam tar and ", " hours of making marrentill tar and ", " hours of making tarromin tar and ", " hours of making harralander tar."]
				levelBracketsLazy = [1, 19, 31, 39, 44, 99]
				experienceRateBracketsLazy = [62500, 61000, 86000, 110000, 145000]
			elif(skillID == 18):
				activityBracketsLazy = [" ", " hours of gnome stronghold agility course and ", " hours of Draynor Village rooftop course and ", " hours of Varrock rooftop course and ", " hours of Canifis rooftop course and ", " hours of Seers' Village rooftop course and ", " hours of Rellekka village rooftop course and ", " hours of Ardougne rooftop course."]
				levelBracketsLazy = [1, 10, 30, 40, 60, 80, 90, 99]
				experienceRateBracketsLazy = [8000, 9000, 13200, 19500, 52000, 54000, 61000]
			elif(skillID == 19):
				activityBracketsLazy = [" ", " hours of pickpocketing normies and ", " hours of stealing from baker's stalls and ", " hours of stealing from fruit stalls and ", " hours of ~~suffering~~ blackjacking bearded bandits and ", " hours of stealing artefacts."]
				levelBracketsLazy = [1, 5, 25, 45, 49, 99]
				experienceRateBracketsLazy = [5000, 19200, 33000, 60000, 160000]
			elif(skillID == 20):
				activityBracketsLazy = [" ", " hours of violence."]
				levelBracketsLazy = [1, 99]
				experienceRateBracketsLazy = [60000]
			elif(skillID == 21):
				activityBracketsLazy = [" ", " hours of raking weeds (don't do this) and " " hours of tithe farming Golovanova and ", " hours of tithe farming Bologano and ", " hours of tithe farming Logavano"]
				levelBracketsLazy = [1, 34, 54, 74 99]
				experienceRateBracketsLazy = [8000, 28273, 65970, 108380]		
			if("activityBracketsLazy" in locals()):
				for index in range(len(levelBracketsLazy)):
					experienceBracketsLazy.append(experienceForLevel[levelBracketsLazy[index]])
				for index in range(len(levelBracketsLazy)):
					if(currentLevel<levelBracketsLazy[index+1]):
						experienceBracketsLazy.pop(0)
						experienceBracketsLazy.insert(index, experienceForLevel[99]-missingExperience)
						remainingBrackets = len(levelBracketsLazy)-(index+1)
						break
				return(recursivecalc(activityBracketsLazy, experienceBracketsLazy, experienceRateBracketsLazy, remainingBrackets, " ", 0))
			return(str(missingExperience))
		experienceForLevel = [-1, 0]
		skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
		skillLevel = ["Level"]
		skillExperience = ["Experience"]
		skillMissingExperience = ["Missing Experience", "Irrelevantlol"]
		output = ""
		exptotal = 0
		outputList = []
		for index in range(2, 100):
			experienceForLevel.append(experienceForLevel[index-1] + (math.floor(index-1+300*2**((index-1)/7))/4))
		for index in range(len(experienceForLevel)):
			experienceForLevel[index] = math.floor(experienceForLevel[index])
		#Variables used in the code, each list is for a column of information.
		username = ' '.join([str(word) for word in name]) 
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
				skillMissingExperience.append(13034431 - min(13034431, int(holder[2])))
		#Calculates lengths of horizontal spacers between entries based on the longest entry in the corresponding list
		level_spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
		level_spacer_two = "═".ljust(len(max(skillLevel, key = len)), "═")
		level_spacer_three = "═".ljust(len(max(skillExperience, key = len)), "═")
		exptotal = int(exptotal)
		#Divides adjusted total by the amount of exp needed to 99 all skills, then parses to a percent
		percent_to_99s = round(100*exptotal/299791913, 2)
		#figures out the width of the entire table by adding length of the border stuff to len(spacers)
		tableWidth=12 + len(level_spacer_one+level_spacer_two+level_spacer_three)
		#Assembling the header and footer, could be done programatically, but immutable strings
		outputTEMP = []
		for index in range(len(skillName)):
			if(index > 1 and skillMissingExperience[index]>0):
				# skillMissingExperience[index] = str(expcalc(skillMissingExperience[index], index))
				# outputTEMP += skillName[index] + " " + str(skillMissingExperience[index]) +"\n\n"
				outputTEMP.append(skillName[index] + " " + str(expcalc(skillMissingExperience[index], index)) +"\n\n")
		await ctx.send("".join(outputTEMP))

	@bot.command(name="rskc", help = 'takes osrs username as a parameter and gives stats on kill counts')
	async def rskc(ctx, *name):
		kcName = ["Name","Unknown1","Unknown2","Unknown3","Clue Scrolls","Beginner Clues","Easy Clues","Medium Clues","Hard Clues","Elite Clues","Master Clues",
					"Unknown4","Abyssal Sire","Hydra","Barrows","Unknown7","Unknown8","Cerberus","Unknown9","Unknown10","Unknown11","Unknown12","Unknown13",
					"Unknown14","Unknown15","Unknown16","Dagganoth Rex","Dagganoth Supreme","Unknown18","Graardor","Unknown20","Unknown21","Hespori","Kalphite Queen",
					"Unknown23","Kraken","Unknown24","K'ril","Mimic","Unknown26","Unknown27","Sarachnis","Unknown29","Skotizo","Unknown30","Unknown31",
					"Unknown32","Thermonuclear","Unknown33","Unknown34","Unknown35","Unknown36","Vorkath","Wintertodt","Zalcano","Zulrah"]
		kcCount = ["Kills"]
		username = ' '.join([str(word) for word in name]) 
		numSkills = 23
		killcount_output = ""
		killcount_outputList = []
		await ctx.send("Looking up " + username + ", please be patient, the API is very slow sometimes.")
		try:
			data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
		except:
			await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
		#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
		killcount_dataHolder = data.read().decode().split("\n")
		for index in range (numSkills+1, len(killcount_dataHolder)-1):
			holder = killcount_dataHolder[index].split(",")
			kcCount.append(holder[1])
		killcount_spacer_one = "═".ljust(len(max(kcName, key = len)), "═")
		killcount_spacer_two = "═".ljust(len(max(kcCount, key = len)), "═")
		killcount_tableWidth=9 + len(killcount_spacer_one+killcount_spacer_two)
		killcount_header = " ╔═"+killcount_spacer_one+"═══"+killcount_spacer_two+"═╗\n" + " ║ "+"KC for " + username + "║".rjust(killcount_tableWidth-len(" ║ "+"KC for " + username)-1)+"\n" +  " ╠═"+killcount_spacer_one+"═╦═"+killcount_spacer_two+"═╣\n" +  " ║ " + kcName[0].ljust(len(killcount_spacer_one)) + " ║ " + kcCount[0].rjust(len(killcount_spacer_two)) + " ║\n" + " ╠═"+killcount_spacer_one+"═╬═"+killcount_spacer_two+"═╣\n"
		killcount_footer = " ╚═"+killcount_spacer_one+"═╩═"+killcount_spacer_two+"═╝\n"
		for index in range (len(kcName)):
			if(index>0 and int(kcCount[index])>0):
				killcount_outputList.append(" ║ " + kcName[index].ljust(len(killcount_spacer_one)) + " ║ " + kcCount[index].rjust(len(killcount_spacer_two)) + " ║\n")
		await ctx.send("```" + killcount_header + "".join(killcount_outputList) + killcount_footer + "```")

@bot.command(name='generate', help="takes a width and height parameter and generates a neat random thing")
async def Generator(ctx, width, height):
	# random.seed(1)
	charset = "╔╦╗╠╬╣╚╩╝═║"
	width = int(width)
	height = int(height)
	success = 0
	if(width<2 or height<2):
		success = 1
		await ctx.send("Too small, lol.")
	if(((height-1)+width*height)>1994):
		success = 1
		await ctx.send("Message length limit says no. ((height-1)+width*height) must be less than 1994.")
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