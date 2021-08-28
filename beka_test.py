import asyncio
import json
import random
import discord
from Dtime import Uptime
import cooldown

from bs4 import BeautifulSoup
from urllib.request import URLopener
import random
from Dtime import Uptime
from discord.ext import commands
from discord.utils import get
from urllib.request import Request
from urllib.request import HTTPError
from urllib.request import urlopen 
from urllib.request import Request, urlopen
from urllib.request import quote
from bs4 import BeautifulSoup
import re


prefix = "ㅂ! "
INTENTS = discord.Intents.all()
client = commands.Bot(
    command_prefix="ㅂ! ",
    intents=INTENTS,
    owner_ids=(653075791814590487, 441202161481809922),
)
cooldown = cooldown.CooldownClient()
Uptime.uptimeset()


opggsummonersearch = 'https://www.op.gg/summoner/userName='
tierScore = {
        'default': 0,
        'iron': 1,
        'bronze': 2,
        'silver': 3,
        'gold': 4,
        'platinum': 5,
        'diamond': 6,
        'master': 7,
        'grandmaster': 8,
        'challenger': 9
    }

def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls

@client.event
async def on_ready():
    print("Beka is online! | 베카가 온라인이에요!")
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game("ㅂ! 도움말 : Test Version.")
    )

@client.event
async def on_message(message):

