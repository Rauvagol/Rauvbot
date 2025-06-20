# coding: utf-8
import os
import discord
import urllib
import random
import math
import string
import datetime
import requests
import asyncio

from datetime import datetime, timedelta, timezone
from discord.ext import tasks, commands
from dotenv import load_dotenv

last_boopsy = None
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PASTEBIN = os.getenv('PASTEBIN_URL')
WORDS = os.getenv('WORDS').split(',')
last_results = set()  # To store the previous results for comparison
soundboard_disabled_until = None

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print("logged in2")
    #check_bfa_quests.start()
    print("BFA quest check task started.")
    print(PASTEBIN)
    print(WORDS[0])
    print(WORDS[1])
    print(WORDS[2])

@tasks.loop(minutes=15)
async def check_bfa_quests():
    global last_results
    url = 'https://www.wowhead.com/world-quests/bfa/na'
    search_strings = [
        "Swab This", "Whiplash", "Chag's Challenge", "Getting Out of Hand",
        "Revenge of Krag'wa", "Cancel the Blood Troll Apocalypse",
        "Sandfishing", "Vulpera for a Day"
    ]

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        webpage_content = response.text

        lower_content = webpage_content.lower()

        current_results = {
            quest for quest in search_strings if quest.lower() in lower_content
        }

        if current_results != last_results:
            last_results = current_results
            if current_results:
                message = "Available today for the BFA meta:\n" + "\n".join(current_results)
            else:
                message = "No quests for the BFA meta achievement are available today."

            channel_id = 522866140146434051
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
            else:
                print(f"Could not find channel with ID {channel_id}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage or process request. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in check_bfa_quests: {e}")

@bot.command(name='commands')
async def commands_command(ctx):
    def stringdecode(input_str):
        decoded_str = input_str.decode('utf-8')
        sections = decoded_str.split('\r\n\r\n')
        result_dict = {}
        for section in sections:
            lines = section.strip().split('\r\n')
            key = lines[0]
            values = lines[1:]
            result_dict[key] = values
        return result_dict
    await ctx.reply('\n'.join(stringdecode(urllib.request.urlopen(PASTEBIN).read()).keys()))


@bot.command(name='rauvbot', help='the new pastebin command storage system')
async def pastebin_command(ctx):
    def stringdecode(input_str):
        decoded_str = input_str.decode('utf-8')
        sections = decoded_str.split('\r\n\r\n')
        result_dict = {}
        for section in sections:
            lines = section.strip().split('\r\n')
            key = lines[0]
            values = lines[1:]
            result_dict[key] = values
        return result_dict
    await ctx.reply(random.choice(stringdecode(urllib.request.urlopen(PASTEBIN).read()).get(ctx.message.content.split()[-1])))


@bot.command(name='test', help='for testing')
async def test_command(ctx):
    print("running")
    await ctx.reply("Running4")


@bot.event
async def on_typing(channel, user, when):
    if user.id == 124664055251075072:
        async with channel.typing():
            print(f"{user} is typing message in {channel} {when}")
            await channel.send()


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 773416052796555264 and payload.emoji.name == "nice":
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        role = discord.utils.get(bot.get_guild(payload.guild_id).roles, name='test role')
        await message.remove_reaction(payload.emoji, payload.member)
        await message.add_reaction(payload.emoji)
        if role in payload.member.roles:
            await payload.member.remove_roles(role)
        else:
            await payload.member.add_roles(role)
    if payload.message_id == 1003780204583473202 and payload.emoji.name == "synthwave":
        print(payload)
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        role = discord.utils.get(bot.get_guild(payload.guild_id).roles, name='Synthwave Enjoyer')
        await message.remove_reaction(payload.emoji, payload.member)
        await message.add_reaction(payload.emoji)
        if role in payload.member.roles:
            await payload.member.remove_roles(role)
        else:
            await payload.member.add_roles(role)


@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel or before.channel

    if channel is not None:
        if len(channel.members) > 10 and bot.user not in channel.members:
            await channel.connect()
        elif len(channel.members) < 10 and bot.user in channel.members:
            voice_client = bot.voice_clients[0]
            await voice_client.disconnect()


@bot.event
async def on_soundboard_play(ctx):
    global soundboard_disabled_until
    if random.random() < 0.01:
        soundboard_disabled_until = datetime.now(timezone.utc) + timedelta(days=1)
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.use_soundboard = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("Soundboard disabled until tomorrow.")


