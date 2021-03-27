import discord
from discord.ext import commands, tasks
from discord import Member, Embed
from discord.ext.commands import cooldown, BucketType
from discord.utils import get
import os
from akinator.async_aki import Akinator
import akinator
import requests
import json
import aiohttp
import random
import asyncio
import sqlite3
from datetime import datetime
from typing import Optional
from discord.ext.commands import has_permissions, MissingPermissions, BadArgument

intents = discord.Intents().all()
client = commands.Bot(command_prefix="=",
                      case_insensitive=True,
                      intents=intents)

emoji = '⚽'
emoji1 = '🆔'
emoji2 = '❌'
emoji3 = 'ℹ️'


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + "\n\n -" + json_data[0]["a"]
    return (quote)


@client.listen()
async def on_message(message):
    authorperms = message.author.permissions_in(message.channel)
    if str(message.channel) == "feedback" and message.content != "":
        if authorperms.manage_messages:
            return
        else:
            await message.channel.purge(limit=1)


def convertToMinutesSeconds(seconds):
    sec = seconds % 60
    sec = int(sec)
    min = seconds // 60
    min = int(min)
    f = {'minutes': min, 'seconds': sec}
    return f


# @client.listen()
# async def on_message(message):
# if str(message.channel) == 'archive' and message.author in message.mentions:
#    member = message.author
#   role = discord.utils.get(message.guild.roles, name="Lord")
#  await member.add_roles(role)


