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

# Gobal var
bot = commands.Bot(command_prefix='#',help_command=None)
moviesDB = imdb.IMDb()

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


bot.run('your token')
# Code by Ratchanon Promsombut