@bot.event
async def on_message(message):
    global soundboard_disabled_until
    global last_boopsy

    if soundboard_disabled_until and datetime.now(timezone.utc) > soundboard_disabled_until:
        try:
            overwrite = message.channel.overwrites_for(message.guild.default_role)
            overwrite.use_soundboard = None
            await message.channel.set_permissions(message.guild.default_role, overwrite=overwrite)
            soundboard_disabled_until = None
            await message.channel.send("Soundboard permissions have been restored.")
        except discord.Forbidden:
            print(f"Missing permissions to change soundboard settings in channel {message.channel.id}")
        except Exception as e:
            print(f"Error resetting soundboard permissions: {e}")

    if message.author.bot:
        return

    target_user_id = 178624853874704384
    if message.author.id == target_user_id:
        most_recent_message = None
        now = datetime.now(timezone.utc)
        one_week_ago = now - timedelta(minutes=10080)
        
        try:
            print(f"Fetching history for user {target_user_id}...")
            print(f"Current time (UTC): {now}")
            
            # Search through channels for the most recent message before the triggering message
            for channel in message.guild.text_channels:
                if channel.permissions_for(message.guild.me).read_message_history:
                    try:
                        async for msg in channel.history(
                            limit=50,  # Lower limit since we only need the most recent message
                            oldest_first=False
                        ):
                            # Skip the triggering message
                            if msg.id == message.id:
                                continue
                                
                            if msg.author.id == target_user_id:
                                # Found the most recent message before the trigger
                                if most_recent_message is None or msg.created_at > most_recent_message[0]:
                                    most_recent_message = (msg.created_at, msg.content, channel.name)
                                break  # Exit after finding the first message in this channel
                                
                    except discord.Forbidden:
                        print(f"No permission to read history in {channel.name} (ID: {channel.id})")
                    except Exception as e:
                        print(f"Error fetching history from {channel.name} (ID: {channel.id}): {e}")

            if most_recent_message:
                timestamp, content, channel_name = most_recent_message
                print(f"Found message from {timestamp} (UTC)")
                
                # Format and send the message to the user
                ts_unix = int(timestamp.timestamp())
                safe_content = content.replace('`', '\\`')
                if len(safe_content) > 150:
                    safe_content = safe_content[:147] + "..."
                
                formatted_message = f"Your most recent message:\n<t:{ts_unix}:F> in #{channel_name}:\n`{safe_content}`"
                #await message.author.send(formatted_message)
                
                # Check if the message is older than 1 minute
                if timestamp < one_week_ago:
                    print(f"Message is older than 1 minute ({now - timestamp}), sending 'response'")
                    await message.reply("A gremlin has appeared! https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXloejV3ZTZjODFxYnZ2ZG5ocGE5Ynl1NHlldmd5NG1mYTJhNmJmcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6nWhy3ulBL7GSCvKw6/giphy.gif")
            else:
                print("No previous messages found")
                await message.reply("A gremlin has appeared! https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXloejV3ZTZjODFxYnZ2ZG5ocGE5Ynl1NHlldmd5NG1mYTJhNmJmcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6nWhy3ulBL7GSCvKw6/giphy.gif")

        except discord.Forbidden:
            print(f"Cannot send DM to user {message.author.id}. DMs might be disabled or bot is blocked.")
        except Exception as e:
            print(f"Error processing message history for user {message.author.id}: {e}")

    if message.content.startswith('```') and message.content.endswith('```'):
        lines = message.content.split('\n')
        if len(lines) > 13:
            file_path = 'code_block.txt'
            with open(file_path, 'w') as file:
                if message.content[3] == '\n':
                    file.write(message.content[4:-3])
                else:
                    file.write(message.content[3:-3])
            with open(file_path, 'rb') as file:
                await message.channel.send(content=f"{message.author.mention} posted a code block:", file=discord.File(file, file_path))
            os.remove(file_path)
            await message.delete()
        return

    if "harmlessbug" in message.author.name:
        banned_letter = random.choice(['x', 'j', 'q', 'z'] + ['ö'] * 25)
        if banned_letter in message.content.lower():
            try:
                original_content = message.content
                edited_content = original_content.replace(banned_letter, '').replace(banned_letter.upper(), '')
                await message.delete()
                await message.channel.send(
                    f"Error: banned letter detected from {message.author.mention}\n\n"
                    f"Here is the edited, Rauvbot approved™ message\n\n"
                    f"```\n{edited_content}\n```"
                )
            except discord.Forbidden:
                print(f"Missing permissions to delete/send messages in {message.channel.id} for harmlessbug logic.")
            except Exception as e:
                print(f"Error in harmlessbug logic: {e}")

    if "dstronghold" in message.author.name:
        if random.random() < 0.003:
            await message.channel.send("https://tenor.com/view/spray-bottle-cat-spray-bottle-spray-bottle-meme-loop-gif-25594440")

    if "lmao" in message.content.lower():
        emojis = ["🇱", "🇦", "🇲", "🇴"]
        try:
            for emoji in emojis:
                await message.add_reaction(emoji)
        except discord.Forbidden:
            print(f"Missing permissions to add reactions in {message.channel.id}")
            pass

    if "samsung" in message.content.lower():
        try:
            await message.channel.send("Don't order from Samsung Direct , remember what happened to Exo and Happy.")
        except discord.Forbidden:
            print(f"Missing permissions to send messages in {message.channel.id} for samsung logic.")
            pass

    cleaned_content_nice = message.content.lower().translate(str.maketrans('', '', string.punctuation)).strip()
    if cleaned_content_nice == "nice":
        try:
            nice_emoji = bot.get_emoji(870075966142185562)
            if nice_emoji:
                await message.add_reaction(nice_emoji)
            else:
                print("Could not find nice emoji (870075966142185562)")
        except discord.Forbidden:
            print(f"Missing permissions to add reactions in {message.channel.id} for nice logic.")
            pass

    cleaned_content_shutup = message.content.lower().translate(str.maketrans('', '', string.punctuation)).strip()
    if cleaned_content_shutup == "shut up" and message.author.id in [124664055251075072, 217788070068617216]:
        if random.randint(1, 10) == 1:
            try:
                await message.channel.send('lamo')
            except discord.Forbidden:
                print(f"Missing permissions to send messages in {message.channel.id} for shut up logic.")
            except Exception as e:
                print(f"Error sending lamo reply: {e}")

    if " 69 " in f" {message.content.lower()} ":
        try:
            nice_emoji = bot.get_emoji(870075966142185562)
            if nice_emoji:
                await message.add_reaction(nice_emoji)
            else:
                print("Could not find nice emoji (870075966142185562)")
        except discord.Forbidden:
            print(f"Missing permissions to add reactions in {message.channel.id} for 69 logic.")
            pass

    if "legion remix" in message.content.lower():
        try:
            await message.reply("they told us everything we need to know about legion remix\nwhen it starts\nwhen it ends \nhow leveling works\nwow tokens for killing mythic argussy\nyou can use the one button to play the entire thing\nwhich is why it was created\n(i am joking they literally said almost nothing besides it exists and small changes)")
        except discord.Forbidden:
            print(f"Missing permissions to send messages in {message.channel.id} for legion remix logic.")
            pass

    if len(WORDS) > 4 and WORDS[3] in message.content.lower():
        try:
            await message.channel.send(WORDS[4])
        except discord.Forbidden:
            print(f"Missing permissions to send messages in {message.channel.id} for WORDS[3]/[4] logic.")
            pass

    if "horde" in message.content.lower():
        if random.randint(1, 10) == 1:
            try:
                await message.reply("I'm sorry for the interruption, but I have to ask if you meant to say horse.", mention_author=False)
            except discord.Forbidden:
                print(f"Missing permissions to send messages in {message.channel.id} for horde logic.")
            except Exception as e:
                print(f"Error sending horde reply: {e}")

    if len(WORDS) > 2 and (WORDS[0] in message.content.lower() or WORDS[1] in message.content.lower() or WORDS[2] in message.content.lower()):
        last_boopsy = datetime.now(timezone.utc)
        print(f"Boopsy detected, last_boopsy set to: {last_boopsy}")
        try:
            await message.channel.send("This is a christian server, please call it a mister boopsy")
        except discord.Forbidden:
            print(f"Missing permissions to send messages in {message.channel.id} for boopsy logic.")
            pass

    elif "mister boopsy" in message.content.lower():
        if last_boopsy is not None and (datetime.now(timezone.utc) - last_boopsy < timedelta(seconds=30)):
            try:
                await message.channel.send("Thank you for using polite language in this christian server.")
            except discord.Forbidden:
                print(f"Missing permissions to send messages in {message.channel.id} for mister boopsy logic.")
            except Exception as e:
                print(f"Error sending mister boopsy message: {e}")
        else:
            print("Mister boopsy detected, but last_boopsy is None or too old.")

    await bot.process_commands(message)


