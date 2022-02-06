import nextcord
from nextcord.ext import commands
import helper
import constants

cluster = helper.getMongo()
pointDB = cluster["discord"]["bozuPoints"]

class bozuPointHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    @commands.has_permissions(administrator = True)
    async def awardMember(self, ctx, user:nextcord.Member, amountOfBozuPoints:int):
        pointDB.update_one({"id":user.id}, {"$inc":{"bozuPoints":amountOfBozuPoints}})

        embed = nextcord.Embed(
            title = f"{user.display_name} has been awarded {amountOfBozuPoints} bozu Points!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{user.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def awardRole(self, ctx, role:nextcord.Role, amountOfBozuPoints:int):
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                pointDB.update_one({"id":member.id}, {"$inc":{"bozuPoints":amountOfBozuPoints}})

        embed = nextcord.Embed(
            title = f"Members of {role.name} have been awarded {amountOfBozuPoints} bozu Points!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{role.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def points(self, ctx, p:nextcord.Member = None):
        if not p:
            p = ctx.author
        
        points = pointDB.find_one({"id":p.id}, {"bozuPoints"})["bozuPoints"]

        embed = nextcord.Embed(title = f"{p.display_name}'s Bozu points!", color = nextcord.Color.green())
        embed.add_field(name = "Bozu Points:", value = f"```{points}BP```")
        embed.set_author(name = p.display_name, icon_url=p.avatar)
        embed.set_thumbnail(url = constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        await ctx.channel.send(embed = embed)


    @commands.command()
    async def leaderboard(self, ctx):
        rankings = pointDB.find().sort("bozuPoints",-1)
        i=1
        embed = nextcord.Embed(title = "Bozu Point Leaderboard", color = ctx.author.color)
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        for x in rankings:
            try:
                temp = ctx.guild.get_member(int(x["id"])).display_name
                tempBP = x["bozuPoints"]
                embed.add_field(name = f"{i}: {temp}", value = f"Bozu points: `{tempBP}BP`", inline = False) 
                i+=1
                if i==11:
                    break
            except:
                pass
        await ctx.channel.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def resetBozuPoints(self, ctx):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
        embed.timestamp = ctx.message.created_at
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        if confirm:
            rankings = pointDB.find().sort("bozuPoints",-1)
            for x in rankings:
                pointDB.update_one({"id":x["id"]}, {"$set":{"bozuPoints":0}})
            embed=nextcord.Embed(
                title = f"{ctx.author.display_name} has reset bozu points!", 
                description = "@here", color = nextcord.Color.blue(), 
                )
            embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
            embed.timestamp =ctx.message.created_at
            await ctx.channel.send(embed=embed)



    


def setup(client):
    client.add_cog(bozuPointHandler(client))