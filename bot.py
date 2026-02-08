import os
import re
import json
import datetime
import discord
from discord.ext import commands

import gspread
from google.oauth2.service_account import Credentials

# ================= Env helpers =================
def env_int(name, default=None):
    v = os.getenv(name)
    if v is None or v.strip() == "":
        return default
    try:
        return int(v)
    except ValueError:
        return default

# ================= Discord config =================
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

LOWER_REQUEST_CHANNEL_ID = env_int("LOWER_REQUEST_CHANNEL_ID")
UPPER_REQUEST_CHANNEL_ID = env_int("UPPER_REQUEST_CHANNEL_ID")
LOWER_UPPER_LIST_CHANNEL_ID = env_int("LOWER_UPPER_LIST_CHANNEL_ID")

INCOLLE_REQUEST_CHANNEL_ID = env_int("INCOLLE_REQUEST_CHANNEL_ID")
INCOLLE_LIST_CHANNEL_ID = env_int("INCOLLE_LIST_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True

# ================= Sheets config =================
LU_SPREADSHEET_ID = os.getenv("LU_SPREADSHEET_ID")
LU_SHEET_NAME = os.getenv("LU_SHEET_NAME")
LU_TS_COLUMN_INDEX = int(os.getenv("LU_TS_COLUMN_INDEX", "1"))
LU_NAME_COL_INDEX = int(os.getenv("LU_NAME_COL_INDEX", "28"))
LU_STATUS_COL_INDEX = int(os.getenv("LU_STATUS_COL_INDEX", "29"))

LU_MENTION_SPREADSHEET_ID = os.getenv("LU_MENTION_SPREADSHEET_ID")
LU_MENTION_SHEET_NAME = os.getenv("LU_MENTION_SHEET_NAME")

INC_SPREADSHEET_ID = os.getenv("INC_SPREADSHEET_ID")
INC_SHEET_NAME = os.getenv("INC_SHEET_NAME")
INC_TS_COLUMN_INDEX = int(os.getenv("INC_TS_COLUMN_INDEX", "1"))
INC_NAME_COL_INDEX = int(os.getenv("INC_NAME_COL_INDEX", "27"))
INC_STATUS_COL_INDEX = int(os.getenv("INC_STATUS_COL_INDEX", "28"))

INC_MENTION_SPREADSHEET_ID = os.getenv("INC_MENTION_SPREADSHEET_ID")
INC_MENTION_SHEET_NAME = os.getenv("INC_MENTION_SHEET_NAME")

# ================= Sheets client =================
def make_gspread_client():
    info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds)

def open_worksheet(gc, spreadsheet_id, sheet_name):
    return gc.open_by_key(spreadsheet_id).worksheet(sheet_name)

# ================= Bot =================
class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.close()

bot = MyBot(command_prefix="!", intents=intents)
bot.run(TOKEN)
