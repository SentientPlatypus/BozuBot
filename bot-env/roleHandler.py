import nextcord
from nextcord.ext import commands
import helper
import constants
cluster = helper.getMongo()
pointDB = cluster["discord"]["bozuPoints"]


def hasRoleByName(guild:nextcord.Guild, roleName:str) -> bool:
    allRoles = guild.fetch_roles()
    for role in allRoles:
        if role.name.lower() == roleName.lower():
            return True
    return False

def getRoleByName(guild:nextcord.Guild, roleName:str) -> nextcord.Role:
    allRoles = guild.fetch_roles()
    for role in allRoles:
        if role.name.lower() == roleName.lower():
            return role
    return None


class roleHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator= True)
    async def sortBySpreadsheet(self, ctx,
        spreadSheetName:str = "testerData",
        roleNameColHead:str = "Team Number", 
        locationColHead:str = "Team Location", 
        LevelColHead:str = "Team Skill Level",
        member1ColHead:str = "Member 1 Discord Username", 
        member2ColHead:str= "Member 2 Discord Username", 
        member3ColHead:str= "Member 3 Discord Username", 
        member4ColHead:str= "Member 4 Discord Username", 
    ):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text="Rishi yo ass better be careful before executing this one")
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        if confirm:
            groupChatCategory = await ctx.guild.create_category("Group Chats")
            recievedData = helper.getSpreadSheetData(r"C:\Users\trexx\Documents\PYTHON CODE LOL\CODEBOZU\bozuBot\bot-env\credentials.json", spreadSheetName)
            for row in recievedData:
                print(row)
                location = row[locationColHead]
                level = row[LevelColHead]


                locationRole = getRoleByName(ctx.guild, location) if hasRoleByName(ctx.guild, location) else await ctx.guild.create_role(name = location)
                levelRole = getRoleByName(ctx.guild, level) if hasRoleByName(ctx.guild, level) else await ctx.guild.create_role(name = level)



                m1 = row[member1ColHead]
                m2 = row[member2ColHead]
                m3 = row[member3ColHead]
                m4 = row[member4ColHead]
                roleName = f"Group {row[roleNameColHead]}"
                if location != "" and level != "" and m1 != "":
                    createdRole = await ctx.guild.create_role(name = roleName)
                    for memberUsername in [m1,m2,m3,m4]:
                        if memberUsername != "":
                            memberObj = ctx.guild.get_member_named(memberUsername)
                            if not memberObj:
                                continue
                            memberObj.add_roles([createdRole, locationRole, levelRole])
                    
                    overwrites = {
                        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                        createdRole: nextcord.PermissionOverwrite(read_messages = True)
                    }
                    await ctx.guild.create_text_channel(roleName, overwrites = overwrites, category= groupChatCategory)
            embed = nextcord.Embed(title = "Hopefully that worked LMAO", color = nextcord.Color.yellow())
            embed.set_image(url=constants.PRAYING_CHEEMS_IMG)
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(roleHandler(client))