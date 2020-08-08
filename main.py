import discord
from discord.ext import commands
import json
import traceback
import os
import logging
import asyncio
import datetime
from discord.ext import tasks
import sys

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix="ya!")
bot.remove_command("help")
bot.load_extension("jishaku")

@bot.command()
async def help(ctx,arg=None):
    if arg is None:
      e = discord.Embed(title="也電botのヘルプ",description="也電botは、yaakiyu#9012が一人で開発する多機能(を目指す)botです。",color=0xff0000)
      e.add_field(name="コマンド一覧",value="`help`,`info`,`say`,`emsay`,`userinfo`,`serverinfo`,`getid`,`timenow`,`follow`,`nofollow`")
      e.set_footer(text="「ya!help [コマンド名]」でコマンドごとの詳細なヘルプが見えます。")
    else:
      helpco = {
        "help":"ヘルプコマンドです。",
        "info":"このbotに関する情報を出せます。",
        "say":"botにしゃべってもらえます。",
        "emsay":"botに埋め込みでしゃべってもらえます。",
        "userinfo":"実行したユーザーの情報を表示できます。\n`ya!userinfo [ユーザーID]`でそのIDの情報を表示することもできます。",
        "serverinfo":"実行したサーバーの情報を表示できます。",
        "getid":"サーバー、実行者、チャンネルなどのIDを取得できます。",
        "timenow":"現在の時間を表示できます。"
      }
      if arg in helpco:
        e=discord.Embed(title="コマンド詳細ヘルプ",description=helpco[arg])
        e.set_footer(text="コマンド名の前には「ya!」を入れてください。")
      else:
        e=discord.Embed(title="うーん...",description=f"{arg}というコマンドは存在しません。`ya!help`で調べてみてください。")
    await ctx.send(embed=e)

@bot.command()
async def info(ctx):
  e=discord.Embed(title="也電botについて",description="botの説明です。",color=0x4db56a)
  e.add_field(name="作成者",value="yaakiyu#9012")
  e.add_field(name="バージョン",value="0.15")
  e.add_field(name="サーバー数", value=f"{len(bot.guilds)}")
  e.add_field(name="ユーザー数", value=f"{len(bot.users)}")
  e.add_field(name="招待リンク", value="https://discord.com/oauth2/authorize?client_id=717715949977075782&scope=bot&permissions=2146959351 \n権限はほとんどいりません。(メッセージの管理権限と基本権限のみ必要)")
  await ctx.send(embed=e)

@bot.command()
async def say(ctx,arg,arg2=None):
  if ctx.guild.id == 573911193127747608:
    if arg2 is None:
      await ctx.send(arg)
    elif int(arg2) < 6:
      s = 0
      while s < int(arg2):
        await ctx.send(arg)
        s = s + 1
    else:
      await ctx.send("しゃべる回数は5回以下にしてください！")
  else:
    if "<@" in arg or "@everyone" in arg or "@here" in arg:
      await ctx.send("メンションはしないでください。")
    else:
      await ctx.send(arg)

@bot.command()
async def emsay(ctx,*,arg):
  await ctx.send(embed=discord.Embed(description=arg))

@bot.command()
async def timenow(ctx):
  await ctx.send(f"現在は、{datetime.datetime.now()}です")

@bot.command(aliases=["ui"])
async def userinfo(ctx,arg=None):
  if arg is None:
    sl = bot.get_user(ctx.author.id)
    e=discord.Embed(title=f"{sl.name}の情報",description="あなたの情報を表示しています。")
    e.add_field(name="名前",value=sl.name)
    e.add_field(name="ID",value=str(sl.id))
    e.add_field(name="アイコンのURL",value=sl.avatar_url)
    e.add_field(name="bot?",value=sl.bot)
    e.set_footer(text=f"アカウント作成日時(イギリス標準時):{sl.created_at}")
  else:
    sl = await bot.fetch_user(int(arg))
    e=discord.Embed(title=f"{sl.name}の情報",description="その人の情報です")
    e.add_field(name="名前",value=sl.name)
    e.add_field(name="ID",value=str(sl.id))
    e.add_field(name="アイコンのURL",value=sl.avatar_url)
    e.add_field(name="bot?",value=sl.bot)
    e.set_footer(text=f"アカウント作成日時(イギリス標準時):{sl.created_at}")
  await ctx.send(embed=e)

