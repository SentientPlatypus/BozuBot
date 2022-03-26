import nextcord
from nextcord.ext import commands
import helper
import constants
import databaseHandler
import json




def getBozuPoints( user:nextcord.Member):
    return databaseHandler.getUserValue(user, "bozuPoints")

async def updatebozuPoints(guild:nextcord.Guild, user:nextcord.Member, amountToIncrementBy):
    """INCREMENTS BozuPoints. TO SET BozuPoints, user set bozuPoints"""
    databaseHandler.incrementUserValue(user, "bozuPoints", amountToIncrementBy)

async def setbozuPoints(guild:nextcord.Guild, user:nextcord.Member, amountTOincrementBY):
    databaseHandler.updateUserValue(user, "bozuPoints", 0)


class bozuPointHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command(name = "awardMember", help = "Awards a member the specified amount of bozu points")
    @commands.has_permissions(administrator = True)
    async def awardMember(self, ctx, user:nextcord.Member, amountOfBozuPoints:int):
        await updatebozuPoints(ctx.guild, user, amountOfBozuPoints)

        embed = nextcord.Embed(
            title = f"{user.display_name} has been awarded {amountOfBozuPoints} bozu Points!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{user.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command(name = "awardRole", help = "Awards all members who have the specified role the specified amount of bozu points")
    @commands.has_permissions(administrator = True)
    async def awardRole(self, ctx, role:nextcord.Role, amountOfBozuPoints:int):
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                await updatebozuPoints(ctx.guild, member, amountOfBozuPoints)


        embed = nextcord.Embed(
            title = f"Members of {role.name} have been awarded {amountOfBozuPoints} bozu Points!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{role.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command(name = "points", help = "displays the bozu points a user has")
    async def points(self, ctx, p:nextcord.Member = None):
        if not p:
            p = ctx.author
        
        points = getBozuPoints(p)

        embed = nextcord.Embed(title = f"{p.display_name}'s Bozu points!", color = nextcord.Color.green())
        embed.add_field(name = "Bozu Points:", value = f"```{points}BP```")
        embed.set_author(name = p.display_name, icon_url=p.avatar)
        embed.set_thumbnail(url = constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        await ctx.channel.send(embed = embed)


    @commands.command(name = "leaderboard", aliases = ["lb"],help = "displays top BozuPoint holders")
    async def leaderboard(self, ctx, limit:int=10):
        with open(constants.USER_DATABASE_PATH, "r") as read:
            dictionary = json.load(read)
            sortedIdDictionary = {k:v for k, v in sorted(dictionary["users"].items(), key=lambda item:-item[1]["bozuPoints"])}
        i=1
        embed = nextcord.Embed(title = "BozuPoint Leaderboard", color = ctx.author.color)
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        rankings = sortedIdDictionary.keys()
        for x in rankings:
            try:
                temp = ctx.guild.get_member(int(x)).display_name
                tempSC = sortedIdDictionary[x]["bozuPoints"]
                embed.add_field(name = f"{i}: {temp}", value = f"`{tempSC} BozuPoint`", inline = False) 
                i+=1
                if i > limit:
                    break
            except:
                pass

        await ctx.channel.send(embed=embed)


    @commands.command(name = "resetBozuPoints", help = "resets ALL bozu points to 0")
    @commands.has_permissions(administrator = True)
    async def resetBozuPoints(self, ctx):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.ERROR_EXCLAMATION_ICON)
        embed.timestamp = ctx.message.created_at
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        if confirm:
            rankings = databaseHandler.getDictionary()
            guild:nextcord.Guild = ctx.guild
            async for member in guild.fetch_members(limit=None):
                await setbozuPoints(ctx.guild, member, 0)

            embed=nextcord.Embed(
                title = f"{ctx.author.display_name} has reset bozuPoints!", 
                description = "@here", color = nextcord.Color.blue(), 
                )
            embed.set_thumbnail(url = constants.ERROR_EXCLAMATION_ICON)
            embed.timestamp =ctx.message.created_at
            await ctx.channel.send(embed=embed)



    


def setup(client):
    client.add_cog(bozuPointHandler(client))