import os


TOKEN = "SECRET"
CMD_PREFIX = "!"

##--------------------MONGO------------------------
MONGO_PASSWORD = "SECRET"


USER_DATABASE_DEFAULTS = {
    "needsUpdate":True,
    "bozuPoints":0
}

GUILD_DATABASE_DEFAULTS = {
    "prefix":"!"
}

USER_DATABASE_PATH = os.path.join(os.path.dirname(__file__),r"./Databases/users.json")
GUILD_DATABASE_PATH = os.path.join(os.path.dirname(__file__),r"./Databases/guilds.json")
DB_CHECK_READY_PRINT = "db done"


##-------------------ASSETS----------------------
SPINNING_COIN_GIF = "https://cdn.dribbble.com/users/6257/screenshots/3833147/coin.gif"
EXCLAMATION_MARK_IMG = "https://thumbs.dreamstime.com/b/vector-pixel-exclamation-point-vector-pixel-exclamation-point-speech-buble-isolated-white-background-s-s-style-design-123217138.jpg"
PRAYING_CHEEMS_IMG = "https://i.imgflip.com/5d1e3o.png"
ERROR_EXCLAMATION_ICON = "https://flyclipart.com/thumb2/alert-danger-error-exclamation-mark-red-icon-227724.png"


DEFAULT_GROUP_CHAT_CATEGORY = "Group Chats"
DEFAULT_GROUP_CHAT_CATEGORY2 = "Group Chats 2"
DEFAULT_GROUP_CHAT_CATEGORY3 = "Group Chats 3"
