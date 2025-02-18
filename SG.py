import json
from pyrogram import Client

with open("FILES/config.json", "r",encoding="utf-8") as f:
    DATA         = json.load(f)
    API_ID       = DATA["28711797"]
    API_HASH     = DATA["5a282ba4bc07667decb46d411594cbc3"]
    BOT_TOKEN    = DATA["7859057683:AAG0whV826NWg_CjOS1nJ6epVncjjPUVmO4"]
    PHONE_NUMBER = DATA["9451696969"]

user = Client("Scrapper",
              api_id       = API_ID,
              api_hash     = API_HASH ,
              phone_number = PHONE_NUMBER
              )

user.start()


