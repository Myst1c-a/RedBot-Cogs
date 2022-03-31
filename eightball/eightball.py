from redbot.core import commands
import random
import discord   

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name='8ball', help='A simpe 8ball command', aliases=['8b'])
    async def eightball(self, ctx,*, question):
     responses = ['As I see it, yes.',
             'Yes.',
             'Positive',
             'From my point of view, yes',
             'Convinced.',
             'Most Likley.',
             'Chances High',
             'No.',
             'Negative.',
             'Not Convinced.',
             'Perhaps.',
             'Not Sure',
             'Mayby',
             'I cannot predict now.',
             'Im to lazy to predict.',
             'I am tired. *proceeds with sleeping*']
     response = random.choice(responses)
     embed=discord.Embed(title="The Magic 8 Ball has Spoken!", color=self.bot.color)
     embed.add_field(name='Question: ', value=f'{question}', inline=True)
     embed.add_field(name='Answer: ', value=f'{response}', inline=False)
     await ctx.send(embed=embed)
