import sys
from nextcord.ext import commands
import nextcord
from googleSpreadSheetReading import getSpreadSheetData
import datetime
import math
import sys
import traceback
import asyncio
##-------------HELPERS-------------------------------
import constants as constants
import helper as helper

##-------------COGS-----------------------------------
import bozuPointHandler
import roleHandler
import databaseHandler
import helpCommand




client = commands.Bot(command_prefix="!", intents =nextcord.Intents.all(), status=nextcord.Status.online)




##------------INITIALIZING COGS----------------------
bozuPointHelperCog = [bozuPointHandler]
for i in range(len(bozuPointHelperCog)):
    bozuPointHelperCog[i].setup(client)

roleHandlerCog = [roleHandler]
for i in range(len(roleHandlerCog)):
    roleHandlerCog[i].setup(client)

databaseHandlerCog = [databaseHandler]
for i in range(len(databaseHandlerCog)):
    databaseHandlerCog[i].setup(client)

helpCommandCog = [helpCommand]
for i in range(len(helpCommandCog)):
    helpCommandCog[i].setup(client)





@client.command(name = "info", help = "Gives information about Bozu!")
async def info(ctx):
    embed=nextcord.Embed(title="BozuBot Information", color=nextcord.Color.purple())
    embed.description= "Servers: %g\nMembers:%g"%(len(client.guilds), helper.getNumMembers(client))
    embed.add_field(name="Resources", value="Check [Here](https://codebozu.com)")
    embed.set_thumbnail(url=client.user.avatar)
    await ctx.channel.send(embed=embed)







@client.event
async def on_command_error(ctx, error):
    commandThatFailed = ctx.command
    embed = nextcord.Embed()
    embed.timestamp = ctx.message.created_at
    embed.set_author(icon_url=client.user.avatar, name="Command Error")
    embed.set_thumbnail(url=client.user.avatar)
    embed.color=nextcord.Color.red()
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Retry in %s"%(datetime.timedelta(seconds=math.floor(error.retry_after)))
        embed.title = "Still On Cooldown!"
        embed.description = "```%s```"%(msg)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.title = "Missing Argument!"
        embed.description = "Syntax: %s"%(helper.syntax(commandThatFailed))
        embed.set_footer(text = 'Make Sure to add "quotation marks" around a parameter that has a space!')
    elif isinstance(error, commands.BadArgument):
        embed.title="Bad Argument"
        embed.description="```%s```"%(str(error))
    elif isinstance(error, asyncio.TimeoutError):
        embed.title = "Timeout"
        embed.description= "```you took too long for that interaction, dummy.```"
    elif isinstance(error, commands.MissingPermissions):
        embed.title = "Missing Permissions"
        embed.description= "```You dont have le perms```"
    else:
        print("failed")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.channel.send(embed=embed)




@client.event
async def on_ready():
    print("--------------------------------------we out--------------------------------------")
    await helper.updatePresence(client)

@client.event
async def on_member_join(member):
    await helper.updatePresence(client)

client.run(constants.TOKEN)
