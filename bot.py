import os
import re
import datetime
import discord
from discord.ext import commands

# ========= 設定 =========
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

REQUEST_CHANNEL_ID = 1133259695671488603
REQUEST_LIST_CHANNEL_ID = 1467530008518983968

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

# ========= 依頼文解析 =========
def extract_request_info(text):
    lines = text.splitlines()

    # 日付（MM/DD）
    date_str = "??/??"
    m = re.search(r'日時[:：]\s*(\d{4})/(\d{2})/(\d{2})', text)
    if m:
        date_str = f"{m.group(2)}/{m.group(3)}"

    # 名前
    name = "不明"
    m = re.search(r'生徒No\d+・(.+?)・', text)
    if m:
        name = m.group(1)

    # ルール・ブキ
    rule = "未定"
    weapon = "未定"
    m = re.search(r'\d+・(.+?)・.+?・(.+)', text)
    if m:
        rule = m.group(1)
        weapon = m.group(2)

    # 指導方法
    method = "未記載"
    for i, line in enumerate(lines):
        if "【希望の指導方法】" in line and i + 1 < len(lines):
            method = lines[i + 1].strip()
            break

    return name, date_str, rule, weapon, method

# ========= 一覧生成 =========
async def create_request_list_embed(bot):
    channel = bot.get_channel(REQUEST_CHANNEL_ID)
    if not channel:
        return None

    embed = discord.Embed(
        title="📘 指導依頼一覧",
        color=0x4caf50
    )

    async for msg in channel.history(limit=50):
         # システムメッセージ除外（スレッド開始通知など）
        if msg.type != 0:
            continue
        # ② Webhook 以外の投稿は除外
    if msg.webhook_id is None:
        continue

        # 👍 が付いていたら除外
        if any(r.emoji == "👍" for r in msg.reactions):
            continue

        name, date_str, rule, weapon, method = extract_request_info(msg.content)

        embed.add_field(
            name=f"■ {name} {date_str}メモプ依頼",
            value=(
                f"│ {rule}/{weapon}/{method}\n"
                f"└ 🔗 [依頼文を開く]({msg.jump_url})"
            ),
            inline=False
        )

    if not embed.fields:
        embed.description = "現在、対応待ちの指導依頼はありません。"

    embed.set_footer(
        text=f"更新: {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%H:%M')}"
    )
    return embed

# ========= Bot本体 =========
class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.update_list()
        await self.close()

    async def update_list(self):
        channel = self.get_channel(REQUEST_LIST_CHANNEL_ID)
        if not channel:
            return

        embed = await create_request_list_embed(self)

        async for msg in channel.history(limit=10):
            if msg.author == self.user and msg.embeds:
                await msg.edit(embed=embed)
                return

        await channel.send(embed=embed)

bot = MyBot(command_prefix="!", intents=intents)
bot.run(TOKEN)


