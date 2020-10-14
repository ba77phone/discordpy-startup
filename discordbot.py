import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzQ0MTAxNDYzNDM2ODIwNTMw.XzeUfQ.jSi4vu4h2I1_hFjs7j18ObW0UVg'
discord_voice_channel_id = ''#732218077583900776
sh_ID = 742193673621471262

# 接続に必要なオブジェクトを生成
client = discord.Client()

#----------------------------------▼

async def app():
    CH_ID = 744161340725133352
    channel = client.get_channel(CH_ID)
    
    embed = discord.Embed(title="石郷ロボ_コマンド",description="ver 0.5.4",color=0xc0f5ff)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/744375782905741342/746768531500040350/ishigou.smile.gif")
    embed.add_field(name="/ishigo",value="石郷のセリフがメッセージ送信されます",inline=False)
    embed.add_field(name="!isgo",value="ボイスチャットに入り込み特定の行動をします",inline=False)
    embed.add_field(name="!isout",value="ボイスチャットから退出します",inline=False)
    embed.add_field(name="!w (市区町村)",value="石郷が(市区町村)の天気予報を送信します\n例)!w kosigaya (=越谷の天気予報をお届け)",inline=False)
    embed.add_field(name="@石郷ロボ(メンション)",value="石郷をメッセージに呼び出します",inline=False)
    embed.add_field(name="(ver 0.5.4 パッチノート)",value="「!w」コマンドのパッチを追加しました。",inline=False)
    
    await channel.send(embed=embed)



#----------------------------------▲

#----------------------------------▼

async def weath(wether):
            #都市コードをディクショナリで保存
            citycode = {
                "misato": '3/14/4310/11237/',
                "soka": '3/14/4310/11221/',
                "kosigaya": '3/14/4310/11222/',
                "yosikawa": '3/14/4310/11243/',
                "kasukabe": '3/14/4310/11214/',
                "yasio": '3/14/4310/11234/',
                "matubusi": '3/14/4310/11465/'
            }

            weth = ''

            #tenki.jpの目的の地域のページのURL
            url = 'https://tenki.jp/forecast/' + citycode[city]
        
            #HTTPリクエスト
            r = requests.get(url)

            #HTMLの解析
            bsObj = BeautifulSoup(r.content, "html.parser")
            
            #今日の天気を取得

            today = bsObj.find(class_="today-weather")
            weather = today.p.string

            #気温情報のまとまり
            temp=today.div.find(class_="date-value-wrap")

            #気温の取得
            temp=temp.find_all("dd")
            temp_max = temp[0].span.string #最高気温
            temp_max_diff=temp[1].string #最高気温の前日比
            temp_min = temp[2].span.string #最低気温
            temp_min_diff=temp[3].string #最低気温の前日比

            #降水確率の取得
            unit = today.find_all("td")

            #結果の出力
            ms1 = ("天気:{}".format(weather))
            ms2 = ("最高気温:{: >2}℃ {}".format(temp_max,temp_max_diff))
            ms3 = ("最低気温:{: >2}℃ {}".format(temp_min,temp_min_diff))
            
            #降水確率比較用リスト
            m = [0,10,20,30,40,50,60,70,80,90,100]
            n = 0
            ok = 0

            rn = ['','','','']
            ms = ['','','','']
            ms[0] = ("--- ")
            ms[1] = ("--- ")
            ms[2] = ("--- ")
            ms[3] = ("--- ")

    
            #降水確率の出力
            for sch in unit:
                for i in m:
                    if format(sch) == '<td>'+ str(i) +'<span class="unit">%</span></td>':
                        ms[n] = ("{: >2}% ".format(str(i)))
                        ok = 1
                
                n += 1

            city_n = {
                "misato": '三郷',
                "soka": '草加',
                "kosigaya": '越谷',
                "yosikawa":'吉川',
                "kasukabe":'春日部',
                "yasio": '八潮',
                "matubusi": '松伏'
            }
                
            toshi = ('---'+city_n[city]+'の今日の天気--------')
            rn[0] = ("降水確率:"+ ms[0] +" [00:00-06:00]")
            rn[1] = ("降水確率:"+ ms[1] +" [06:00-12:00]")
            rn[2] = ("降水確率:"+ ms[2] +" [12:00-18:00]")
            rn[3] = ("降水確率:"+ ms[3] +" [18:00-24:00]")
    
            wethe = ("```\n"+toshi+'\n\n'+ms1+'\n\n'+ms2+'\n'+ms3+'\n\n'+rn[0]+'\n'+rn[1]+'\n'+rn[2]+'\n'+rn[3]+'\n'+"```")
            return wethe

#----------------------------------▲


# 60秒に一回に動作する処理-----------▼
@tasks.loop(minutes=1)
async def send_message_every_60sec():
    global city
    #指定時間に天気情報を投下
    wether = ''
    now = datetime.now().strftime('%H:%M')
    if now == '21:00':
        CH_ID = 746361807668641882
        channel = client.get_channel(CH_ID)
        city = 'misato'
        w = await weath(wether)
        await channel.send(w)
    
# 起動時に動作する処理-------------▼
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される

    #await app()

    send_message_every_60sec.start()


# メッセージ受信時に動作する処理---▼
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「/ishigo」と発言したら「」が返る処理
    if message.content == '/ishigo':
        await message.channel.send('宙に浮いている状態が続いていて...')
        

    # global sorce
    global voich
    
    # 「!isgo」だったら
    if message.content == '!isgo':
        
        # 接続
        voich = await discord.VoiceChannel.connect(message.author.voice.channel)
        
        # source = discord.FFmpegPCMAudio("doso_vol1.mp3")
        # massage.voice_client.play(source)
        
        await message.channel.send('!kuki')
        
        # await voich.disconnect()
        
    # 「!isout」で切断
    if message.content == '!isout':
        await voich.disconnect()
    
    #天気予報受送信
    if message.content.startswith('!w'):
        wether = ''
        global city
        if message.content == '!w misato':
            city = 'misato'
            w = await weath(wether)
            await message.channel.send(w)

        elif message.content == '!w soka':
            city = 'soka'
            w = await weath(wether)
            await message.channel.send(w)

        elif message.content == '!w kosigaya':
            city = 'kosigaya'
            w = await weath(wether)
            await message.channel.send(w)

        elif message.content == '!w yosikawa':
            city = 'yosikawa'
            w = await weath(wether)
            await message.channel.send(w)

        elif message.content == '!w kasukabe':
            city = 'kasukabe'
            w = await weath(wether)
            await message.channel.send(w)

        elif message.content == '!w yasio':
            city = 'yasio'
            w = await weath(wether)
            await message.channel.send(w)
            
        elif message.content == '!w matubusi':
            city = 'matubusi'
            w = await weath(wether)
            await message.channel.send(w)
            
        else :
            await message.channel.send('!isgo.error: [市区町村] is not setting')


    if client.user in message.mentions: # 話しかけられたかの判定
        await reply(message) # 返信する非同期関数を実行

# ボイスチャンネル内の状態が変化時-▼
@client.event
async def on_voice_state_update(member, before, after):
    # チャンネルを移動していない場合処理をしない
    if before.channel == after.channel:
        return
    
    # チャンネルから退出してきた場合
    if before.channel is not None:
        if member.name == '空気清浄機くん':
            await voich.disconnect()

# 返信する非同期関数を定義▼
@client.event
async def reply(message):
    reply = f'{message.author.mention} なんでしょう' # 返信メッセージの作成
    await message.channel.send(reply) # 返信メッセージを送信


    
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