@client.event
async def on_member_join(member):
    channel = client.get_channel(811944290406105122)
    embed = discord.Embed(
        title="Welcome",
        description=
        f'Hey {member.mention}, Welcome to our Humble **__{member.guild.name}__**! We are still making some effort in this server to make it better but you can enjoy at the mean time!\n Have Fun and we are happy with your presence among us',
        color=discord.Colour.blue())
    await channel.send(embed=embed)
    embed = discord.Embed(
        title=f'Welcome to {member.guild.name} Server!',
        description=
        '**__Welcome to our Server, :classical_building: PES Mobile Empire :classical_building:!__** \n\n :large_blue_diamond: Make sure you read the Server rules in <#746610509666713630> Channel! \n\n :large_orange_diamond: Also do not forget to check the Tournaments rules in <#746765578143924434> \n\n :large_blue_diamond: Also do not miss out joining our tournaments by checking the latest Tournament announced in <#766946275857006612>! \n\n :large_orange_diamond: Last but not least, Have fun chatting in <#746757671675363449> and Bragging your pulls :star_struck:  in <#746758651213119498> And Asking for Team Advices in <#746757899312693278>! \n\n :large_blue_diamond: And Eventually, Have Fun!',
        color=discord.Colour.green())

    await member.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.watching,
                                     name="The Tournament"))

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS konami(
            user_id TEXT,
            channel_id TEXT,
            konami_id TEXT
        )
    ''')


print("bot on")


# BAN Command
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.ban(member, reason=reason)
    await member.send(f'You have been BANNED from **PES Mobile Empire**')
    embed = discord.Embed(
        title="Ban Case",
        description=
        f"**{member.mention} has been BANNED from **PES Mobile Empire!**",
        colour=discord.Colour.red())
    await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'{ctx.author.mention} , You are Unauthorized to Run this Command because You are Missing the **__BAN MEMBERS__** Permission!')
        print(
            f'{ctx.author.name} {ctx.author.id} do not have Permission to use this command')


# role removing
@client.command(aliases=["-role", "removerole"])
@has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Removed {role.mention} from {member.mention}!')
    print(f'Removed {role.mention} from {member.mention}!')


# MUTE Command
@client.command(pass_context=True)
async def mute(ctx, member: discord.Member, time: int, d, *, reason=None):
    role = discord.utils.get(member.server.roles, name='Muted')
    await ctx.add_roles(member, role)
    embed = discord.Embed(title="User Muted!",
                          description="**{0}** was muted by **{1}**!".format(
                              member, ctx.message.author),
                          color=0xff00f6)
    await ctx.send(embed=embed)

    if d == "s":
        await asyncio.sleep(time)

    if d == "m":
        await asyncio.sleep(time * 60)

    if d == "h":
        await asyncio.sleep(time * 60 * 60)

    if d == "d":
        await asyncio.sleep(time * 60 * 60 * 24)

        await member.remove_roles(role)

        embed = discord.Embed(title="Unmute Case! ",
                              description=f"Unmuted! -{member.mention} ",
                              colour=discord.Colour.blue())
        await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def friendly(ctx):
    msg = await ctx.send(
        f'<@&744075658463936563>, {ctx.author.mention} is asking for a friendly! React with :soccer: to Accept their Challenge!')

    await msg.add_reaction(emoji)
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji3)

    def check(reaction, user):
        return not user.bot and str(reaction.emoji) == emoji

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=600.0, check=check)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
    else:
        await ctx.send(f"<@{ctx.message.author.id}> , {user.mention} has accepted the challenge!")

    def check(reaction, user):
        return not user.bot and str(reaction.emoji) == emoji1
    try:
       reaction, user = await client.wait_for('reaction_add', timeout=600.0, check=check)

    except asyncio.TimeoutError:
      await msg.clear_reactions()
    else:
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT konami_id FROM konami WHERE user_id = {user.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.send('Id not set yet!')
        else:
            await ctx.send(result[0])


    def check(reaction, user):
       return not user.bot and str(reaction.emoji) == emoji3


    try:
       reaction, user = await client.wait_for('reaction_add', timeout=600.0, check=check)
    except asyncio.TimeoutError:
       await msg.clear_reactions()
    else:
       await user.send(f" Reacting with {emoji} makes you accept the challenge!\n\n Reacting with {emoji1} returns the Command User Konami ID!\n\n Reacting with {emoji3} returns this Guide in the DM (Direct Messages)!\n\n Reacting with {emoji2} Terminates the Friendly Command!")





@friendly.error
async def friendly_error(ctx, error):
    print('error', error)
    if isinstance(error, commands.CommandOnCooldown):
        tm = convertToMinutesSeconds(error.retry_after)
        embed = discord.Embed(title="Command on Cooldown!",
                              description='Please try again in {min} minutes and {sec} seconds'.format(
                                  min=tm['minutes'], sec=tm['seconds']), color=discord.Colour.green())
        await ctx.send(embed=embed)


# KICK Command
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await member.send(
        f'You have been kicked out of **PES Mobile Empire** by {ctx.message.author.mention}'
    )
    embed = discord.Embed(
        title="Kick Case",
        description=
        f"**{member.mention} has been kicked out of the guild(server)!**",
        colour=discord.Colour.gold())
    await ctx.send(embed=embed)
    print(f'User {member} has been kicked out of the guild')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'{ctx.author.mention} , You are Unauthorized to Run this Command because You are Missing the **__KICK MEMBERS__** Permission!'
        )
        print(
            f'{ctx.author.name} {ctx.author.id} do not have Permission to use this command'
        )


# PURGE Command
@client.command(name="clear", aliases=["purge", "delete", "del"])
@has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: Optional[int] = 1):
    if 0 < limit <= 100:
        await ctx.channel.purge(limit=limit)
        msg = await ctx.send('Deleted the required messages!')
        await asyncio.sleep(2)
        await msg.delete()
    else:
        await ctx.send("The Limit provided is Invalid!")


@clear_messages.error
async def clear_messages_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'{ctx.author.mention} , You are Unauthorized to Run this Command because You are Missing the **__MANAGE MESSAGES__** Permission!'
        )
        print(
            f'{ctx.author.name} {ctx.author.id} do not have Permission to use this command'
        )
    else:
        raise (error)


# 8BALL Command
@client.command(aliases=['8ball'])
async def _8ball(ctx, sentence=None):
    responses = [
        "**It is certain**", "**It is decidedly so**", "**Without a doubt**",
        "**Yes, definitely**", "**You may rely on it**",
        "**As I see it, yes**", "**Most likely**", "**Outlook good**",
        "**Yes**", "**Signs point to yes**", "**Reply hazy, try again**",
        "**Ask again later**", "**Better not tell you now**",
        "**Cannot predict now**", "**Concentrate and ask again**",
        "**Don't count on it**", "**My reply is no**", "**My sources say no**",
        "**Outlook not so good**", "**Very doubtful**"
    ]
    await ctx.send(random.choice(responses))


@client.command(aliases=["av", "pfp"])
async def avatar(ctx, *, avamember: discord.Member = None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)


@client.command(aliases=["random", "match"])
async def ran(ctx, home, away):
    numbers = ["1", "2", "3", "4", "5"]
    embed = discord.Embed(title="Random Match Result Generator",
                          colour=discord.Colour.green())
    embed.add_field(name="**__Home__**", value=f'{home}', inline=True)
    embed.add_field(
        name="**__Score__**",
        value=f' **{random.choice(numbers)} - {random.choice(numbers)} **')
    embed.add_field(name="**__Away__**", value=f'{away}', inline=True)
    await ctx.send(embed=embed)


@client.command()
async def quote(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)


@client.command(aliases=["serverinfo", "server info", "si", "sim"])
async def _sim(ctx):
    name = str(ctx.guild.name)
    region = str(ctx.guild.region)
    description = "A PES Mobile Server for All the PES Mobile Knights out there!"
    id = str(ctx.guild.id)
    owner = ":crown: World Class Noob#2244"
    channels = ctx.guild.text_channels
    v_channels = ctx.guild.voice_channels

    member = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " " + "**__SERVER INFORMATION__**",
                          description=description,
                          colour=discord.Colour.gold(),
                          timestamp=datetime.utcnow())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="**OWNER**", value=owner, inline=True)
    embed.add_field(name="**SERVER ID**", value=id, inline=True)
    embed.add_field(name="**REGION**", value=region, inline=True)
    embed.add_field(name="**CREATED AT**",
                    value=ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=True)
    embed.add_field(name="**MEMBERS**", value=member, inline=True)
    embed.add_field(name="**BANNED MEMBERS**",
                    value=len(await ctx.guild.bans()),
                    inline=True)
    embed.add_field(name="**CATEGORIES**",
                    value=len(ctx.guild.categories),
                    inline=True)
    embed.add_field(name="**TEXT CHANNELS**", value=len(channels), inline=True)
    embed.add_field(name="**VOICE CHANNELS**",
                    value=len(v_channels),
                    inline=True)
    embed.add_field(name="**INVITES**",
                    value=len(await ctx.guild.invites()),
                    inline=True)

    await ctx.send(embed=embed)


@client.command(aliases=["member info", "user info", "userinfo"])
async def ui(ctx, member: discord.Member):
    embed = discord.Embed(title="User information",
                          colour=discord.Colour.red(),
                          timestamp=datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="**Name**", value=str(member), inline=True)
    embed.add_field(name="**ID**", value=member.id, inline=True)
    embed.add_field(name="**Bot?**", value=member.bot, inline=True)
    embed.add_field(name="**Top Role**",
                    value=member.top_role.mention,
                    inline=True)
    embed.add_field(name="**Status**",
                    value=str(member.status).title(),
                    inline=True)
    embed.add_field(name="**Created At**",
                    value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=True)
    embed.add_field(name="**Joined At**",
                    value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=True)
    embed.add_field(name="Boosted",
                    value=bool(member.premium_since),
                    inline=True)
    await ctx.send(embed=embed)


@client.command()
async def draft(ctx):
    Choices = [
        "**__Italy__**", "**__Spain__**", "**__Belgium__**", "**__Brazil__**",
        " **__Netherlands__**", "**__Germany__**", "**__Uruguay__**",
        "**__Portugal__**", "**__England__**", "**__Argentina__**",
        "**__France__**", "**__Croatia__**"
    ]
    embed = discord.Embed(title="My Draft", color=0x00ff00)
    embed.add_field(name="Nation No.1", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.2", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.3", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.4", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.5", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.6", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.7", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.8", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.9", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.10", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.11", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.12", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.13", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.14", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.15", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.16", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.17", value=f'{random.choice(Choices)}', inline=False)
    embed.add_field(name="Nation No.18", value=f'{random.choice(Choices)}', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def h(ctx):
    embed = discord.Embed(
        title="Help Page",
        description=
        "To view a Command, write the Command and help. \n For example, =serverinfo help",
        colour=discord.Colour.red())
    embed.add_field(name="h", value="This Page!", inline=False)
    embed.add_field(name="Moderation Commands", value=chr(173), inline=False)
    embed.add_field(name="purge", value="=purge help", inline=False)
    embed.add_field(name="mute", value="=mute help", inline=False)
    embed.add_field(name="kick", value="=kick help", inline=False)
    embed.add_field(name="ban", value="=ban help", inline=False)
    embed.add_field(name="addrole", value="=addrole help", inline=False)
    embed.add_field(name="removerole", value="=removerole help", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def add(ctx, identity):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(
        f"SELECT konami_id FROM konami WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO konami (user_id, konami_id) VALUES(?,?)")
        val = (ctx.author.id, int(identity))
        await ctx.send(f" ID saved!")
    elif result is not None:
        sql = ("UPDATE konami SET konami_id = ? WHERE user_id = ?")
        val = (int(identity), ctx.author.id)
        await ctx.send(f"ID Updated!")
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Id must be an Integer!")


@client.command()
async def id(ctx, user: discord.Member):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT konami_id FROM konami WHERE user_id = {user.id}")
    result = cursor.fetchone()
    if result is None:
        await ctx.send('Id not set yet!')
    else:
        await ctx.send(result[0])


@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                'https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            await ctx.send(res['data']['children'][random.randint(
                0, 25)]['data']['url'])


@client.command()
async def roleinfo(ctx, role: discord.Role):
    rolename = role.name
    roleid = role.id
    rolecolour = role.colour
    hoisted = role.hoist
    mentionable = role.mentionable
    position = role.position
    createdat = role.created_at
    rolemembers = " ".join([i.mention for i in role.members])
    mention = role.mention

    embed = discord.Embed(title=f'{rolename}',
                          description=chr(173),
                          color=discord.Colour.green())
    embed.add_field(name="Role Id", value=roleid, inline=False)
    embed.add_field(name="Role Colour", value=rolecolour, inline=False)
    embed.add_field(name="Hoisted?", value=hoisted, inline=False)
    embed.add_field(name="Mentionable?", value=mentionable, inline=False)
    embed.add_field(name="Role Position", value=position, inline=False)
    embed.add_field(name="Created At", value=createdat, inline=False)
    embed.add_field(name="Role Members", value=rolemembers, inline=False)
    embed.add_field(name="Role Mention", value=mention, inline=False)
    await ctx.send(embed=embed)




@client.command(name="akinator", aliases=["aki"])
async def akinator_game(ctx):
    aki = Akinator()
    first = await ctx.send("Processing...")
    q = await aki.start_game()

    game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q,
                               url=r"https://en.akinator.com/", color=discord.Color.blurple())
    game_embed.set_footer(text=f"Wait for the bot to add reactions before you give your response.")

    option_map = {'✅': 'y', '❌': 'n', '🤷‍♂️': 'p', '😕': 'pn', '⁉️': 'i'}
    """You can pick any emojis for the responses, I just chose what seemed to make sense.
      '✅' -> YES, '❌'-> NO, '🤷‍♂️'-> PROBABLY YES, '😕'-> PROBABLY NO, '⁉️'->IDK, '😔'-> force end game, '◀️'-> previous question"""

    def option_check(reaction, user):  # a check function which takes the user's response
        return user == ctx.author and reaction.emoji in ['◀', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']

    count = 0
    while aki.progression <= 80:  # this is aki's certainty level on an answer, per say. 80 seems to be a good number.
        if count == 0:
            await first.delete()  # deleting the message which said "Processing.."
            count += 1

        game_message = await ctx.send(embed=game_embed)

        for emoji in ['◀️', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']:
            await game_message.add_reaction(emoji)

        option, _ = await client.wait_for('reaction_add', check=option_check)  # taking user's response
        if option.emoji == '😔':  # there might be a better way to be doing this, but this seemed the simplest.
            return await ctx.send("Game ended.")
        async with ctx.channel.typing():
            if option.emoji == '◀️':  # to go back to previous question
                try:
                    q = await aki.back()
                except:  # excepting trying-to-go-beyond-first-question error
                    pass
                # editing embed for next question
                game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q,
                                           url=r"https://en.akinator.com/", color=discord.Color.blurple())
                continue
            else:
                q = await aki.answer(option_map[option.emoji])
                # editing embed for next question
                game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q,
                                           url=r"https://en.akinator.com/", color=discord.Color.blurple())
                continue

    await aki.win()

    result_embed = discord.Embed(title="My guess....", colour=discord.Color.dark_blue())
    result_embed.add_field(name=f"My first guess is **{aki.first_guess['name']}**",
                           value=aki.first_guess['description'], inline=False)
    result_embed.set_footer(text="Was I right? Add the reaction accordingly.")
    result_embed.set_image(url=aki.first_guess['absolute_picture_path'])
    result_message = await ctx.send(embed=result_embed)
    for emoji in ['✅', '❌']:
        await result_message.add_reaction(emoji)

    option, _ = await client.wait_for('reaction_add', check=option_check, timeout=15)
    if option.emoji == '✅':
        final_embed = discord.Embed(title="I'm a genius", description= "Had Fun Plying with You!", color=discord.Color.green())
    elif option.emoji == '❌':
        final_embed = discord.Embed(title="Oof", description="Maybe try again?", color=discord.Color.red())
        # this does not restart/continue a game from where it was left off, but you can program that in if you like.

    return await ctx.send(embed=final_embed)





client.run('NzY2MDAxNTYxMjE3NTMxOTM2.X4dAiw.rB-ac3cQUVzcMExgO_i-tnX1Fb8')