@bot.command(name='10seconds', help='for when you envy the you of 10 seconds ago')
async def ten_seconds(ctx):
    await ctx.send("https://i.imgur.com/tnJtepM.jpg")


@bot.command(name='bfa', help='for the BFA meta WQ')
async def bfa(ctx):
    url = 'https://www.wowhead.com/world-quests/bfa/na'
    search_strings = [
        "Swab This", "Whiplash", "Chag's Challenge", "Getting Out of Hand",
        "Revenge of Krag'wa", "Cancel the Blood Troll Apocalypse",
        "Sandfishing", "Vulpera for a Day"
    ]
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        webpage_content = response.text

        lower_content = webpage_content.lower()

        available_quests = [
            quest for quest in search_strings if quest.lower() in lower_content
        ]

        message = "Available today for the BFA meta:\n" + "\n".join(available_quests)

    except requests.exceptions.RequestException as e:
        message = f"Failed to retrieve the webpage. Error: {e}"

    channel = bot.get_channel(522866140146434051)
    if channel:
        await channel.send(message)
    else:
        await ctx.send("Failed to find the specified channel.")


@bot.command(name='checkgames', help='Check if Steam games are good')
async def checkgames(ctx):
    game_ids = [216150, 1056640, 1599340, 582660, 2074920]
    game_data_list = []

    async with ctx.typing():
        for game_id in game_ids:
            try:
                details_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
                details_response = requests.get(details_url)

                if details_response.status_code == 200:
                    game_data = details_response.json()
                    if game_data and game_data.get(str(game_id), {}).get('success', False):
                        game_name = game_data[str(game_id)]['data']['name']
                    else:
                        game_name = f"Game {game_id}"
                else:
                    game_name = f"Game {game_id}"

                reviews_url = f"https://store.steampowered.com/appreviews/{game_id}?json=1&language=all&purchase_type=all&num_per_page=0"
                overall_data = requests.get(reviews_url).json()

                histogram_url = f"https://store.steampowered.com/appreviewhistogram/{game_id}?l=english"
                histogram_data = requests.get(histogram_url).json()

                if 'query_summary' in overall_data and 'results' in histogram_data:
                    recent_data = histogram_data['results']['recent']
                    recent_positive = sum(day['recommendations_up'] for day in recent_data)
                    recent_negative = sum(day['recommendations_down'] for day in recent_data)
                    recent_total = recent_positive + recent_negative
                    recent_percent = (recent_positive / recent_total * 100) if recent_total > 0 else 0

                    overall_summary = overall_data['query_summary']
                    overall_positive = overall_summary['total_positive']
                    overall_total = overall_summary['total_reviews']
                    overall_percent = (overall_positive / overall_total * 100) if overall_total > 0 else 0

                    difference = recent_percent - overall_percent

                    game_data_list.append({
                        'id': game_id,
                        'name': game_name,
                        'difference': difference,
                        'recent_percent': recent_percent,
                        'recent_total': recent_total,
                        'overall_percent': overall_percent,
                        'overall_total': overall_total
                    })
                else:
                    game_data_list.append({
                        'name': game_name,
                        'difference': float('-inf'),
                        'error': 'No review data available'
                    })

            except Exception as e:
                game_data_list.append({
                    'name': game_name,
                    'difference': float('-inf'),
                    'error': str(e)
                })

            await asyncio.sleep(1)

        game_data_list.sort(key=lambda x: x['difference'], reverse=True)

        summary = ""
        for game in game_data_list:
            if 'error' in game:
                summary += f"**{game['name']}**: {game['error']}\n\n"
            else:
                difference = game['difference']
                if difference > 0:
                    if difference < 5:
                        emoji = "🔼"
                    else:
                        check_count = (difference // 5)
                        emoji = "✅" * int(check_count)
                elif difference < 0:
                    if abs(difference) < 5:
                        emoji = "🔽"
                    else:
                        x_count = (abs(difference) // 5)
                        emoji = "❌" * int(x_count)
                else:
                    emoji = ""

                summary += f"[**{game['name']}**](<https://store.steampowered.com/app/{game['id']}>) {emoji}\n"
                summary += f"Recent: {game['recent_percent']:.1f}% positive ({game['recent_total']:,} reviews)\n"
                summary += f"Overall: {game['overall_percent']:.1f}% positive ({game['overall_total']:,} reviews)\n"
                summary += f"Difference: {difference:+.1f}%\n\n"

        await ctx.send(summary)


@bot.command(name='breakup', help='for serious conversations')
async def breakup(ctx):
    await ctx.send(
        "Babe :baby::sob:, i'm :cupid: breaking :hammer: up :arrow_up: with you :point_left_tone2:. it's not you "
        ":point_left::no_entry_sign:, you :point_left: were poggers :sunglasses::nail_care:. it's me, i'm :cupid: "
        "omegalul :crying_cat_face::person_frowning:. im :cupid: sorry :person_bowing: if this is pepehands "
        ":palms_up_together: but :thinking: it has to be done :hammer:, i've :person_raising_hand_tone1: just been "
        "feeling :grin: pepega and our relationship :couple: has been weirdchamp :scream_cat: for months "
        ":calendar_spiral:, it's time :clock1: to end :end: it, no :persevere: kappa "
        ":stuck_out_tongue_closed_eyes::zany_face::kissing_heart:")


@bot.command(name='modabuse', help="change user's nickname given id and new nickname")
async def modabuse(ctx, victim_id: int, newname):
    if victim_id == 106205285760135168:
        await ctx.send("No can do boss. Discord doesn't let me opress the server owner.")
    victim = await ctx.guild.fetch_member(victim_id)
    await victim.edit(nick=newname)
    await ctx.send("Done")


@bot.command(name='rockgolem', help='makes htg happy')
async def rockgolem(ctx):
    await ctx.send("he done it with 27,758,267 exp!")


@bot.command(name='beaver', help='makes htg sad')
async def beaver(ctx):
    await ctx.send("he done it with 60,052,138  exp!")


@bot.command(name='rslevels', help='takes osrs username as a parameter and gives stats on levels')
async def rslevels(ctx, *name):
    def get_hiscores(runescape_username):
        total_experience = [0, 0, 0, 0]
        try:
            total_experience[0] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on normal hiscores")
            pass
        try:
            total_experience[1] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on ironman hiscores")
            pass
        try:
            total_experience[2] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on hardcore ironman hiscores")
            pass
        try:
            total_experience[3] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on ultimate ironman hiscores")
            pass
        print(total_experience)
        print(max(total_experience))
        if total_experience[3] == max(total_experience):
            print("uim")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        elif total_experience[2] == max(total_experience):
            print("hcim")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        elif total_experience[1] == max(total_experience):
            print("im")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        else:
            print("normie")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + runescape_username.replace(" ", "%20")).read().decode().split("\n")

    experience_for_level = [-1, 0]
    skill_name = ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:",
                  "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:",
                  "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:",
                  "Hunter:", "Construction:"]
    skill_level = ["Level"]
    skill_experience = ["Experience"]
    skill_missing_experience = ["Missing Experience", "Irrelevantlol"]
    exptotal = 0
    output_list = []
    async with ctx.typing():
        for index in range(2, 100):
            experience_for_level.append(
                experience_for_level[index - 1] + (math.floor(index - 1 + 300 * 2 ** ((index - 1) / 7)) / 4))
        for index in range(len(experience_for_level)):
            experience_for_level[index] = math.floor(experience_for_level[index])
        username = ' '.join([str(word) for word in name])
        try:
            data_holder = get_hiscores(username)
        except urllib.error.HTTPError:
            await ctx.send(
                "An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your "
                "username btw.")
            return
        for index in range(len(skill_name) - 1):
            holder = data_holder[index].split(",")
            skill_level.append(holder[1])
            skill_experience.append(holder[2])
            if index > 0:
                exptotal += min(13034431, int(holder[2]))
                skill_missing_experience.append(13034431 - min(13034431, int(holder[2])))
        for index in range(len(skill_level)):
            if skill_level[index] == "69":
                skill_level[index] = "Nice."
        level_spacer_one = "═".ljust(len(max(skill_name, key=len)), "═")
        level_spacer_two = "═".ljust(len(max(skill_level, key=len)), "═")
        level_spacer_three = "═".ljust(len(max(skill_experience, key=len)), "═")
        exptotal = int(exptotal)
        percent_to_99s = round(100 * exptotal / 299791913, 2)
        table_width = 12 + len(level_spacer_one + level_spacer_two + level_spacer_three)
        header = " ╔═" + level_spacer_one + "═══" + level_spacer_two + "═══" + level_spacer_three + "═╗\n" + " ║ " + "Stats for " + username + "║".rjust(table_width - len(" ║ " + "Stats for " + username) - 1) + "\n" + " ╠═" + level_spacer_one + "═╦═" + level_spacer_two + "═╦═" + level_spacer_three + "═╣\n" + " ║ " + skill_name[0].ljust(len(level_spacer_one)) + " ║ " + skill_level[0].rjust(len(level_spacer_two)) + " ║ " + skill_experience[0].rjust(len(level_spacer_three)) + " ║\n" + " ╠═" + level_spacer_one + "═╬═" + level_spacer_two + "═╬═" + level_spacer_three + "═╣\n"
        footer = " ╠═" + level_spacer_one + "═╩═" + level_spacer_two + "═╩═" + level_spacer_three + "═╣\n" + " ║ Adjusted total EXP = " + str(exptotal) + "║".rjust(table_width - len(" ║ Adjusted total EXP = " + str(exptotal)) - 1) + "\n" + " ║ " + str(percent_to_99s) + "% of the way to all skills 99" + "║".rjust(table_width - len(" ║ " + str(percent_to_99s) + "X of the way to all skills 99") - 1) + "\n" + " ╚═" + level_spacer_one + "═══" + level_spacer_two + "═══" + level_spacer_three + "═╝\n"
        for index in range(len(skill_name)):
            if index > 0:
                output_list.append(
                    " ║ " + skill_name[index].ljust(len(level_spacer_one)) + " ║ " + skill_level[index].rjust(
                        len(level_spacer_two)) + " ║ " + skill_experience[index].rjust(
                        len(level_spacer_three)) + " ║\n")
    await ctx.send("```" + header + "".join(output_list) + footer + "```")