@bot.command(aliases=["si","sinfo"])
async def serverinfo(ctx,arg=None):
  if arg is None:
    server = ctx.guild
    e=discord.Embed(title="サーバー検索",description=f"{server.name}の情報を表示しています")
    e.add_field(name="名前",value=server.name)
    e.add_field(name="ID",value=str(server.id))
  else:
    server = await bot.fetch_guild(arg)
    e=discord.Embed(title="サーバー検索",description=f"{server.name}の情報を表示しています")
    e.add_field(name="名前",value=server.name)
    e.add_field(name="ID",value=str(server.id))
  await ctx.send(embed=e)

@tasks.loop(seconds=20)
async def loop():
  await bot.get_channel(740738263588929577).send("::t")
  def ch(m):
    return m.channel.id == 740738263588929577 and m.author.id == 695288604829941781
  msg = await bot.wait_for('message', check=ch)
  if "ログイン" in msg.embeds[0].description:
    await asyncio.sleep(5)
    await msg.channel.send("::login")
  else:
    def co(m):
      return m.channel.id == 740738263588929577 and m.author.id == 664790025040429057
    ms = await bot.wait_for('message', check=co)
    await asyncio.sleep(1)
    await ms.channel.send(ms.content)

@bot.command()
async def getid(ctx):
  await ctx.send(f"IDを表示します。\nサーバーID:{ctx.guild.id}\nユーザーID:{ctx.author.id}\nチャンネルID:{ctx.channel.id}\nコマンドを打ったメッセージのID:{ctx.message.id}")

@bot.command()
async def follow(ctx):
  global datas
  if ctx.author:
    if ctx.channel.id in datas["newsf"]:
      await ctx.send("このチャンネルはすでにお知らせ登録されています！")
    elif ctx.channel == discord.DMChannel:
      await ctx.send("DMでお知らせを登録しないでください！")
    else:
      datas["newsf"].append(ctx.channel.id)
      with open("bot/data.json",mode="w") as f:
        json.dump(datas,f,indent=4)
      await ctx.send(embed=discord.Embed(title="完了！",description="お知らせチャンネルの登録が完了しました。\n解除したい場合は`ya!nofollow`をこのチャンネルで実行してください。"))
  else:
    await ctx.send(embed=discord.Embed(title="エラー",description="あなたには`チャンネルの管理`権限が足りません！"))

@bot.command()
async def nofollow(ctx):
  global datas
  try:
    datas["newsf"].remove(ctx.channel.id)
    with open("bot/data.json",mode="w") as f:
      json.dump(datas,f,indent=4)
    await ctx.send("チャンネルのお知らせ登録を削除しました。")
  except ValueError:
    await ctx.send(embed=discord.Embed(title="エラー",description="このチャンネルはお知らせを受け取るように設定されていません！"))

@bot.command()
async def welcome(ctx,arg,arg2=None):
  global datas
  if arg == "channel":
    if arg2 == "here" or arg2 is None:
      datas[ctx.guild.id]["wel"]["channel"] = ctx.channel.id
      with open("bot/data.json",mode="w") as f:
        json.dump(datas,f,indent=4)
      await ctx.send("チャンネルの登録に成功しました。")
    else:
      try:
        print(ctx.guild.get_channel(int(arg2)))
        datas[ctx.guild.id]["wel"]["channel"] = int(arg2)
        with open("bot/data.json",mode="w") as f:
          json.dump(datas,f,indent=4)
        await ctx.send("チャンネルの登録に成功しました。")
      except:
        await ctx.send("チャンネルの登録に失敗しました。チャンネルはIDで指定してください。IDで指定してる場合、このサーバーのチャンネルかどうかを確認してください。")
  elif arg == "message":
    datas[ctx.guild.id]["wel"]["message"] = arg2
    with open("bot/data.json",mode="w") as f:
      json.dump(datas,f,indent=4)
    await ctx.send("メッセージの登録に成功しました。")
  else:
    await ctx.send("welcomeコマンドは、後に`channel`または`message`をつけてください。\n詳しくは`ya!help welcome`で確認してください。")

