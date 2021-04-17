#coding: utf-8
import os
import discord
import urllib
import random
import math
import time
import string

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
# bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	print("logged in")

@bot.command(name='test', help='for testing')
async def testcommand(ctx):
	print("running")
	await ctx.send("Running")

@bot.event
async def on_raw_reaction_add(payload):
	message_id=payload.message_id
	if(message_id == 773416052796555264):
		guild = bot.get_guild(payload.guild_id)
		if(payload.emoji.name == "nice"):
			role = discord.utils.get(guild.roles, name='test role')
		if(role is not None):
			member = payload.member
			if(member is not None):
				await member.add_roles(role)
				print(str(member) + " assigned role \"" + role.name + "\"")


@bot.event
async def on_raw_reaction_remove(payload):
	message_id=payload.message_id
	if(message_id == 773416052796555264):
		print(" ")
		print(payload)
		guild = bot.get_guild(payload.guild_id)
		print(guild)
		print(payload.user_id)
		print(str(guild.get_member(106205285760135168)))
		member = guild.get_member(payload.user_id)
		print(member)
		if(payload.emoji.name == "nice"):
			print("yes")
			role = discord.utils.get(guild.roles, name='test role')
			print(role.name)
		if(role is not None):
			print(payload)
			print(member)
			print(guild.get_member(payload.user_id))
			if(member is not None):
				print("here")
				await member.remove_roles(role)

last_niced = 0
@bot.event
async def on_message(message):
	if("lmao" in message.content.lower()):
		await message.channel.send("You mean lamo.")
	if(message.content.lower().translate(str.maketrans('','',string.punctuation)) == "nice"):
		global last_niced
		if(time.time() > last_niced+120):
			print (str(time.time()) + ">" + str(last_niced+5))
			if(not message.author.bot):
					last_niced = time.time()
					await message.channel.send('Nice.')
	if(message.content.lower().translate(str.maketrans('','',string.punctuation)) == "shut up" and message.author.id == 124664055251075072):
			await message.channel.send('lamo')
	if(message.content.lower().translate(str.maketrans('','',string.punctuation)) == "test"):
		print("yes")
	if("kate beckinsale" in message.content.lower()):
		await message.channel.send("https://tenor.com/view/smiling-hehehe-how-you-doin-kate-beckinsale-gif-15386322")
	else:
		await bot.process_commands(message)

class ChatCommands:

	@bot.command(name='10seconds', help='for when you envy the you of 10 seconds ago')
	async def tenSeconds(ctx):
		await ctx.send("https://i.imgur.com/tnJtepM.jpg")

	@bot.command(name='cunt', help='for when you need to express yourself in song')
	async def tenSeconds(ctx):
		await ctx.send("https://www.youtube.com/watch?v=VFh8WubLzYY")

	@bot.command(name='christmas', help='for the holiday spirit')
	async def christmas(ctx):
		await ctx.send("Christmas is coming up lads and lasses and i've got a serious skoadon (skoda rod on ha ha). everyone knows me as a half time bible basher and full time beer lover. if you don't know me... get to know me 😉 as you know i have a girlfriend and she is BEAUTFul... woof woof. So sorry to all the single girls who were expected me as a stocking filler (if you're picking up what i'm putting down).. LOL. Any who let me explain what i'm offering here. GIVEAWAY TIME!!!! I'm giving away a set of sweet sweet Marbles. All you have to do is send me a picture of your bare feet (business never pleasure). the winner will be announced on my Clash of Clans blog.\n\nAlways a pleasure never a chore.\n\np.s. GOD LOVES YOU!")

	@bot.command(name='breakup', help = 'for serious conversations')
	async def breakup(ctx):
		await ctx.send("Babe :baby::sob:, i'm :cupid: breaking :hammer: up :arrow_up: with you :point_left_tone2:. it's not you :point_left::no_entry_sign:, you :point_left: were poggers :sunglasses::nail_care:. it's me, i'm :cupid: omegalul :crying_cat_face::person_frowning:. im :cupid: sorry :person_bowing: if this is pepehands :palms_up_together: but :thinking: it has to be done :hammer:, i've :person_raising_hand_tone1: just been feeling :grin: pepega and our relationship :couple: has been weirdchamp :scream_cat: for months :calendar_spiral:, it's time :clock1: to end :end: it, no :persevere: kappa :stuck_out_tongue_closed_eyes::zany_face::kissing_heart:")

	@bot.command(name = 'modabuse',  help = "change user's nickname given id and new nickname")
	async def modabuse(ctx, id: int, newname):
		if(id == 106205285760135168):
			await ctx.send("No can do boss. Discord doesn't let me opress the server owner.")
		victim = await ctx.guild.fetch_member(id)
		await victim.edit(nick = newname)
		await ctx.send("Done")