@bot.command(name='hiscores', help='takes osrs username as a parameter and gives stats on hiscore ranks')
async def hiscores(ctx, *name):
    def get_hiscores(runescape_username):
        total_experience = [0, 0, 0, 0]
        try:
            total_experience[0] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on normal hiscores")
            pass
        try:
            total_experience[1] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on ironman hiscores")
            pass
        try:
            total_experience[2] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on hardcore ironman hiscores")
            pass
        try:
            total_experience[3] = int(urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")[0].split(",")[2])
        except urllib.error.HTTPError:
            print("Not on ultimate ironman hiscores")
            pass
        print(total_experience)
        print(max(total_experience))
        if total_experience[3] == max(total_experience):
            print("uim")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        elif total_experience[2] == max(total_experience):
            print("hcim")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        elif total_experience[1] == max(total_experience):
            print("im")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player=" +
                runescape_username.replace(" ", "%20")).read().decode().split("\n")
        else:
            print("normie")
            return urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + runescape_username.replace(" ", "%20")).read().decode().split("\n")

    experience_for_level = [-1, 0]
    skill_name = ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:",
                  "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:",
                  "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:",
                  "Hunter:", "Construction:"]
    skill_level = ["Rank"]
    skill_experience = ["Experience"]
    skill_missing_experience = ["Missing Experience", "Irrelevantlol"]
    exptotal = 0
    output_list = []
    async with ctx.typing():
        for index in range(2, 100):
            experience_for_level.append(
                experience_for_level[index - 1] + (math.floor(index - 1 + 300 * 2 ** ((index - 1) / 7)) / 4))
        for index in range(len(experience_for_level)):
            experience_for_level[index] = math.floor(experience_for_level[index])
        username = ' '.join([str(word) for word in name])
        try:
            data_holder = get_hiscores(username)
        except urllib.error.HTTPError:
            await ctx.send(
                "An error occurred, probably a 404, but what do I know? I just work here. Check the spelling of your "
                "username btw.")
            return
        for index in range(len(skill_name) - 1):
            holder = data_holder[index].split(",")
            print(holder)
            skill_level.append(holder[0])
            skill_experience.append(holder[2])
            if index > 0:
                exptotal += min(13034431, int(holder[2]))
                skill_missing_experience.append(13034431 - min(13034431, int(holder[2])))
        output_temp = []
        calculated_holder = []
        for index in range(len(skill_name)):
            if index > 1 and skill_missing_experience[index] > 0:
                calculated_holder.append("".join(expcalc(skill_missing_experience[index], index)))
        try:
            longest_skill_todo = max(calculated_holder, key=len)
        except urllib.error.HTTPError:
            if username == "himtheguy":
                await ctx.send("https://youtu.be/LDU_Txk06tM?t=75")
        longest_skill = -1
        for index in range(len(calculated_holder)):
            if len(calculated_holder[index]) == len(longest_skill_todo):
                longest_skill = index
        rs99_spacer_one = "═".ljust(len(max(skill_name, key=len)), "═")
        rs99_spacer_two = "═".ljust(len(max(calculated_holder, key=len)), "═")
        associated_skill = []
        for index in range(len(skill_name)):
            if index > 1 and skill_missing_experience[index] > 0:
                holder = "".join(expcalc(skill_missing_experience[index], index))
                associated_skill.append(skill_name[index])
                output_temp.append(" ║ " + skill_name[index].ljust(len(rs99_spacer_one)) + " ║ " + holder.rjust(
                    len(rs99_spacer_two)) + " ║\n")
        print(associated_skill)
        print(calculated_holder)
        header = " ╔═" + rs99_spacer_one + "═╦═" + rs99_spacer_two + "═╗\n" + " ║ " + "Skill Name".ljust(
            len(rs99_spacer_one)) + " ║ " + "To Do:".ljust(
            len(rs99_spacer_two)) + " ║\n" + " ╠═" + rs99_spacer_one + "═╬═" + rs99_spacer_two + "═╣\n"
        footer = " ╚═" + rs99_spacer_one + "═╩═" + rs99_spacer_two + "═╝\n"
    try:
        await ctx.send("```" + header + "".join(output_temp) + footer + "```")
    except discord.errors.HTTPException:
        await ctx.send(
            "Error, to-do list too long, work on " + associated_skill[longest_skill][:-1] + ", requiring " + calculated_holder[longest_skill])