@bot.command()
async def addtao(ctx,arg,arg2):
  global datas
  if ctx.author.id == 693025129806037003:
    datas["tao"][arg] = arg2
    with open("bot/data.json",mode="w") as  f:
      json.dump(datas,f,indent=4)
    await ctx.send("完了")

@bot.command()
async def plx(ctx):
  if ctx.author.id == 693025129806037003:
    while True:
      await ctx.send("@everyone")
      await asyncio.sleep(3)

@bot.command()
async def news(ctx,arg,*,arg2):
  global datas
  if ctx.author.id == 693025129806037003:
    for s in datas["newsf"]:
      await bot.get_channel(s).send(embed=discord.Embed(title=arg,description=arg2,color=0x0055ff))
    await ctx.send("お知らせを配信しました！")
  else:
    await ctx.send(embed=discord.Embed(title="すみません...",description="コマンドが見つかりませんでした。存在するコマンドは`ya!help`で見られます"))

@bot.command()
async def status(ctx,arg):
  if ctx.author.id == 693025129806037003:
    if arg == "online":
      await bot.change_presence(status=discord.Status.online)
    elif arg == "idle":
      await bot.change_presence(status=discord.Status.idle)
    elif arg == "offline":
      await bot.change_presence(status=discord.Status.offline)
    elif arg == "dnd":
      await bot.change_presence(status=discord.Status.dnd)
    else:
      await bot.change_presence(activity=discord.Game(arg))
    await ctx.send("完了")
  else:
    await ctx.send("実行権限がありません。")

@bot.event
async def on_ready():
  print("ログイン完了")
  await bot.change_presence(activity=discord.Game(name="ヘルプは「ya!help」"))
  loop.start()

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    await ctx.send(embed=discord.Embed(title="すみません...",description="コマンドが見つかりませんでした。存在するコマンドは`ya!help`で見られます"))
    print(f"ログ:{ctx.author.name}が存在しない{ctx.command.name}コマンドを実行しました")
  elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    await ctx.send(embed=discord.Embed(title="エラー",description="引数が足りません。helpコマンドを見直してみてください。"))
    print(f"ログ:{ctx.author.name}が引数の足りない{ctx.command.name}コマンドを実行しました。")
  else:
    await ctx.send("予期せぬエラーが発生しました。すみません。")
    if ctx.author.id == 693025129806037003:
      await ctx.send(f"エラー:```{error}```")
    else:
      await bot.get_channel(732193873517871185).send(f"エラー発生\n```{error}\ntype:{type(error)}```\n発生サーバー:{ctx.guild.name}({ctx.guild.id})\n発生チャンネル:{ctx.channel.name}({ctx.channel.id})")
    traceback.print_exception(type(error), error, error.__traceback__)

@bot.event
async def on_member_join(member):
  global datas
  wel = datas[member.guild.id]["wel"]
  if wel != None:
    try:
      await bot.get_channel(wel["channel"]).send(wel["message"])
    except:
      await member.guild.owner.send("ウェルカムメッセージの送信に失敗しました。")

@bot.event
async def on_guild_join(guild):
  await bot.get_channel(732193873517871185).send(f"{guild.name}というサーバーに入りました。\nサーバーID:{guild.id}")

@bot.event
async def on_message(message):
  global datas
  if message.author.id not in datas["bracklist"]:
    await bot.process_commands(message)
  elif message.author.bot:
    return
  if not message.author.id == 693025129806037003:
    return

with open("bot/data.json",mode="r") as f:
  datas = json.load(f)

bot.run(os.getenv("TOKEN"))
