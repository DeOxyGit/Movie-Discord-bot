from configparser import DEFAULTSECT
from socket import EBADF
from warnings import resetwarnings
import discord
from datetime import datetime,timedelta
from discord import embeds
from discord import colour
from discord.ext import commands
import imdb
import requests
import random
import translators as trans


# all value 
message_lastseen = datetime.now()

moviesDB = imdb.IMDb()

r =(''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 2)))

bot = commands.Bot(command_prefix='#',help_command=None)

message_lastseen = datetime.now()

Token='ODU1MzQxNTM5OTk5MjE5NzIz.YMxE4g.k_eEa1mFn_M1TleQjbRU8JB_HA4'

# console loggin
@bot.event
async def on_ready():
    print(f'Loggin in  as {bot.user}')



# help
@bot.command()
async def help(ctx):
    emBed1=discord.Embed(title='LuvMovie BOT! :robot:',description='วิธีการใช้คำสั่งกับบอท',color=0xb021fc)
    emBed1.add_field(name='Commands :video_game:',value='1) #movie ชื่อหนัง \n 2) #help: show this message\n 3) #thai เอาไว้ดูยอดผู้ติดเชื้อ covid-19 ในไทย \n 4) #tran คำที่อยากแปล \n 5) #exchange จำนวณเงิน $ to THB',inline=False)
    emBed1.add_field(name='Update sheet :newspaper:',value='Beta test อยู่ในช่วงทดลอง\n ถ้าพบBug แจ้ง@Deoxy\n คำสั่ง #movie ตอบสนองช้าไม่รู้ทำไม',inline=False)
    emBed1.set_thumbnail(url='https://cdn.discordapp.com/attachments/852573771021680680/857660108653199421/960-9609689_red-question-mark-symbol-question-mark-removebg-preview.png')
    emBed1.set_footer(text='Beta test Codee')
    await ctx.channel.send(embed=emBed1)



# movie
@bot.command(pass_context=True)
async def movie(ctx,*,par):
       movies = moviesDB.search_movie(par)
       id = movies[0].getID()
      # var movie   
       movies = moviesDB.get_movie(id)
       title = movies['title']
       year = movies['year']
       rating = movies['rating']
       genres=movies['genres']
       director=movies['directors']
       runtime = movies['runtime']
       urll=movies['full-size cover url']
      # array to normal   
       direc= ''.join(map(str,director))
       genr=', '.join(map(str,genres))
       min=''.join(map(str,runtime))

       mention = ctx.author.mention


       
       #output message    
       emBed = discord.Embed(title='Movie!! :popcorn:',description=f'ค้นหาเพื่อดูข้อมูลหนังง request by[{mention}]',color=0xf44a79)
       emBed.add_field(name='ชื่อหนัง :movie_camera:',value=title)
       emBed.add_field(name='เรตติ้ง :star:',value=rating)
       emBed.add_field(name='ปี :hourglass:',value=year)
       emBed.add_field(name='ประเภทหนัง',value=f'{genr}')
       emBed.add_field(name='ผู้กำกับหนัง :man_detective:',value=f'{direc}')
       emBed.add_field(name='เวลาดู :timer:',value=f'{min}'+str('นาที'))
       emBed.set_footer(text='beta test Update 21/6/2021')
       emBed.set_thumbnail(url=f'{urll}')
       emBed.set_image(url=f'{urll}')

       await ctx.channel.send(embed=emBed)



# plot เนื้อเรื่องของหนัง
@bot.command()
async def plot(ctx,par):
    movies = moviesDB.search_movie(par)
    id = movies[0].getID()
    movies = moviesDB.get_movie(id)
    # value
    plots=movies['plot summaries']
    plotss=''.join(map(str,plots))

    # output
    await ctx.channel.send(plotss)



# thai เช๊คcovid-19
@bot.command()
async def thai(ctx):
    # API
    response=requests.get("https://disease.sh/v3/covid-19/countries/thailand")
    data=response.json()
    newcon=data['todayCases']
    allcase=data['cases']
    reco=data['recovered']
    hospi=data['active']
    die=data['deaths']
    todaydie=data['todayDeaths']

    datestr = datetime.fromtimestamp(data["updated"] / 1e3)
    normdate=datestr.strftime("%A %d/%m/%Y")

    mention = ctx.author.mention
    
    emBedcovid=discord.Embed(title='Covid-19 Update today!',description=f'request by [{mention}]',color=0xFF0000)
    emBedcovid.add_field(name='ผู้ติดเชื้อทั้งหมด',value='{:,}'.format(allcase)+' คน')
    emBedcovid.add_field(name='ติดเชื้อเพิ่ม',value='{:,}'.format(newcon)+' คน')
    emBedcovid.add_field(name='หายแล้ว',value='{:,}'.format(reco)+' คน')
    emBedcovid.add_field(name='อยู่โรงพยาบาล',value='{:,}'.format(hospi)+' คน')
    emBedcovid.add_field(name='ตายแล้ว',value='{:,}'.format(die)+' คน')
    emBedcovid.add_field(name='ตายเพิ่ม',value='{:,}'.format(todaydie)+' คน')
    emBedcovid.add_field(name='อัพเดตเมื่อ',value=f'{normdate}')
    emBedcovid.set_thumbnail(url='https://phil.cdc.gov//PHIL_Images/23311/23311_lores.jpg')

    await ctx.channel.send(embed=emBedcovid)



# tran แปลภาษา
@bot.command(pass_context=True)
async def tran(ctx,*,par):
    b =(trans.google(str(par), form_language='en', to_language='th'))
    mention = ctx.author.mention

    tranembed=discord.Embed(title='บอทวุ้นแปลภาษา  :arrows_counterclockwise:', description=f'request by[{mention}]\nรองรับ ภาษา en ไป th',color=0x3483eb)
    tranembed.add_field(name='แปลว่า :white_check_mark:',value=f'{b}')
    await ctx.channel.send(embed=tranembed)
    


# $ to THB
@bot.command(pass_context=True)
async def exchange(ctx,*,par):
    mention = ctx.author.mention
    r = int(par)*32.5
    emVeds=discord.Embed(title='Exchange Bot!', description=f'$ to THB\n request by [{mention}]',color=0x118C4F)
    emVeds.add_field(name='You will get', value='{:,}'.format(r)+' THB')
    emVeds.set_footer(text='Test Code by DeOxYz')
    await ctx.channel.send(embed=emVeds)


# # message
@bot.event
async def on_message(message):

    mention = message.author.mention

    if message.content == 'ตุ้ก':
        await message.channel.send(f'{mention} ตุ้กกกกกกกกกี้')
    elif message.content == 'shader':
        await message.channel.send(f'{mention} Shader---> https://www.mediafire.com/file/2p9tn2fult48hny/Sildur%2527s_Vibrant_Shaders_v1.29_High.zip/file \n Optifine --> http://adfoc.us/serve/sitelinks/?id=475250&url=http://optifine.net/adloadx?f=preview_OptiFine_1.17_HD_U_G9_pre24.jar&x=fcb9')

    await bot.process_commands(message) 

bot.run(Token)