import nextcord
from nextcord.ext import commands
import helper
import constants
cluster = helper.getMongo()
pointDB = cluster["discord"]["bozuPoints"]
class roleHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(roleHandler(client))