class RunescapeCommands:

	@bot.command(name='rslevels', help = 'takes osrs username as a parameter and gives stats on levels')
	async def rslevels(ctx, *name):
		def getHiScores(username):
			totalExperience = [0,0,0,0]
			try:
				totalExperience[0] = int(urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
			except:
				pass
			try:
				totalExperience[1] = int(urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
			except:
				pass
			try:
				totalExperience[2] = int(urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
			except:
				pass
			try:
				totalExperience[3] = int(urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
			except:
				pass
			print(totalExperience)
			print(max(totalExperience))
			if(totalExperience[3] == max(totalExperience)):
				print("uim")
				return urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")
			elif(totalExperience[2] == max(totalExperience)):
				print("hcim")
				return urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")
			elif(totalExperience[1] == max(totalExperience)):
				print("im")
				return urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")
			else:
				print("normie")
				return urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20")).read().decode().split("\n")
		experienceForLevel = [-1, 0]
		skillName= ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
		skillLevel = ["Level"]
		skillExperience = ["Experience"]
		skillMissingExperience = ["Missing Experience", "Irrelevantlol"]
		output = ""
		exptotal = 0
		outputList = []
		async with ctx.typing():
			for index in range(2, 100):
				experienceForLevel.append(experienceForLevel[index-1] + (math.floor(index-1+300*2**((index-1)/7))/4))
			for index in range(len(experienceForLevel)):
				experienceForLevel[index] = math.floor(experienceForLevel[index])
			#Variables used in the code, each list is for a column of information.
			username = ' '.join([str(word) for word in name]) 
			#Combines and parses the url to access the OSRS highscores api page for given character name
			try:
				dataHolder=getHiScores(username)
			except:
				await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
				return
			#Takes each entry in the previous list, splits into the 3 parts, and assigns each to the appropriate column (discarding rank)
			for index in range (len(skillName)-1):
				holder = dataHolder[index].split(",")
				skillLevel.append(holder[1])
				skillExperience.append(holder[2])
				if(index>0):
					#Adds either the exp for level 99 or the skills total exp to exptotal, to get an adjusted total value
					exptotal += min(13034431, int(holder[2]))
					skillMissingExperience.append(13034431 - min(13034431, int(holder[2])))
			for index in range(len(skillLevel)):
				if skillLevel[index] == "69":
					skillLevel[index] = "Nice."
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
		async with ctx.typing():
			def expcalc(missingExperience, skillID):
				def recursivecalc(activityBrackets, experienceBrackets, experienceRateBrackets, loops, remainingTime, totalRemainingTime):
					while(loops>0):
						remainingTime.append(str(round((experienceBrackets[len(experienceBrackets)-loops] - experienceBrackets[len(experienceBrackets)-(loops+1)])/experienceRateBrackets[len(experienceRateBrackets)-loops],2)) + activityBrackets[len(experienceBrackets)-loops])
						totalRemainingTime = totalRemainingTime + round((experienceBrackets[len(experienceBrackets)-loops] - experienceBrackets[len(experienceBrackets)-(loops+1)])/experienceRateBrackets[len(experienceRateBrackets)-loops],2)
						loops = loops-1
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
					activityBracketsLazy = [" ", " hours of Arrow Shafts and ", " hours of Unstrung Longbows and ", " hours of Unstrung Oak Shortbows and ", " hours of Unstrung Oak Longbows and ", " hours of Unstrung Willow Shortbows and ", " hours of Unstrung Willow Longbows and ", " hours of Unstrung Maple Shortbows and ", " hours of Unstrung Maple Longbows and ", " hours of Unstrung Yew Shortbows and ", " hours of Unstrung Yew Longbows and ", " hours of Unstrung Magic Shortbows and ", " hours of Unstrung Magic Longbows."]
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
					activityBracketsLazy = [" ", " hours of raking weeds (don't do this) and ", " hours of tithe farming Golovanova and ", " hours of tithe farming Bologano and ", " hours of tithe farming Logavano."]
					levelBracketsLazy = [1, 34, 54, 74, 99]
					experienceRateBracketsLazy = [8000, 28273, 65970, 108380]
				elif(skillID == 22):
					activityBracketsLazy = [" ", " hours of crafting tiaras and ", " hours of crafting smoke runes."]
					levelBracketsLazy = [1, 15, 99]
					experienceRateBracketsLazy = [40000, 50000]
				elif(skillID == 23):
					activityBracketsLazy = [" ", " regular birdhouses and ", " oak birdhouses and ", " willow birdhouses and ", " teak birdhouses and ", " maple birdhouses and ", " mahogany birdhouses and ", " yew birdhouses and ", " magic birdhouses and ", " redwood birdhouses."]
					levelBracketsLazy = [5, 14, 24, 34, 44, 49, 59, 74, 89, 99]
					experienceRateBracketsLazy = [280, 420, 560, 700, 820, 960, 1020, 1140, 1200]
				elif(skillID == 24):
					activityBracketsLazy = [" ", " regular planks and ", " oak planks."]
					levelBracketsLazy = [1, 15, 99]
					experienceRateBracketsLazy = [29, 60]
				remainingTime = []
				if("activityBracketsLazy" in locals()):
					for index in range(len(levelBracketsLazy)):
						experienceBracketsLazy.append(experienceForLevel[levelBracketsLazy[index]])
					for index in range(len(levelBracketsLazy)):
						if(currentLevel<levelBracketsLazy[index+1]):
							experienceBracketsLazy.pop(0)
							experienceBracketsLazy.insert(index, experienceForLevel[99]-missingExperience)
							remainingBrackets = len(levelBracketsLazy)-(index+1)
							break
					return(recursivecalc(activityBracketsLazy, experienceBracketsLazy, experienceRateBracketsLazy, remainingBrackets, remainingTime, 0))
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
			try:
				data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
			except:
				await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
			#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
			dataHolder = data.read().decode().split("\n")
			#Takes each entry in the previous list, splits into the 3 parts, and assigns each to the appropriate column (discarding rank)
			
			rs99_spacer_two_length = 0
			for index in range (len(skillName)-1):
				holder = dataHolder[index].split(",")
				skillLevel.append(holder[1])
				skillExperience.append(holder[2])
				if(index>0):
					skillMissingExperience.append(13034431 - min(13034431, int(holder[2])))
			outputTEMP = []
			calculated_holder = []
			for index in range(len(skillName)):
				if(index > 1 and skillMissingExperience[index]>0):
					calculated_holder.append("".join(expcalc(skillMissingExperience[index], index)))
			try:
				longest_skill_todo = max(calculated_holder, key=len)
			except:
				if(username=="himtheguy"):
					await ctx.send("https://youtu.be/LDU_Txk06tM?t=75")
			longest_skill = -1
			for index in range (len(calculated_holder)):
				if(len(calculated_holder[index])==len(longest_skill_todo)):
					longest_skill = index
			rs99_spacer_one = "═".ljust(len(max(skillName, key = len)), "═")
			rs99_spacer_two = "═".ljust(len(max(calculated_holder, key = len)), "═")
			associatedSkill = []
			for index in range(len(skillName)):
				if(index > 1 and skillMissingExperience[index]>0):
					holder = "".join(expcalc(skillMissingExperience[index], index))
					associatedSkill.append(skillName[index])
					outputTEMP.append(" ║ " + skillName[index].ljust(len(rs99_spacer_one)) + " ║ " + holder.rjust(len(rs99_spacer_two)) +" ║\n")
			print(associatedSkill)
			print(calculated_holder)
			header = " ╔═" + rs99_spacer_one + "═╦═" + rs99_spacer_two + "═╗\n"+" ║ " + "Skill Name".ljust(len(rs99_spacer_one)) + " ║ " + "To Do:".ljust(len(rs99_spacer_two)) + " ║\n"+" ╠═" + rs99_spacer_one + "═╬═" + rs99_spacer_two + "═╣\n"
			footer = " ╚═" + rs99_spacer_one + "═╩═" + rs99_spacer_two + "═╝\n"
		try:
			await ctx.send("```"+ header + "".join(outputTEMP)+footer+"```")
		except:
			await ctx.send("Error, to-do list too long, work on " + associatedSkill[longest_skill][:-1] + ", requiring " + calculated_holder[longest_skill])

	@bot.command(name="rskc", help = 'takes osrs username as a parameter and gives stats on kill counts')
	async def rskc(ctx, *name):
		kcName = ["Name","Unknown1","Bounty Hunter - Hunter","Bounty Hunter - Rogue","Clue Scrolls (Total)","Beginner Clues","Easy Clues","Medium Clues","Hard Clues","Elite Clues","Master Clues",
					"LMS", "SPACER, IF YOU SEE THIS YELL AT ADAM", "Abyssal Sire","Hydra","Barrows","Bryophyta","Callisto","Cerberus","CoX","CoX CM","Chaos Elemental","Chaos Fanatic","Zilyana",
					"Corporeal Beast","Crazy Archaeologist","Dagganoth Prime","Dagganoth Rex","Dagganoth Supreme","Deranged Archaeologist","Graardor","Giant Mole","Grotesque Guardians","Hespori","Kalphite Queen",
					"King Black Dragon","Kraken","Kree'Arra","K'ril","Mimic","Nightmare","Obor","Sarachnis","Scorpia","Skotizo", "Tempoross", "The Gauntlet","The Corrupted Gauntlet",
					"ToB","Thermonuclear","Zuk","Jad","Venenatis","Vet'ion","Vorkath","Wintertodt","Zalcano","Zulrah"]
		kcCount = ["Kills"]
		username = ' '.join([str(word) for word in name]) 
		numSkills = 23
		killcount_output = ""
		killcount_outputList = []
		async with ctx.typing():
			try:
				data=urllib.request.urlopen("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username.replace(" ", "%20"))
			except:
				await ctx.send("An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your username btw.")
			#Takes the JSON data from the url, decodes it using utf-8, throws away all information after the experience, and splits entries on newlines
			killcount_dataHolder = data.read().decode().split("\n")
			print(killcount_dataHolder)
			for index in range (numSkills+1, len(killcount_dataHolder)-1):
				holder = killcount_dataHolder[index].split(",")
				kcCount.append(holder[1])
			print(kcCount)
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
	async with ctx.typing():
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