@bot.command(name='rs99', help='takes osrs username as a parameter and gives stats on levels')
async def rs99(ctx, *name):
    async with ctx.typing():
        def expcalc(missing_experience, skill_id):
            def recursivecalc(activity_brackets, experience_brackets, experience_rate_brackets, loops, remaining_time_recursive, total_remaining_time):
                while loops > 0:
                    remaining_time_recursive.append(str(round((experience_brackets[len(experience_brackets) - loops] - experience_brackets[len(experience_brackets) - (loops + 1)]) / experience_rate_brackets[len(experience_rate_brackets) - loops], 2)) + activity_brackets[len(experience_brackets) - loops])
                    total_remaining_time = total_remaining_time + round((experience_brackets[len(experience_brackets) - loops] - experience_brackets[len(experience_brackets) - (loops + 1)]) / experience_rate_brackets[len(experience_rate_brackets) - loops], 2)
                    loops = loops - 1
                return remaining_time_recursive

            skill_name_temp = ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:", "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:", "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:", "Runecraft:", "Hunter:", "Construction:"]
            for level_number in range(2, 100):
                experience_for_level.append(
                    experience_for_level[level_number - 1] + (math.floor(level_number - 1 + 300 * 2 ** ((level_number - 1) / 7)) / 4))
            for level_number in range(len(experience_for_level)):
                experience_for_level[level_number] = math.floor(experience_for_level[level_number])
            current_level = 0
            remaining_brackets = 0
            for level_number in range(len(experience_for_level)):
                if experience_for_level[level_number + 1] > experience_for_level[99] - missing_experience:
                    current_level = level_number
                    break
            experience_brackets_lazy = []
            level_brackets_lazy = []
            activity_brackets_lazy = []
            experience_rate_brackets_lazy = []
            if skill_id < 7:
                activity_brackets_lazy = [" ", " ammonite crab kills."]
                level_brackets_lazy = [1, 99]
                experience_rate_brackets_lazy = [400]
                if skill_id == 5:
                    experience_rate_brackets_lazy = [133.33]
            elif skill_id == 7:
                activity_brackets_lazy = [" ", " hours of offering Big Bones at the Gilded Altar."]
                level_brackets_lazy = [1, 99]
                experience_rate_brackets_lazy = [133875]
            elif skill_id == 8:
                activity_brackets_lazy = [" ", " hours of Lvl-1 enchanting and ", " hours of Lvl-2 enchanting and ",
                                          " hours of Lvl-3 enchanting and ", " hours of High Alching."]
                level_brackets_lazy = [1, 27, 49, 55, 99]
                experience_rate_brackets_lazy = [28000, 59200, 94400, 78000]
            elif skill_id == 9:
                activity_brackets_lazy = [" ", " hours of cooking shrimp and ", " hours of cooking trout and ",
                                          " hours of cooking salmon and ", " hours of cooking karambwan."]
                level_brackets_lazy = [1, 15, 25, 35, 99]
                experience_rate_brackets_lazy = [35000, 85000, 110000, 250000]
            elif skill_id == 10:
                activity_brackets_lazy = [" ", " hours of normal trees and ", " hours of oaks and ",
                                          " hours of willows and ", " hours of unmanipulated teaks."]
                level_brackets_lazy = [1, 15, 30, 35, 99]
                experience_rate_brackets_lazy = [10000, 40000, 40000, 90000]
            elif skill_id == 11:
                activity_brackets_lazy = [" ", " hours of Arrow Shafts and ", " hours of Unstrung Longbows and ",
                                          " hours of Unstrung Oak Shortbows and ",
                                          " hours of Unstrung Oak Longbows and ",
                                          " hours of Unstrung Willow Shortbows and ",
                                          " hours of Unstrung Willow Longbows and ",
                                          " hours of Unstrung Maple Shortbows and ",
                                          " hours of Unstrung Maple Longbows and ",
                                          " hours of Unstrung Yew Shortbows and ",
                                          " hours of Unstrung Yew Longbows and ",
                                          " hours of Unstrung Magic Shortbows and ",
                                          " hours of Unstrung Magic Longbows."]
                level_brackets_lazy = [1, 10, 20, 25, 35, 40, 50, 55, 65, 70, 80, 85, 99]
                experience_rate_brackets_lazy = [9000, 17000, 28050, 42500, 56525, 70550, 85000, 99025, 114750, 127500,
                                                 141100, 155550]
            elif skill_id == 12:
                activity_brackets_lazy = [" ", " hours of Shrimp fishing, and ", " hours of Trout fly fishing, and ",
                                          " hours of Drift Net fishing."]
                level_brackets_lazy = [1, 20, 47, 99]
                experience_rate_brackets_lazy = [1500, 25000, 75000]
            elif skill_id == 13:
                activity_brackets_lazy = [" ", " hours of burning normal logs and ",
                                          " hours of burning oak logs and ", " hours of burning willow logs and ",
                                          " hours of burning maple logs."]
                level_brackets_lazy = [1, 15, 30, 45, 99]
                experience_rate_brackets_lazy = [59400, 89100, 133650, 200475]
            elif skill_id == 14:
                activity_brackets_lazy = [" ", " hours of making leather gloves and ",
                                          " hours of making leather chaps and ", " hours of cutting sapphires and ",
                                          " hours of cutting emeralds and ", " hours of cutting rubies and ",
                                          " hours of cutting diamonds and ",
                                          " hours of making fire battlestaffs and ",
                                          " hours of making air battlestaffs and ",
                                          " hours of making red d'hide bodies and ",
                                          " hours of making black d'hide bodies."]
                level_brackets_lazy = [1, 18, 20, 27, 34, 43, 62, 66, 77, 84, 99]
                experience_rate_brackets_lazy = [26000, 50000, 145000, 175000, 230000, 290000, 306000, 336000, 386000,
                                                 425000]
            elif skill_id == 15:
                activity_brackets_lazy = [" ", " hours of forging bronze daggers and ",
                                          " hours of forging bronze scimitars and ",
                                          " hours of forging bronze warhammers and ",
                                          " hours of forging bronze platebodies and ",
                                          " hours of forging iron warhammers and ",
                                          " hours of forging iron platebodies and ",
                                          " hours of forging steel warhammers and ",
                                          " hours of making gold bars in the blast furnace."]
                level_brackets_lazy = [1, 5, 9, 18, 24, 33, 39, 40, 99]
                experience_rate_brackets_lazy = [13900, 25700, 36200, 52100, 72300, 104200, 108500, 300000]
            elif skill_id == 16:
                activity_brackets_lazy = [" ", " hours of mining copper or tin ore and ",
                                          " hours of mining iron ore and ", " hours of Motherlode Mine."]
                level_brackets_lazy = [1, 15, 30, 99]
                experience_rate_brackets_lazy = [5000, 45000, 40000]
            elif skill_id == 17:
                activity_brackets_lazy = [" ", " hours of making attack potions and ",
                                          " hours of making guam tar and ", " hours of making marrentill tar and ",
                                          " hours of making tarromin tar and ", " hours of making harralander tar."]
                level_brackets_lazy = [1, 19, 31, 39, 44, 99]
                experience_rate_brackets_lazy = [62500, 61000, 86000, 110000, 145000]
            elif skill_id == 18:
                activity_brackets_lazy = [" ", " hours of gnome stronghold agility course and ",
                                          " hours of Draynor Village rooftop course and ",
                                          " hours of Varrock rooftop course and ",
                                          " hours of Canifis rooftop course and ",
                                          " hours of Seers' Village rooftop course and ",
                                          " hours of Rellekka village rooftop course and ",
                                          " hours of Ardougne rooftop course."]
                level_brackets_lazy = [1, 10, 30, 40, 60, 80, 90, 99]
                experience_rate_brackets_lazy = [8000, 9000, 13200, 19500, 52000, 54000, 61000]
            elif skill_id == 19:
                activity_brackets_lazy = [" ", " hours of pickpocketing normies and ",
                                          " hours of stealing from baker's stalls and ",
                                          " hours of stealing from fruit stalls and ",
                                          " hours of ~~suffering~~ blackjacking bearded bandits and ",
                                          " hours of stealing artefacts."]
                level_brackets_lazy = [1, 5, 25, 45, 49, 99]
                experience_rate_brackets_lazy = [5000, 19200, 33000, 60000, 160000]
            elif skill_id == 20:
                activity_brackets_lazy = [" ", " hours of violence."]
                level_brackets_lazy = [1, 99]
                experience_rate_brackets_lazy = [60000]
            elif skill_id == 21:
                activity_brackets_lazy = [" ", " hours of raking weeds (don't do this) and ",
                                          " hours of tithe farming Golovanova and ",
                                          " hours of tithe farming Bologano and ",
                                          " hours of tithe farming Logavano."]
                level_brackets_lazy = [1, 34, 54, 74, 99]
                experience_rate_brackets_lazy = [8000, 28273, 65970, 108380]
            elif skill_id == 22:
                activity_brackets_lazy = [" ", " hours of crafting tiaras and ", " hours of crafting smoke runes."]
                level_brackets_lazy = [1, 15, 99]
                experience_rate_brackets_lazy = [40000, 50000]
            elif skill_id == 23:
                activity_brackets_lazy = [" ", " regular birdhouses and ", " oak birdhouses and ",
                                          " willow birdhouses and ", " teak birdhouses and ",
                                          " maple birdhouses and ", " mahogany birdhouses and ",
                                          " yew birdhouses and ", " magic birdhouses and ", " redwood birdhouses."]
                level_brackets_lazy = [5, 14, 24, 34, 44, 49, 59, 74, 89, 99]
                experience_rate_brackets_lazy = [280, 420, 560, 700, 820, 960, 1020, 1140, 1200]
            elif skill_id == 24:
                activity_brackets_lazy = [" ", " hours of regular planks and ", " hours of oak planks."]
                level_brackets_lazy = [1, 15, 99]
                experience_rate_brackets_lazy = [29, 60]
            remaining_time = []
            if "activity_brackets_lazy" in locals():
                for level_number in range(len(level_brackets_lazy)):
                    experience_brackets_lazy.append(experience_for_level[level_brackets_lazy[level_number]])
                for level_number in range(len(level_brackets_lazy)):
                    if current_level < level_brackets_lazy[level_number + 1]:
                        experience_brackets_lazy.pop(0)
                        experience_brackets_lazy.insert(level_number, experience_for_level[99] - missing_experience)
                        remaining_brackets = len(level_brackets_lazy) - (level_number + 1)
                        break
                return (recursivecalc(activity_brackets_lazy, experience_brackets_lazy, experience_rate_brackets_lazy,
                                      remaining_brackets, remaining_time, 0))
            return str(missing_experience)

        experience_for_level = [-1, 0]
        skill_name = ["Skill Name", "Total:", "Attack:", "Defence:", "Strength:", "Hitpoints:", "Ranged:", "Prayer:",
                      "Magic:", "Cooking:", "Woodcutting:", "Fletching:", "Fishing:", "Firemaking:", "Crafting:",
                      "Smithing:", "Mining:", "Herblore:", "Agility:", "Thieving:", "Slayer:", "Farming:",
                      "Runecraft:", "Hunter:", "Construction:"]
        skill_level = ["Level"]
        skill_experience = ["Experience"]
        skill_missing_experience = ["Missing Experience", "Irrelevantlol"]
        for index in range(2, 100):
            experience_for_level.append(
                experience_for_level[index - 1] + (math.floor(index - 1 + 300 * 2 ** ((index - 1) / 7)) / 4))
        for index in range(len(experience_for_level)):
            experience_for_level[index] = math.floor(experience_for_level[index])
        username = ' '.join([str(word) for word in name])
        try:
            data = urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + username.replace(" ", "%20"))
        except urllib.error.HTTPError:
            await ctx.send(
                "An error occurred, probably a 404, but what do I know? I just work here. "
                "Check the spelling of your username btw.")
            return
        for index in range(len(skill_name) - 1):
            holder = data.read().decode().split("\n")[index].split(",")
            skill_level.append(holder[1])
            skill_experience.append(holder[2])
            if index > 0:
                skill_missing_experience.append(13034431 - min(13034431, int(holder[2])))
        output_temp = []
        calculated_holder = []
        for index in range(len(skill_name)):
            if index > 1 and skill_missing_experience[index] > 0:
                calculated_holder.append("".join(expcalc(skill_missing_experience[index], index)))
        try:
            longest_skill_todo = max(calculated_holder, key=len)
        except urllib.error.HTTPError:
            if username == "himtheguy":
                await ctx.send("https://youtu.be/LDU_Txk06tM?t=75")
        longest_skill = -1
        for index in range(len(calculated_holder)):
            if len(calculated_holder[index]) == len(longest_skill_todo):
                longest_skill = index
        rs99_spacer_one = "═".ljust(len(max(skill_name, key=len)), "═")
        rs99_spacer_two = "═".ljust(len(max(calculated_holder, key=len)), "═")
        associated_skill = []
        for index in range(len(skill_name)):
            if index > 1 and skill_missing_experience[index] > 0:
                holder = "".join(expcalc(skill_missing_experience[index], index))
                associated_skill.append(skill_name[index])
                output_temp.append(" ║ " + skill_name[index].ljust(len(rs99_spacer_one)) + " ║ " + holder.rjust(
                    len(rs99_spacer_two)) + " ║\n")
        print(associated_skill)
        print(calculated_holder)
        header = " ╔═" + rs99_spacer_one + "═╦═" + rs99_spacer_two + "═╗\n" + " ║ " + "Skill Name".ljust(
            len(rs99_spacer_one)) + " ║ " + "To Do:".ljust(
            len(rs99_spacer_two)) + " ║\n" + " ╠═" + rs99_spacer_one + "═╬═" + rs99_spacer_two + "═╣\n"
        footer = " ╚═" + rs99_spacer_one + "═╩═" + rs99_spacer_two + "═╝\n"
    try:
        await ctx.send("```" + header + "".join(output_temp) + footer + "```")
    except discord.errors.HTTPException:
        await ctx.send(
            "Error, to-do list too long, work on " + associated_skill[longest_skill][:-1] + ", requiring " + calculated_holder[longest_skill])


