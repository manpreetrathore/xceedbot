from discord import Embed, Member
from discord.ext import commands
from discord.utils import get
import random
import discord
from random import choice, randint
from requests import get as rget

class Random(commands.Cog, name='Random'):
    """
    Can be used by everyone and contains "games" and randomness.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='!toss [heads/tails]', description='Toss against the bot')
    async def toss(self, ctx, arg):
        if arg.lower() == 'heads' or arg.lower() == 'tails':
            piece = random.choice(['heads', 'tails'])
            if arg.lower() in piece:
                await ctx.send(f':white_check_mark: {piece}! GG, you won. ')
            else:
                await ctx.send(f':negative_squared_cross_mark: {piece}! You lost. ')
        else:
            await ctx.send('❌ You must enter "heads" or "tails"!')

    # @commands.command(brief='!ping [random/pseudo]', description="Mention someone")
    # async def ping(self, ctx, arg):
    #     members = [x for x in ctx.guild.members if not x.bot]
    #     if arg.content.lower() == 'random':
    #         await ctx.send(f'Hey {random.choice(members).mention} !')
    #     else:
    #         await ctx.send(f'Hey {arg.mention} !')

    @commands.command(aliases=['r'], brief='!roll [x]', description="Roll a die of [x] sides")
    async def roll(self, ctx, faces: int):
        number = randint(1, faces)
        await ctx.send(f'🎲 You got a {number} !')

    # @commands.command(brief='!meme', description='Watch a random meme')
    # async def meme(self, ctx):
    #     res = rget('https://meme-api.herokuapp.com/gimme').json()
    #     rant = random.randint(0, 0xffffff)
    #     embed = discord.Embed(title=f":speech_balloon: res['title']",
    #                    url=res['postLink'],
    #                    description=' ',color=rant)
    #         # embed.add_field(name='✍', value=res['author'], inline=False)
    #         # embed.add_field(name='👍', value=res['ups'], inline=True)
    #     embed.set_image(url=url)
    #     embed.set_footer(text="  ✍ {}    👍 {}  ".format(res['author'],res['ups']))
    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
