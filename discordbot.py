import discord
from discord.ext import commands
import os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzQ0MTAxNDYzNDM2ODIwNTMw.XzeUfQ.CT8t6jkhj4Kb7N_Fqk277QRmPPY'
CH_ID = 744161340725133352
discord_voice_channel_id = ''#732218077583900776

voice = None
player = None

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    channel = client.get_channel(CH_ID)

    member_id = 742193673621471262
    member = channel.guild.get_member(member_id)


    #await channel.send("密を避けるため、"f"{member.mention}を使って空気を入れ替えてください")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「/ishigo」と発言したら「」が返る処理
    if message.content == '/ishigo':
        await message.channel.send('私は今、宙に浮いている状態で...')
        
    global voich
    # 接続
    if message.content.startswith('!isgo'):
        voich = await discord.VoiceChannel.connect(message.author.voice.channel)
    # 切断
    if message.content.startswith('!isout'):
        await voich.disconnect()

    if client.user in message.mentions: # 話しかけられたかの判定
        await reply(message) # 返信する非同期関数を実行

# 返信する非同期関数を定義
async def reply(message):
    reply = f'{message.author.mention} はい？' # 返信メッセージの作成
    await message.channel.send(reply) # 返信メッセージを送信

    
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