@bot.command(name="rskc", help='takes osrs username as a parameter and gives stats on kill counts')
async def rskc(ctx, *name):
    kc_name = ["Name", "", "", "BH - Hunter", "BH - Rogue", "BH (Legacy) - Hunter", "BH (Legacy) - Rogue",
               "Clue Scrolls (Total)", "Beginner Clues", "Easy Clues", "Medium Clues", "Hard Clues", "Elite Clues", "Master Clues",
               "LMS - Rank", "PVP Arena - Rank", "Soul Wars - Zeal", "Rifts Closed", "Colosseum Glory",
               "Abyssal Sire", "Alchemical Hydra", "Artio", "Barrows", "Bryophyta",
               "Callisto", "Calvar'ion", "Cerberus", "CoX", "CoX CM", "Chaos Elemental", "Chaos Fanatic", "Zilyana",
               "Corporeal Beast", "Crazy Archaeologist", "Dagganoth Prime", "Dagganoth Rex", "Dagganoth Supreme",
               "Deranged Archaeologist", "Duke Sucellus", "Graardor", "Giant Mole", "Grotesque Guardians", "Hespori",
               "Kalphite Queen",
               "King Black Dragon", "Kraken", "Kree'Arra", "K'ril", "Lunar Chests", "Mimic", "Nex", "Nightmare", "Phosani's Nightmare", "Obor",
               "Phantom Muspah", "Sarachnis",
               "Scorpia", "Scurrius", "Skotizo", "Sol Heredit", "Spindel", "Tempoross", "The Gauntlet", "The Corrupted Gauntlet",
               "The Leviathan", "The Whisperer",
               "ToB", "ToB - Hard Mode", "Thermonuclear", "ToA", "ToA - Expert Mode", "Zuk", "Jad", "Vardorvis", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano",
               "Zulrah"]
    kc_count = ["Kills"]
    username = ' '.join([str(word) for word in name])
    num_skills = 23
    killcount_output_list = []
    async with ctx.typing():
        try:
            data = urllib.request.urlopen(
                "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + username.replace(" ", "%20"))
        except urllib.error.HTTPError:
            await ctx.send(
                "An error occurred, probably a 404, but what do I know? I just work here. "
                "Check the spelling of your username btw.")
            return
        killcount_data_holder = data.read().decode().split("\n")
        print(killcount_data_holder)
        for index in range(num_skills + 1, len(killcount_data_holder) - 1):
            holder = killcount_data_holder[index].split(",")
            kc_count.append(holder[1])
        print(kc_count)
        killcount_spacer_one = "═".ljust(len(max(kc_name, key=len)), "═")
        killcount_spacer_two = "═".ljust(len(max(kc_count, key=len)), "═")
        killcount_table_width = 9 + len(killcount_spacer_one + killcount_spacer_two)
        killcount_header = " ╔═" + killcount_spacer_one + "═══" + killcount_spacer_two + "═╗\n" + " ║ " + "KC for " + username + "║".rjust(
            killcount_table_width - len(
                " ║ " + "KC for " + username) - 1) + "\n" + " ╠═" + killcount_spacer_one + "═╦═" + killcount_spacer_two + "═╣\n" + " ║ " + kc_name[0].ljust(len(killcount_spacer_one)) + " ║ " + kc_count[0].rjust(
            len(killcount_spacer_two)) + " ║\n" + " ╠═" + killcount_spacer_one + "═╬═" + killcount_spacer_two + "═╣\n"
        killcount_footer = " ╚═" + killcount_spacer_one + "═╩═" + killcount_spacer_two + "═╝\n"
        for index in range(len(kc_name)):
            if index > 0 and int(kc_count[index]) > 0:
                killcount_output_list.append(
                    " ║ " + kc_name[index].ljust(len(killcount_spacer_one)) + " ║ " + kc_count[index].rjust(
                        len(killcount_spacer_two)) + " ║\n")
    stringtosend = killcount_header + "".join(killcount_output_list) + killcount_footer
    print(stringtosend)
    arraytosend = stringtosend.splitlines(True)
    print(arraytosend)
    finalstring = "```"
    for line in arraytosend:
        finalstring += line
        print(finalstring)
        if len(finalstring) > 1800:
            await ctx.send(finalstring + "```")
            finalstring = "```"
    await ctx.send(finalstring + "```")


@bot.command(name='generate', help="takes a width and height parameter and generates a neat random thing")
async def generator(ctx, width, height):
    width = int(width)
    height = int(height)
    success = 0
    async with ctx.typing():
        if width < 2 or height < 2:
            success = 1
            await ctx.send("Too small, lol.")
        if ((height - 1) + width * height) > 1994:
            success = 1
            await ctx.send("Message length limit says no. ((height-1)+width*height) must be less than 1994.")
        while success == 0:
            output_array = [["X" * width] * height]
            for row in range(height):
                for column in range(width):
                    if row == 0:
                        if column == 0:
                            output_array[row][column] = random.choice("╔ ")
                        elif output_array[row][column - 1] in "╔╦╠╬╚╩═":
                            if column < width - 1:
                                output_array[row][column] = random.choice("╦╗═")
                            else:
                                output_array[row][column] = "╗"
                        elif output_array[row][column - 1] in " ╗╣╝║":
                            if column < width - 1:
                                output_array[row][column] = random.choice(" ╔")
                            else:
                                if output_array[row][column - 2] in "╔╦╠╬╚╩═":
                                    output_array[row][column - 1] = "╦"
                                else:
                                    output_array[row][column - 1] = "╔"
                                output_array[row][column] = "╗"
                    elif 0 < row < height - 1:
                        if column == 0:
                            if output_array[row - 1][column] in "╔╦╗╠╬╣║":
                                output_array[row][column] = random.choice("║╠╚")
                            elif output_array[row - 1][column] in "╚╩╝═ ":
                                output_array[row][column] = random.choice("╔ ")
                        elif output_array[row - 1][column] in "╔╦╗╠╬╣║":
                            if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                output_array[row][column] = random.choice("╬╣╩╝")
                            elif output_array[row][column - 1] in "╗╣╝║ ":
                                output_array[row][column] = random.choice("╠╚║")
                        elif output_array[row - 1][column] in "╚╩╝═ ":
                            if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                output_array[row][column] = random.choice("╦╗═")
                            elif output_array[row][column - 1] in "╗╣╝║ ":
                                output_array[row][column] = random.choice("╔")
                        if column == width - 1:
                            if output_array[row - 1][column] in "╔╦╗╠╬╣║":
                                if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                    output_array[row][column] = random.choice("╣╝")
                                    success = 1
                                elif output_array[row][column - 1] in "╗╣╝║ ":
                                    success = 0
                            elif output_array[row - 1][column] in "╚╩╝═ ":
                                if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                    success = 0
                                elif output_array[row][column - 1] in "╗╣╝║ ":
                                    output_array[row][column] = random.choice(" ")
                                    success = 1
                    elif row == height - 1:
                        if column == 0:
                            if output_array[row - 1][column] in "╔╦╗╠╬╣║":
                                output_array[row][column] = "╚"
                            elif output_array[row - 1][column] in "╚╩╝═ ":
                                output_array[row][column] = " "
                        elif output_array[row - 1][column] in "╔╦╗╠╬╣║":
                            if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                output_array[row][column] = random.choice("╝╩")
                            elif output_array[row][column - 1] in "╗╣╝║ ":
                                output_array[row][column] = random.choice("╚")
                        elif output_array[row - 1][column] in "╚╩╝═ ":
                            if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                output_array[row][column] = random.choice("═")
                            elif output_array[row][column - 1] in "╗╣╝║ ":
                                output_array[row][column] = random.choice(" ")
                        if column == width - 1:
                            if output_array[row - 1][column] in "╔╦╗╠╬╣║":
                                if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                    output_array[row][column] = random.choice("╝")
                                    success = 1
                                elif output_array[row][column - 1] in "╗╣╝║ ":
                                    success = 0
                            elif output_array[row - 1][column] in "╚╩╝═ ":
                                if output_array[row][column - 1] in "╔╦╠╬╚╩═":
                                    success = 0
                                elif output_array[row][column - 1] in "╗╣╝║ ":
                                    output_array[row][column] = random.choice(" ")
                                    success = 1
        output_holder = []
        for row in output_array:
            output_holder.append("".join(map(str, row)))
            output_holder.append("\n")
        print("".join(output_holder))
    await ctx.send("```" + "".join(output_holder) + "```")


bot.run(TOKEN)
