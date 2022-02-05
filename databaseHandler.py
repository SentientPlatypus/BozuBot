from nextcord.ext import commands
import nextcord
import constants as constants
import helper as helper

cluster = helper.getMongo()
pointDB = cluster["discord"]["bozuPoints"]


def checkMember(user:nextcord.Member):
    try:
        needsUpdate = pointDB.find_one({"id":user.id},{"needsUpdate"})["needsUpdate"]
    except:
        pointDB.update_one({"id":user.id}, {"$set":{"needsUpdate":True}}, True)
        needsUpdate = pointDB.find_one({"id":user.id},{"needsUpdate"})["needsUpdate"]
        print("updated %s' needUpdate to True"%(user.display_name))
    if needsUpdate:
        for x in constants.USER_DATABASE_DEFAULTS:
            try:
                value = pointDB.find_one({"id":user.id},{x["name"]})[x["name"]]
            except:
                pointDB.update_one({"id":user.id}, {"$set":{x["name"]:x["value"]}})
                print("updated %s' %s"%(user.display_name, x["name"]))
                try:
                    value = pointDB.find_one({"id":user.id},{x["name"]})[x["name"]]
                except:
                    pointDB.update_one({"id":user.id}, {"$set":{x["name"]:x["value"]}}, True)
                    print("updated %s' %s"%(user.display_name, x["name"]))     
        pointDB.update_one({"id":user.id}, {"$set":{"needsUpdate":False}})
        print("updated %s' needUpdate to False"%(user.display_name))   





class databseHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            checkMember(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        checkMember(member)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def checkGuild(self, ctx):
        guild = ctx.guild
        for member in guild.members:
            checkMember(member)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for member in guild.members:
                checkMember(member)


def setup(client):
    client.add_cog(databseHandler(client))