# Main | 기본

    if message.content.startswith(f'{prefix}'):
        await open_account(message.author)
        users = await get_bank_data()
        user = message.author
        if users[str(user.id)]["blist"] == 1:
            await message.reply('**무기한 베카 서비스 제한** 상태인 도박러시네요!\n\n모든 베카 서비스를 사용하실 수 없는 상태에요.')
        if users[str(user.id)]["blist"] == 0:
            if message.content.startswith(f"{prefix}jsk") or message.content.startswith(f"{prefix}종료"):
                ctx = await client.get_context(message)
                await client.invoke(ctx)

            if message.content == f'{prefix}핑':
                await message.reply(f":ping_pong: 베카의 핑은 **{str(round(client.latency * 1000))}ms** 입니다!")

            if message.content in (f'{prefix}도움말',f'{prefix}도움',f'{prefix}명령어',f'{prefix}명령',f'{prefix}help'):
                await message.reply(f'<:ZeroBOT_Warning:799431198489313340> 정말 죄송하지만, 아직 도움말이 완성되지 않았어요. 뚝딱뚝딱..')

            if message.content == f'{prefix}업타임':
                uptime = str(Uptime.uptime()).split(":")
                hours = uptime[0]
                minitues = uptime[1]
                seconds = uptime[2].split(".")[0]
                await message.channel.send(f"베카는 **{hours}시간 {minitues}분 {seconds}초** 동안 켜져있어요!")

            if message.content == f'{prefix}봇정보':
                embed = discord.Embed(title="베카의 정보!", description="베카의 정보서를 몰래 훔쳐보고 있어요..\nDev. `Cookie_` and `심심러`", color=discord.Color.blurple())
                embed.add_field(name="Special thanks.",value="Profile image disaginer\nTester. **(^0^)**\nBox system idea by. **Dashmaster**",inline=False)
                embed.add_field(name="Python Version",value="3.8.6")
                embed.add_field(name="Discord Version",value=discord.__version__)
                embed.set_footer(text="Beka.")
                await message.reply(embed=embed)


        # Json Bating | Json 도박

            if message.content == f"{prefix}가입":
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "N":
                    embed = discord.Embed(title=":wave: 안녕하세요!", description="안녕하세요! 저를 처음 만나시는군요!\n\n저는 베카라고 해요!\n그래서 도박러분의 소중한 정보를 저장하기 위해 허락을 받고 있어요!\n\n허락해주신다면 아래에 있는 ✅ 체크로 반응해주세요!\n\n도박러분에게서 수집하는 정보는 다음과 같아요!\n- 디스코드 닉네임 및 ID", color=discord.Color.blurple())
                    verify_info = await message.reply("베카를 처음 만나시는 분이시군요!\n아래에 있는 내용을 확인한 후, 반응을 체크해주세요!",embed=embed)
                    await verify_info.add_reaction('✅')
                    await verify_info.add_reaction('❎')
                    try:
                        reaction, user = await client.wait_for(
                            "reaction_add",
                            timeout=120,
                            check=lambda reaction, user: user == message.author
                            and str(reaction.emoji) in ["✅", "❎"],
                        )
                    except TimeoutError:
                        await verify_info.delete()
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **2분**를 초과하여 가입에 실패했어요.")
                    else:
                        if str(reaction.emoji) == "✅":
                            await verify_info.delete()
                            await message.reply("와아! 가입에 성공했어요!\n앞으로 베카와 함께 억만장자가 되봅시다!")
                            users[str(user.id)]["verify"] = "Y"
                            users[str(user.id)]["username"] = str(message.author.name)
                            with open("save.json","w", encoding="UTF-8") as f:
                                json.dump(users,f)
                        if str(reaction.emoji) == "❎":
                            await verify_info.delete()
                            await message.reply("<:ZeroBOT_Warning:799431198489313340> 음.. 그래요. 다음에 다시 생각하고 돌아와주세요..!")
                else:
                    await message.reply("<:ZeroBOT_Warning:799431198489313340> 이미 억만장자를 위해 여정을 떠나고 있는데 태초로 돌아가려는건 아니시죠?")

            if message.content.startswith(f'{prefix}좋아요'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                data = cooldown.Cooldown(18000, message.author.id)
                if message.content == f'{prefix}좋아요':
                    await message.reply(f'**{prefix}좋아요 <유저 멘션 / 아이디>** 로 좋아요를 줄 수 있습니다!\n\n**※** 해당 명령어는 5시간의 쿨타임이 존재합니다.') # 43200
                else:
                    if data == True:
                        cooldown.CooldownUpdate(message.author.id) # 쿨타임을 새로 갱신해줍니다. 
                        user_choiced = (
                            message.content.split(" ")[2]
                            .replace("<@", "")
                            .replace("!", "")
                            .replace(">", "")
                        )
                        user_choice = int(user_choiced)
                        user_name = await client.fetch_user(user_choice)
                        if users[str(user_choiced)]["verify"] == "Y":
                            msg = await message.reply(f'**{users[str(user_choiced)]["username"]} 님**에게 좋아요를 지급할까요?\n\n**※** 지급한 뒤에는 5시간 후 재사용이 가능하니 신중히 선택해주세요!')
                            await msg.add_reaction('✅')
                            await msg.add_reaction('❎')
                            try:
                                reaction, user = await client.wait_for(
                                    "reaction_add",
                                    timeout=15,
                                    check=lambda reaction, user: user == message.author
                                    and str(reaction.emoji) in ["✅", "❎"],
                                )
                            except TimeoutError:
                                await msg.delete()
                                await message.reply('<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **10초** 를 초과하여 좋아요는 아껴두기로 했어요..')
                            else:
                                if str(reaction.emoji) == '✅':
                                    await message.reply(f'**{users[str(user_choiced)]["username"]} 님**에게 좋아요를 드렸어요!')
                                    users[str(user_name.id)]["like"] += 1
                                    cooldown.CooldownUpdate(message.author.id)
                                    with open('save.json','w',encoding='UTF-8') as f:
                                        json.dump(users,f)
                                if str(reaction.emoji) == '❎':
                                    await message.reply('<:ZeroBOT_Warning:799431198489313340> 좋아요를 주지 않기로 했어요.')
                    else:
                        hours = data // 3600
                        s = data - hours*3600
                        mu = s // 60
                        ss = s - mu*60
                        await message.reply(f"좋아요를 지급하려면 **{hours}시간 {mu}분 {ss}초** 를 기다려야 해요!") 

            if message.content == f"{prefix}지원금":
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if users[str(user.id)]["money"] == 0:
                        money_give = random.randint(1000,3000)
                        await message.reply(f"**{money_give} 코인**을 지급해드렸어요!\n아껴쓰시길 바랄게요!")
                        users[str(user.id)]["money"] += money_give
                        with open("save.json","w", encoding="UTF-8") as f:
                            json.dump(users,f)
                    else:
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 돈이 이미 있으신데 거지 행세를 하시면 안돼요!")
                else:
                    await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 베카가 친해지고 난 뒤에 오세요!\n**{prefix} 가입** 명령어를 사용해서 가입해주세요!")

            if message.content.startswith(f'{prefix}상점'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                split = message.content.split(" ")
                if message.content == f'{prefix}상점':
                    embed = discord.Embed(title=':shopping_cart: 베카의 상점!', description=f"**{prefix}상점 <아이템 이름> <수량>** 으로 아이템을 구매하실 수 있어요!\n**{prefix}상점 아이템정보 <아이템 이름>** 으로 아이템의 정보를 확인할 수 있어요!", color=discord.Color.random())
                    embed.add_field(name=":gift: 일반 아이템", value=":gift: 상자 : 5,000 <:bekacoin:864009180465201182>")
                    embed.add_field(name=":tickets: 티켓", value=":tickets: 닉네임 변경권 : 3,000,000 <:bekacoin:864009180465201182>\n:tickets: 출금권 : 100 :trophy:")
                    await message.reply(embed=embed)
                if message.content == f'{prefix}상점 아이템정보 상자':
                    await message.reply(embed=discord.Embed(title="아이템정보 : :gift: 상자",description="어딘가 마법이 깃든것 같은 특별한 상자입니다.\n누군가가 담아놓았는지는 몰라도 아주 많은 코인이 담겨있는 상자도 대다수라고 합니다.\n\n특별한 주술을 외치고 상자를 개봉해봅시다! 상자르디움 레비오사!\n\n------------------------------\n\n가격 : 5,000 <:bekacoin:864009180465201182>"))
                if message.content == f'{prefix}상점 아이템정보 닉네임 변경권':
                    await message.reply(embed=discord.Embed(title="아이템정보 : :tickets: 닉네임 변경권",description="신비한 작명가가 만든 닉네임 변경권입니다.\n이 티켓을 사용하면 어떠한 힘에 이끌려 닉네임을 변경할 수 있다고 합니다!\n\n------------------------------\n\n가격 : 3,000,000 <:bekacoin:864009180465201182>"))
                if message.content == f'{prefix}상점 아이템정보 출금권':
                    await message.reply(embed=discord.Embed(title="아이템정보 : :tickets: 출금권",description="자신이 저금해놓은 모든 코인을 한번에 꺼낼 수 있는 티켓입니다.\n최고급 은행에서 만든 티켓이라 1회를 사용하면 사라져버립니다.\n\n------------------------------\n\n가격 : 100 :trophy:"))
                if message.content.startswith(f'{prefix}상점 상자'):
                    number = True
                    try:
                        test = int(split[3])
                    except:
                        number = False
                        await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 상자의 수는 문자가 아니라 숫자라구요!")
                        return None
                    if users[str(user.id)]["money"] >= test*5000:
                        await message.reply(f":shopping_bags: **상자** 아이템을 **{test}개** 만큼 구입하셨어요!")
                        users[str(user.id)]["money"] -= test*5000
                        users[str(user.id)]["box"] += test
                        with open("save.json", "w", encoding="UTF-8") as f:
                            json.dump(users,f)
                    else:
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 아쉽지만, 코인이 부족해서 구매할수가 없어요..")
                if message.content == f'{prefix}상점 출금권':
                    if users[str(user.id)]["point"] >= 100:
                        await message.reply(f":shopping_bags: **출금권** 아이템을 구입하셨어요!")
                        users[str(user.id)]["point"] -= 100
                        users[str(user.id)]["ticket_cgg"] += 1 
                        with open("save.json", "w", encoding="UTF-8") as f:
                            json.dump(users,f)
                    else:
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 아쉽지만, 명성치가 부족해서 구매할수가 없어요..")
                if message.content == f'{prefix}상점 닉네임 변경권':
                    if users[str(user.id)]["money"] >= 3000000:
                        await message.reply(f":shopping_bags: **닉네임 변경권** 아이템을 구입하셨어요!")
                        users[str(user.id)]["money"] -= 5000000
                        users[str(user.id)]["ticket_nick"] += 1 
                        with open("save.json", "w", encoding="UTF-8") as f:
                            json.dump(users,f)
                    else:
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 아쉽지만, 코인이 부족해서 구매할수가 없어요..")
                
            if message.content.startswith(f'{prefix}닉네임변경'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if message.content == f'{prefix}닉네임변경':
                        await message.reply(f'만약 **닉네임 변경권** 을 가지고 있다면 표시되는 닉네임을 변경할 수 있어요!\n\n**{prefix}닉네임변경 <변경할 닉네임>** 으로 변경하실 수 있어요!\n**※** 닉네임은 15글자 이하로 제한돼요.')
                    else:
                        if users[str(user.id)]["ticket_nick"] >= 1:
                            split_msg = message.content[9:23]
                            nick_msg = await message.reply(f'정말 닉네임을 **{split_msg}**로 설정하시겠어요?\n\n**※** 닉네임을 변경한 후에는 닉네임 변경권을 재구매해야 해요!')
                            await nick_msg.add_reaction('✅')
                            await nick_msg.add_reaction('❎')
                            try:
                                reaction, user = await client.wait_for(
                                    "reaction_add",
                                    timeout=10,
                                    check=lambda reaction, user: user == message.author
                                    and str(reaction.emoji) in ["✅", "❎"],
                                )
                            except asyncio.TimeoutError:
                                await nick_msg.delete()
                                await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **5초**를 초과하여 닉네임을 바꾸지 않았어요.")
                            else:
                                if str(reaction.emoji) == '✅':
                                    await message.reply(f"마법의 티켓을 사용해 **{split_msg}**님이 되셨어요! 반가워요!")
                                    users[str(user.id)]["ticket_nick"] -= 1
                                    users[str(user.id)]["username"] = str(split_msg)
                                    with open('save.json','w',encoding='UTF-8') as f:
                                        json.dump(users,f)
                                if str(reaction.emoji) == '❎':
                                    await message.reply('<:ZeroBOT_Warning:799431198489313340> 닉네임 변경을 취소했어요.')

            if message.content.startswith(f'{prefix}강화'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                

            if message.content.startswith(f'{prefix}상자'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                split = message.content.split(" ")
                if message.content == f'{prefix}상자':
                    box_info = await message.reply(f'{users[str(user.id)]["username"]}님은 상자를 **{users[str(user.id)]["box"]}개** 를 가지고 계세요!\n\n**{prefix}상자 <개수>** 로 상자를 개봉해보세요!\n\n아래에 있는 📜 이모지를 눌러 확률을 확인할 수 있어요!')
                    await box_info.add_reaction('📜')
                    try:
                        reaction, user = await client.wait_for(
                            "reaction_add",
                            timeout=10,
                            check=lambda reaction, user: user == message.author
                            and str(reaction.emoji) in ["📜"],
                        )
                    except asyncio.TimeoutError:
                        pass
                    else:
                        if str(reaction.emoji) == "📜":
                            embed = discord.Embed(title="📜 : 상자 확률", description=f"상자 등급 및 잭팟 확률을 알려드려요!\n\n:slot_machine: **잭팟 확률** : 0.5%\n\n:medal: **상자 등급 확률**\n S급 : 1% ( 20,000 ~ 40,000 코인 )\n A급 : 6% ( 6,000 ~ 10,000 코인 )\n B급 : 13% ( 5,000 ~ 9,000 코인 )\n C급 : 20% ( 3,000 ~ 6,000 코인 )\n D급 : 60% ( 1,000 ~ 2,500 코인 )", color=discord.Color.teal())
                            await message.reply(embed=embed) 
                else:
                    number = True
                    try:
                        test = int(split[2])
                    except:
                        number = False
                        await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 상자의 개수는 문자가 아니라 숫자라구요!")
                        return None
                    if users[str(user.id)]["box"] >= test:
                        if int(test) == 1:
                            ran = random.randint(1,100)
                            if ran >= 1 and ran <= 60:
                                ran_money_d = random.randint(1000,2500)
                                if ran_money_d >= 2450 and ran_money_d <= 2500:
                                    await message.reply(f':tada: **Jackpot D등급** 상자를 개봉하여 **{ran_money_d*2}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_d*2
                                    users[str(user.id)]["box"] -= 1
                                else:
                                    await message.reply(f'**D등급** 상자를 개봉하여 **{ran_money_d}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_d
                                    users[str(user.id)]["box"] -= 1
                            if ran >= 61 and ran <= 80:
                                ran_money_c = random.randint(3000,6000)
                                if ran_money_c >= 5950 and ran_money_c <= 6000:
                                    await message.reply(f':tada: **Jackpot C등급** 상자를 개봉하여 **{ran_money_c*2}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_c*2
                                    users[str(user.id)]["box"] -= 1
                                else:
                                    await message.reply(f'**C등급** 상자를 개봉하여 **{ran_money_c}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_d
                                    users[str(user.id)]["box"] -= 1
                            if ran >= 81 and ran <= 93:
                                ran_money_b = random.randint(5000,9000)
                                if ran_money_b >= 8950 and ran_money_b <= 9000:
                                    await message.reply(f':tada: **Jackpot B등급** 상자를 개봉하여 **{ran_money_b*2}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_b*2
                                    users[str(user.id)]["box"] -= 1
                                else:
                                    await message.reply(f'**B등급** 상자를 개봉하여 **{ran_money_b}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_b*2
                                    users[str(user.id)]["box"] -= 1
                            if ran >= 93 and ran <= 99:
                                ran_money_a = random.randint(6000,10000)
                                if ran_money_a >= 9950 and ran_money_a <= 10000:
                                    await message.reply(f':tada: **Jackpot A등급** 상자를 개봉하여 **{ran_money_a*2}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_a*2
                                    users[str(user.id)]["box"] -= 1
                                else:
                                    await message.reply(f'**A등급** 상자를 개봉하여 **{ran_money_a}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_a
                                    users[str(user.id)]["box"] -= 1
                            if ran == 100:
                                ran_money_s = random.randint(20000,40000)
                                if ran_money_s >= 39950 and ran_money_s <= 40000:
                                    await message.reply(f':tada: **Jackpot S등급** 상자를 개봉하여 **{ran_money_s*2}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_s*2
                                    users[str(user.id)]["box"] -= 1
                                else:
                                    await message.reply(f':**S등급** 상자를 개봉하여 **{ran_money_s}코인**을 얻었어요!')
                                    users[str(user.id)]["money"] += ran_money_s
                                    users[str(user.id)]["box"] -= 1
                        else:
                            s = 0
                            a = 0
                            b = 0
                            c = 0
                            d = 0
                            sm = 0
                            am = 0
                            bm = 0
                            cm = 0
                            dm = 0
                            result_money = 0
                            jackpot = 0
                            count = 0
                            print(test)
                            for i in range(1,int(test)+1):
                                ran = random.randint(1,100)
                                if ran >= 1 and ran <= 60:
                                    ran_money_d = random.randint(1000,2500)
                                    if ran_money_d >= 2450 and ran_money_d <= 2500:
                                        jackpot += 1
                                        result_money += ran_money_d*2
                                        d += 1
                                        dm += ran_money_d*2
                                        count += 1
                                    else:
                                        d += 1
                                        result_money += ran_money_d
                                        dm += ran_money_d
                                        count += 1
                                if ran >= 61 and ran <= 80:
                                    ran_money_c = random.randint(3000,6000)
                                    if ran_money_c >= 5950 and ran_money_c <= 6000:
                                        jackpot += 1
                                        result_money += ran_money_c*2
                                        c += 1
                                        cm += ran_money_c*2
                                        count += 1
                                    else:
                                        c += 1
                                        result_money += ran_money_c
                                        cm += ran_money_c
                                        count += 1
                                if ran >= 81 and ran <= 93:
                                    ran_money_b = random.randint(5000,9000)
                                    if ran_money_b >= 8950 and ran_money_b <= 9000:
                                        jackpot += 1
                                        result_money += ran_money_b*2
                                        b += 1
                                        bm += ran_money_b*2
                                        count += 1
                                    else:
                                        b += 1
                                        result_money += ran_money_b
                                        bm += ran_money_b 
                                        count += 1
                                if ran >= 94 and ran <= 99:
                                    ran_money_a = random.randint(6000,10000)
                                    if ran_money_a >= 9950 and ran_money_a <= 10000:
                                        jackpot += 1
                                        result_money += ran_money_a*2
                                        a += 1
                                        am += ran_money_a*2
                                        count += 1
                                    else:
                                        a += 1
                                        result_money += ran_money_a
                                        am += ran_money_a
                                        count += 1
                                if ran == 100:
                                    ran_money_s = random.randint(20000,40000)
                                    if ran_money_s >= 39950 and ran_money_s <= 40000:
                                        jackpot += 1
                                        result_money += ran_money_s*2
                                        s += 1
                                        sm += ran_money_s*2
                                        count += 1
                                    else:
                                        s += 1
                                        result_money += ran_money_s
                                        sm += ran_money_s
                                        count += 1
                            users[str(user.id)]["money"] += result_money
                            users[str(user.id)]["box"] -= test
                            msg = await message.reply(f'상자 **{int(test)}개**를 개봉하여 **{result_money}코인**을 얻었어요!\n\n자세한 개봉 결과를 보고 싶다면 📜 이모지를 눌러주세요!')
                            print(str(count) + ' / ' + str(test) + '번 상자 명령어가 작동되었습니다. ')
                            await msg.add_reaction('📜')
                            try:
                                reaction, user = await client.wait_for(
                                    "reaction_add",
                                    timeout=10,
                                    check=lambda reaction, user: user == message.author
                                    and str(reaction.emoji) in ["📜"],
                                )
                            except asyncio.TimeoutError:
                                pass
                            else:
                                if str(reaction.emoji) == "📜":
                                    embed = discord.Embed(title="📜 : 상자 개봉 결과", description=f"상자 개봉 결과를 알려드려요!\n\n:gift: **총 개봉한 상자 수** : {int(test)}개\n:slot_machine: **잭팟 상자 수** : {jackpot}개\n\n:medal: **상자 등급**\n S급 : {s}개 ( {sm} 코인 )\n A급 : {a}개 ( {am} 코인 )\n B급 : {b}개 ( {bm} 코인 )\n C급 : {c}개 ( {cm} 코인 )\n D급 : {d}개 ( {dm} 코인 )", color=discord.Color.teal())
                                    await message.reply(embed=embed)    


                        with open("save.json","w", encoding="UTF-8") as f:
                            json.dump(users,f)

            if message.content.startswith(f'{prefix}소개말'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                split = message.content.split(" ")
                if users[str(user.id)]["verify"] == "Y":
                    if message.content == f'{prefix}소개말':
                        await message.reply(f"**{prefix}소개말 <소개말 내용>** 으로 소개말을 설정하실 수 있어요!\n\n다만, 30글자가 넘어간다면 칸이 부족해서 잘라낼거에요!")
                    else:
                        message_info = message.content[7:37]
                        await message.reply(f"소개말을 **{message_info}**로 설정해드릴게요!")
                        users[str(user.id)]["infom"] = str(message_info)
                        with open("save.json","w",encoding="UTF-8") as f:
                            json.dump(users,f)

            if message.content.startswith(f'{prefix}도박'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                split = message.content.split(" ")
                money = users[str(user.id)]["money"]
                if users[str(user.id)]["verify"] == "Y":
                    if split[2] == "올인" or split[2] == "ㅇㅇ":
                        if users[str(user.id)]["money"] == 0:
                            await message.reply("<:ZeroBOT_Warning:799431198489313340> 아쉽지만 **0 코인** 으론 배팅할 수 없어요.")
                        else:
                            info_message = await message.reply(f'정말 보유하고 계신 **{money} 코인**을 전부 배팅하시겠어요?')
                            await info_message.add_reaction("✅")
                            await info_message.add_reaction("❎")
                            try:
                                reaction, user = await client.wait_for(
                                    "reaction_add",
                                    timeout=10,
                                    check=lambda reaction, user: user == message.author
                                    and str(reaction.emoji) in ["✅", "❎"],
                                )
                            except asyncio.TimeoutError:
                                await info_message.delete()
                                await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **5초**를 초과하여 배팅을 하지 않았어요."
                                )
                            else:
                                if str(reaction.emoji) == "✅":
                                    result_allin = random.randint(1,100)
                                    random_point = random.randint(1,3)
                                    if 1<=users[str(user.id)]["dobak_per"]>=result_allin:
                                        embed_clear = discord.Embed(title=":slot_machine: 배팅에 성공했어요!", description=f"축하드려요!\n\n**{money} 코인** 과 **{random_point} 명성치**를 얻으셨네요!",color=discord.Color.gold())
                                        await message.reply(embed=embed_clear)
                                        users[str(user.id)]["money"] += money
                                        users[str(user.id)]["dobak_per"] -= 2
                                        users[str(user.id)]["point"] += random_point
                                        users[str(user.id)]["command_count"] += 1
                                    if users[str(user.id)]["dobak_per"]<=result_allin:
                                        embed_fail = discord.Embed(title=":slot_machine: 배팅에 실패했어요.", description=f"안타까워요..\n\n**{money} 코인** 을 잃으셨어요..", color=discord.Color.red())
                                        await message.reply(embed=embed_fail)
                                        users[str(user.id)]["money"] -= money
                                        users[str(user.id)]["dobak_per"] += 1
                                        users[str(user.id)]["command_count"] += 1
                                    with open("save.json","w", encoding="UTF-8") as f:
                                        json.dump(users,f)
                                if str(reaction.emoji) == "❎":
                                    await message.reply("<:ZeroBOT_Warning:799431198489313340> 신중히 배팅하기 위해 조금만 더 기다리기를 선택했어요.")
                    else:
                        number = True
                        try:
                            test = int(split[2])
                        except:
                            number = False
                            await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 코인은 문자가 아니라 숫자라구요!")
                            return None
                        if (number == True and test <= users[str(user.id)]["money"] and 0 <= int(test) and int(test)>=1000):
                            result_dobak = random.randint(1,100)
                            random_point = random.randint(0,2)
                            if 1<=users[str(user.id)]["dobak_per"]>=result_dobak:
                                embed_clear = discord.Embed(title=":slot_machine: 배팅에 성공했어요!", description=f"축하드려요!\n\n**{test} 코인**과 **{random_point} 명성치**를 얻으셨네요!",color=discord.Color.gold())
                                await message.reply(embed=embed_clear)
                                users[str(user.id)]["money"] += test
                                users[str(user.id)]["dobak_per"] -= 2
                                users[str(user.id)]["point"] += random_point
                                users[str(user.id)]["command_count"] += 1
                            if users[str(user.id)]["dobak_per"]<=result_dobak:
                                embed_fail = discord.Embed(title=":slot_machine: 배팅에 실패했어요.", description=f"안타까워요..\n\n**{test} 코인** 을 잃으셨어요..", color=discord.Color.red())
                                await message.reply(embed=embed_fail)
                                users[str(user.id)]["money"] -= test
                                users[str(user.id)]["dobak_per"] += 1
                                users[str(user.id)]["command_count"] += 1
                            with open("save.json","w", encoding="UTF-8") as f:
                                json.dump(users,f)
                        else:
                            await message.reply("<:ZeroBOT_Warning:799431198489313340> 정말 아쉽지만, 배팅한 코인이 가지고 있는 코인보다 많거나, **1,000 코인** 이하로는 배팅을 할 수 없어요!")

            if message.content.startswith(f'{prefix}슬롯'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if message.content == f'{prefix}슬롯':
                    await message.reply(f'**{prefix}슬롯 <배팅할 코인>** 으로 슬롯머신에 배팅해보세요!\n\n**※** 해당 도박은 __도박 성공 확률__ 의 영향을 받지 않습니다.')
                else:
                    number = True
                    try:
                        test = int(message.content.split(" ")[2])
                    except:
                        number = False
                        await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 코인은 문자가 아니라 숫자라구요!")
                        return None
                    if (number == True and test <= users[str(user.id)]["money"] and 0 <= int(test)):
                        if users[str(user.id)]["money"] >= int(message.content.split(" ")[2]):
                            list_slot = ['👑','💎','❤','🏆','💰','7️⃣']
                            a = random.choice(list_slot)
                            b = random.choice(list_slot)
                            c = random.choice(list_slot)
                            a_msg = await message.reply(f':slot_machine: | {a}..',mention_author=False)
                            await asyncio.sleep(1)
                            await a_msg.delete()
                            b_msg = await message.reply(f':slot_machine: | {a} : {b}..',mention_author=False)
                            await asyncio.sleep(1)
                            await b_msg.delete()
                            c_msg = await message.reply(f':slot_machine: | {a} : {b} : {c}!',mention_author=False)
                            if a == b or a == c or b == c:
                                await c_msg.delete()
                                await message.reply(f'2개의 슬롯이 같아서 1.5배의 코인 ( **{int(message.content.split(" ")[2]) + int(message.content.split(" ")[2])//2} 코인** ) 을 받았어요!')
                                users[str(user.id)]["money"] += int(message.content.split(" ")[2]) + int(message.content.split(" ")[2])//2
                            if a == b and b == c:
                                await message.reply(f':tada: **Jackpot!** 3배의 코인 ( **{int(message.content.split(" ")[2])*3} 코인** ) 을 받았어요!')
                                users[str(user.id)]["money"] += int(message.content.split(" ")[2]) * 3
                            if a != b and b != c:
                                await message.reply(f'모든 슬롯이 달라 배팅한 코인을 모두 잃었어요..')
                                users[str(user.id)]["money"] -= int(message.content.split(" ")[2])
                            with open('save.json','w',encoding='UTF-8') as f:
                                json.dump(users,f)
                        else:
                            await message.reply(f'<:ZeroBOT_Warning:799431198489313340> 정말 안타깝지만, 코인이 부족해요.')

            if message.content == f'{prefix}출금':
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["ticket_cgg"] >= 1:
                    cg_msg = await message.reply(f'정말 **출금권**을 사용하여 {users[str(user.id)]["bankm"]}코인을 출금하시겠어요?\n\n**※** 출금후에는 20%의 수수료를 추가로 지급해드려요!')
                    await cg_msg.add_reaction('✅')
                    await cg_msg.add_reaction('❎')
                    try:
                        reaction, user = await client.wait_for(
                            "reaction_add",
                            timeout=10,
                            check=lambda reaction, user: user == message.author
                            and str(reaction.emoji) in ["✅", "❎"],
                        )
                    except asyncio.TimeoutError:
                        await info_message.delete()
                        await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **10초**를 초과하여 출금을 취소했어요."
                        )
                    else:
                        if str(reaction.emoji) == '✅':
                            cg_susureo = users[str(user.id)]["bankm"] // 5
                            cg_result = cg_susureo + users[str(user.id)]["bankm"]
                            await message.reply(f'**{cg_result} 코인**을 출금했어요!')
                            users[str(user.id)]["bankm"] = 0
                            users[str(user.id)]["money"] += cg_result
                            users[str(user.id)]["ticket_cgg"] -= 1
                            with open('save.json','w',encoding='UTF-8') as f:
                                json.dump(users,f)

            if message.content.startswith(f"{prefix}가방"):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if message.content == f'{prefix}가방':
                        embed = discord.Embed(title=f'<:ZeroBOT_Backpack:799432571318304768> <{users[str(user.id)]["dg"]}> {users[str(user.id)]["username"]}님의 가방!', description="뒤적뒤적.. 가방을 살펴봤어요!", color=discord.Color.dark_gold())
                        embed.add_field(name=f":thought_balloon: : 소개말 | {prefix}소개말으로 변경할 수 있어요.", value=users[str(user.id)]["infom"], inline=True)
                        embed.add_field(name="👍 : 좋아요", value=f'{users[str(user.id)]["like"]}개',inline=False)
                        embed.add_field(name="<:bekacoin:864009180465201182> : 코인",value=f'{users[str(user.id)]["money"]} 코인')
                        embed.add_field(name=":scales: : 도박 성공 확률",value=f'{users[str(user.id)]["dobak_per"]}%')
                        embed.add_field(name=":gift: : 상자", value=f'{users[str(user.id)]["box"]} 개')
                        embed.add_field(name=":trophy: : 명성치", value=f'{users[str(user.id)]["point"]} 점')
                        embed.add_field(name=":bank: : 저금액", value=f'{users[str(user.id)]["bankm"]} 코인')
                        embed.add_field(name=":tickets: : 티켓", value=f'닉네임 변경권 : {users[str(user.id)]["ticket_nick"]}장, 출금권 : {users[str(user.id)]["ticket_cgg"]}장')
                        await message.reply(embed=embed)
                    else:
                        user_choiced = (
                            message.content[6:]
                            .replace("<@", "")
                            .replace("!", "")
                            .replace(">", "")
                        )
                        user_choice = int(user_choiced)
                        user_name = await client.fetch_user(user_choice)
                        if users[str(user_choice)]["verify"] == "Y":
                            embed = discord.Embed(title=f'<:ZeroBOT_Backpack:799432571318304768> <{users[str(user_choice)]["dg"]}> {users[str(user_name.id)]["username"]}님의 가방!', description="뒤적뒤적.. 가방을 몰래 훔쳐봤어요!", color=discord.Color.dark_gold())
                            embed.add_field(name=":thought_balloon: : 소개말", value=users[str(user_choice)]["infom"], inline=False)
                            embed.add_field(name="👍 : 좋아요", value=f'{users[str(user_choice)]["like"]}개',inline=False)
                            embed.add_field(name="<:bekacoin:864009180465201182> : 코인",value=f'{users[str(user_choice)]["money"]} 코인')
                            embed.add_field(name=":scales: : 도박 성공 확률",value=f'{users[str(user_choice)]["dobak_per"]}%')
                            embed.add_field(name=":gift: : 상자", value=f'{users[str(user_choice)]["box"]} 개')
                            embed.add_field(name=":trophy: : 명성치", value=f'{users[str(user_choice)]["point"]} 점')
                            embed.add_field(name=":bank: : 저금액", value=f'{users[str(user_choice)]["bankm"]} 코인')
                            embed.add_field(name=":tickets: : 티켓", value=f'닉네임 변경권 : {users[str(user_choice)]["ticket_nick"]}장, 출금권 : {users[str(user_choice)]["ticket_cgg"]}장')
                            await message.reply(embed=embed)
                else:
                    await message.reply(f'아직 베카가 친해지지 않으신 분이시네요! **{prefix}가입** 명령어를 사용해서 가입해주세요!')

            if message.content == f'{prefix}일':
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == 'Y':
                    if users[str(user.id)]["runing"] == 0:
                        quiz = await message.reply('어떤 일을 진행하시겠어요?\n\n1️⃣ - 15초 ( 2,500 코인 )\n2️⃣ - 30초 ( 4,500 코인 )\n3️⃣ - 1분 ( 8,000 코인 )\n\n**※** 시간이 길수록 보상 코인이 적은 이유는 시간이 많을수록 메시지 작성량이 적어지기 때문이에요.')
                        await quiz.add_reaction('1️⃣')
                        await quiz.add_reaction('2️⃣')
                        await quiz.add_reaction('3️⃣')
                        try:
                            reaction, user = await client.wait_for(
                                "reaction_add",
                                timeout=10,
                                check=lambda reaction, user: user == message.author
                                and str(reaction.emoji) in ["1️⃣", "2️⃣","3️⃣"],
                            )
                        except asyncio.TimeoutError:
                            await quiz.delete()
                            await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **10초**를 초과하여 일을 하지 않았어요."
                            )
                        else:
                            if str(reaction.emoji) == '1️⃣':
                                await message.reply(f'일을 시작했어요! 15초 뒤에 **2,500 코인** 이 지급될거에요!')
                            if str(reaction.emoji) == '2️⃣':
                                await message.reply(f'일을 시작했어요! 30초 뒤에 **4,500 코인** 이 지급될거에요!')
                            if str(reaction.emoji) == '3️⃣':
                                await message.reply(f'일을 시작했어요! 1분 뒤에 **8,000** 코인이 지급될거에요!')
                            users[str(user.id)]["runing"] = 1
                            with open('save.json','w',encoding='UTF-8') as f:
                                json.dump(users,f)
                            if str(reaction.emoji) == '1️⃣':
                                await asyncio.sleep(15)
                            if str(reaction.emoji) == '2️⃣':
                                await asyncio.sleep(30)
                            if str(reaction.emoji) == '3️⃣':
                                await asyncio.sleep(60)
                            if str(reaction.emoji) == '1️⃣':
                                await message.reply('일이 끝났어요! **2,500 코인** 을 지급해드렸어요!',mention_author=False)
                            if str(reaction.emoji) == '2️⃣':
                                await message.reply('일이 끝났어요! **4,500 코인** 을 지급해드렸어요!',mention_author=False)
                            if str(reaction.emoji) == '3️⃣':
                                await message.reply('일이 끝났어요! **8,000 코인** 을 지급해드렸어요!',mention_author=False)
                            if str(reaction.emoji) == '1️⃣':
                                users[str(user.id)]["money"] += 2500
                            if str(reaction.emoji) == '2️⃣':
                                users[str(user.id)]["money"] += 4500
                            if str(reaction.emoji) == '3️⃣':
                                users[str(user.id)]["money"] += 8000
                            users[str(user.id)]["runing"] = 0
                            with open('save.json','w',encoding='UTF-8') as f:
                                json.dump(users,f)
                    if users[str(user.id)]["runing"] == 1:
                        await message.reply('<:ZeroBOT_Warning:799431198489313340> 이중 알바는 안돼요!')
                else:
                    await message.reply(f'<:ZeroBOT_Warning:799431198489313340> 베카와 친해진 다음에 알바가 가능해요!\n\n**{prefix}가입** 을 사용해 가입 후 사용해주세요!')


            if message.content.startswith(f'{prefix}저금'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if message.content == f'{prefix}저금':
                        await message.reply(f'보유하신 돈을 저금하고 이자를 받으실 수 있어요!\n\n**{prefix}저금 <저금할 금액>** 으로 저금할 수 있어요!')
                    else:
                        split = message.content.split(" ")
                        number = True
                        try:
                            test = int(split[2])
                        except:
                            number = False
                            await message.reply(f"<:ZeroBOT_Warning:799431198489313340> 코인은 문자가 아니라 숫자라구요!")
                            return None
                        if number == True and test <= users[str(user.id)]["money"]:
                            msg = await message.reply(f'정말로 **{test} 코인** 을 저금하시겠어요?\n\n상점에서 출금 티켓을 구매해야 출금할 수 있으니 신중히 선택해주세요.')
                            await msg.add_reaction('✅')
                            await msg.add_reaction('❎')
                            try:
                                reaction, user = await client.wait_for(
                                    "reaction_add",
                                    timeout=10,
                                    check=lambda reaction, user: user == message.author
                                    and str(reaction.emoji) in ["✅", "❎"],
                                )
                            except TimeoutError:
                                await verify_info.delete()
                                await message.reply("<:ZeroBOT_Warning:799431198489313340> 반응 대기시간 **10초**를 초과하여 저금을 취소했어요.")
                            else:
                                if str(reaction.emoji) == "✅":
                                    await msg.delete()
                                    await message.reply(f"**{test} 코인** 을 저금했어요!")
                                    users[str(user.id)]["money"] -= test
                                    users[str(user.id)]["bankm"] += test
                                    with open("save.json","w", encoding="UTF-8") as f:
                                        json.dump(users,f)
                                if str(reaction.emoji) == "❎":
                                    await msg.delete()
                                    await message.reply(f'<:ZeroBOT_Warning:799431198489313340> 저금을 취소했어요!')

            if message.content == f'{prefix}등급':
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if users[str(user.id)]["dg"] == '초보 도박러':
                        chat_hando = 100 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 100:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n앞으로 도박을 더해 베카를 더 알아가는 단계에요.\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴테니 화이팅하세요!')
                        if users[str(user.id)]["command_count"] >= 100:
                            await message.reply(f'도박을 **100번** 하셔서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n도박에 좋은 결과가 있었길 바래요.')
                            users[str(user.id)]["dg"] = '경험 도박러'
                            users[str(user.id)]["next_dg"] = '중수 도박러'
                    if users[str(user.id)]["dg"]== '경험 도박러':
                        chat_hando = 300 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 300:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n베카의 도박을 많이 경험하고, 시련을 느끼는 단계에요.\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴게요!')
                        if users[str(user.id)]["command_count"] >= 300:
                            await message.reply(f'도박을 **300번** 하셔서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n이제 도박에 익숙해지셨나요?')
                            users[str(user.id)]["dg"] = '중수 도박러'
                            users[str(user.id)]["next_dg"] = '고수 도박러'
                    if users[str(user.id)]["dg"] == '중수 도박러':
                        chat_hando = 500 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 500:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n베카의 도박으로 많은 코인을 얻었을거에요.\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴게요!')
                        if users[str(user.id)]["command_count"] >= 500:
                            await message.reply(f'도박을 **500번** 해서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n나쁘지 않은 결과가 분명 있을거에요!')
                            users[str(user.id)]["dg"] = '고수 도박러'
                            users[str(user.id)]["next_dg"] = '프로 도박러'
                    if users[str(user.id)]["dg"]== '고수 도박러':
                        chat_hando = 1000 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 1000:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n이 정도면 중독이네요! 쉬엄쉬엄 하세요..\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴게요!')
                        if users[str(user.id)]["command_count"] >= 1000:
                            await message.reply(f'도박을 **1000번** 해서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n이제 슬슬 만족하셔야 될것 같아요..')
                            users[str(user.id)]["dg"] = '프로 도박러'
                            users[str(user.id)]["next_dg"] = '레전드 도박러'
                    if users[str(user.id)]["dg"]== '프로 도박러':
                        chat_hando = 3000 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 3000:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n도박에만 몰두하는 프로정신을 가지셨어요..\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴게요!')
                        if users[str(user.id)]["command_count"] >= 3000:
                            await message.reply(f'도박을 **3000번** 해서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n사람이세요..?')
                            users[str(user.id)]["dg"] = '레전드 도박러'
                            users[str(user.id)]["next_dg"] = '신급 도박러'
                    if users[str(user.id)]["dg"]== '레전드 도박러':
                        chat_hando = 7000 - int(users[str(user.id)]["command_count"])
                        if users[str(user.id)]["command_count"] <= 7000:
                            await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n경이로운 단계인 레전드 도박러세요..\n앞으로 도박을 **{chat_hando}번** 더 하시면 다음으로 등업해드릴게요!')
                        if users[str(user.id)]["command_count"] >= 7000:
                            await message.reply(f'도박을 **7000번** 해서 **{users[str(user.id)]["next_dg"]}** 등급으로 등업해드렸어요.\n\n도박 멈춰!')
                            users[str(user.id)]["dg"] = '신'
                            users[str(user.id)]["next_dg"] = '없음'
                    if users[str(user.id)]["dg"]== '신':
                        await message.reply(f'**{users[str(user.id)]["dg"]}** 이시군요!\n\n제 자신에 있는 모든 경이로움을 표합니다.. 사람 맞아요..?')
                    with open('save.json','w',encoding='UTF-8') as f:
                        json.dump(users,f)
            
            if message.content.startswith(f'{prefix}변경'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                split = message.content.split(" ")
                if users[str(user.id)]["dev"] == 1:
                    if message.content == f'{prefix}변경':
                        await message.reply(f'**{prefix}변경 <종류> <유저아이디> <추가/삭제할 수>** 명령어를 사용해 사용할 수 있습니다.\n\n**ex )** {prefix}변경 money 123456789 -10000\n\n종류 : money, bankm, point, box, dobak_per, command_count, ticket_cgg, ticket_nick, runing, dg, next_dg, infom, **dev**, **premium**, **blist**')
                    else:
                        if split[2] == 'infom' or split[2] == 'dg' or split[2] == 'next_dg':
                            split = message.content.split(" ")
                            users[str(split[3])][split[2]] = str(split[4])
                            await message.reply(f'**{await client.fetch_user(split[3])} 님**의 {split[2]} 항목을 {split[4]} 으로 변경했습니다.')
                            with open('save.json','w') as f:
                                json.dump(users,f)
                        else:
                            split = message.content.split(" ")
                            users[str(split[3])][split[2]] += int(split[4])
                            await message.reply(f'**{await client.fetch_user(split[3])} 님**의 {split[2]} 에 {split[4]} 을(를) 성공적으로 추가했습니다.')
                            with open('save.json','w') as f:
                                json.dump(users,f)
                else:
                    await message.reply('<:ZeroBOT_Warning:799431198489313340> **변경** 커맨드를 사용하려면 최소 **Developer** 권한이 필요해요.')

            if message.content.startswith(f'{prefix}nt'):
                await open_account(message.author)
                users = await get_bank_data()
                user = message.author
                if users[str(user.id)]["verify"] == "Y":
                    if message.content == f'{prefix}nt':
                        embed = discord.Embed(title=f'<:ZeroBOT_Backpack:799432571318304768> <{users[str(user.id)]["dg"]}> {users[str(user.id)]["username"]}님의 가방!', description="뒤적뒤적.. 가방을 살펴봤어요!", color=discord.Color.dark_gold())
                        embed.add_field(name=f":thought_balloon: : 소개말 | {prefix}소개말으로 변경할 수 있어요.", value=users[str(user.id)]["infom"], inline=True)
                        embed.add_field(name="👍 : 좋아요", value=f'{users[str(user.id)]["like"]}개',inline=False)
                        amount = int(users[str(user.id)]["money"])
                        embed.add_field(name="<:bekacoin:864009180465201182> : 코인",value=f'{amount[0:-8]}, {amount[-8,-4]}, {amount[-4]} 코인')
                        embed.add_field(name=":scales: : 도박 성공 확률",value=f'{users[str(user.id)]["dobak_per"]}%')
                        embed.add_field(name=":gift: : 상자", value=f'{users[str(user.id)]["box"]} 개')
                        embed.add_field(name=":trophy: : 명성치", value=f'{users[str(user.id)]["point"]} 점')
                        embed.add_field(name=":bank: : 저금액", value=f'{users[str(user.id)]["bankm"]} 코인')
                        embed.add_field(name=":tickets: : 티켓", value=f'닉네임 변경권 : {users[str(user.id)]["ticket_nick"]}장, 출금권 : {users[str(user.id)]["ticket_cgg"]}장')
                        await message.reply(embed=embed)

            if message.content.startswith(f"{prefix}롤"):
                playerNickname = message.content[5:]
                """롤전적을 보여줍니다."""
                checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')

                # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다
                RankMedal = bs.findAll('img', {
                    'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
                # index 0 : Solo Rank
                # index 1 : Flexible 5v5 rank

                # for mostUsedChampion
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

                # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

                if len(playerNickname) == 1:
                    embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0xff0000)
                    embed.add_field(name="Summoner name not entered",
                                    value="To use command {prefix}롤 : {prefix}롤 (Summoner Nickname)", inline=False)
                    await message.reply("Error : Incorrect command usage ", embed=embed)

                elif len(deleteTags(bs.findAll('h2', {'class': 'Title'}))) != 0:
                    embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0xff0000)
                    embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
                    await message.reply("Error : Non existing Summoner ", embed=embed)
                else:
                    try:
                        # Scrape Summoner's Rank information
                        # [Solorank,Solorank Tier]
                        solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                        # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                        solorank_Point_and_winratio = deleteTags(
                            bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                        # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                        flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                            'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                                    'sub-tier__gray-text'}}))
                        # ['Flextier W/L]
                        flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                        # embed.set_imag()는 하나만 들어갈수 있다.

                        # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
                        if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                            embed = discord.Embed(title="소환사 전적검색", description="", color=0xff00)
                            embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                            embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                            await message.reply(f"소환사 **{playerNickname}** 님의 전적", embed=embed)

                        # 솔로랭크 기록이 없는경우
                        elif len(solorank_Point_and_winratio) == 0:

                            # most Used Champion Information : Champion Name, KDA, Win Rate
                            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                            mostUsedChampion = mostUsedChampion.a.text.strip()
                            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                            FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                            FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                            embed = discord.Embed(title="소환사 전적검색", description="", color=0xff00)
                            embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                            embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                            embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                            value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                            inline=False)
                            embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                            await message.reply(f"소환사 **{playerNickname}** 님의 전적", embed=embed)

                        # 자유랭크 기록이 없는경우
                        elif len(flexrank_Point_and_winratio) == 0:

                            # most Used Champion Information : Champion Name, KDA, Win Rate
                            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                            mostUsedChampion = mostUsedChampion.a.text.strip()
                            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                            SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                            SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                                1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                            embed = discord.Embed(title="소환사 전적검색", description="", color=0xff00)
                            embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                            embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                            embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                            value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                            inline=False)
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                            await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
                        # 두가지 유형의 랭크 모두 완료된사람
                        else:
                            # 더 높은 티어를 thumbnail에 안착
                            solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                            flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                             # Make State
                            SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                            SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                                1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                            FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                            FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                            # most Used Champion Information : Champion Name, KDA, Win Rate
                            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                            mostUsedChampion = mostUsedChampion.a.text.strip()
                            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                            cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                            embed = discord.Embed(title="소환사 전적검색", description="", color=0xff00)
                            embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                            embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                            embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                            value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                            inline=False)
                            if cmpTier == 0:
                                embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                            elif cmpTier == 1:
                                embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                            else:
                                if solorankmedal[1] > flexrankmedal[1]:
                                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                                elif solorankmedal[1] < flexrankmedal[1]:
                                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                                else:
                                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                            await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
                    except HTTPError as e:
                        embed = discord.Embed(title="소환사 전적검색 실패", description="", color=discord.Colour.red())
                        embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                        await message.channel.send("Wrong Summoner Nickname")

                    except UnicodeEncodeError as e:
                        embed = discord.Embed(title="소환사 전적검색 실패", description="", color=discord.Colour.red())
                        embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
                        await message.channel.send("Wrong Summoner Nickname", embed=embed)
        




# Json Loading | Json 로드

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["username"] = ""
        users[str(user.id)]["money"] = 1000
        users[str(user.id)]["bankm"] = 0
        users[str(user.id)]["verify"] = "N"
        users[str(user.id)]["box"] = 10
        users[str(user.id)]["blist"] = 0
        users[str(user.id)]["dev"] = 0
        users[str(user.id)]["premium"] = 0
        users[str(user.id)]["dobak_per"] = 50
        users[str(user.id)]["infom"] = "없음"
        users[str(user.id)]["point"] = 0
        users[str(user.id)]["ticket_cgg"] = 0
        users[str(user.id)]["ticket_nick"] = 0
        users[str(user.id)]["runing"] = 0
        users[str(user.id)]["dg"] = "초보 도박러"
        users[str(user.id)]["next_dg"] = "경험 도박러"
        users[str(user.id)]["command_count"] = 0
        users[str(user.id)]["like"] = 0

    with open("save.json", "w", encoding='UTF-8') as f:
        users = json.dump(users, f, indent=2)
    return True


async def get_bank_data():
    with open("save.json", encoding='UTF-8') as f:
        users = json.load(f)

    return users

client.load_extension('jishaku')

client.run("ODE0NzE5MTQ3ODcwOTEyNTIy.YDh8VQ.X8VEj_CZqmoCiBAt5JTBn_UhczQ")
