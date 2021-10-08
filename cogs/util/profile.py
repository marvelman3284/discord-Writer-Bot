import discord, lib
from discord.ext import commands
from structures.db import Database
from structures.user import User
from structures.wrapper import CommandWrapper
from structures.guild import Guild

class Profile(commands.Cog, CommandWrapper):

    def __init__(self, bot):
        self.bot = bot
        self.__db = Database.instance()

    @commands.command(name="profile")
    @commands.guild_only()
    async def profile(self, context):
        """
        Displays your Writer-Bot profile information and statistics.
        """

        if not Guild(context.guild).is_command_enabled('profile'):
            return await context.send(lib.get_string('err:disabled', context.guild.id))

        user = User(context.message.author.id, context.guild.id, context)
        goals = {
            'daily': user.get_goal_progress('daily')
        }
        profile = {
            'lvlxp': user.get_xp_bar(),
            'words': user.get_stat('total_words_written'),
            'words_sprints': user.get_stat('sprints_words_written'),
            'sprints_started': user.get_stat('sprints_started'),
            'sprints_completed': user.get_stat('sprints_completed'),
            'sprints_won': user.get_stat('sprints_won'),
            'challenges_completed': user.get_stat('challenges_completed'),
            'daily_goals_completed': user.get_stat('daily_goals_completed'),
            'weekly_goals_completed': user.get_stat('weekly_goals_completed'),
            'monthly_goals_completed': user.get_stat('monthly_goals_completed'),
            'yearly_goals_completed': user.get_stat('yearly_goals_completed'),
        }

        embed = discord.Embed(title=user.get_name(), color=3066993)

        embed.add_field(name=lib.get_string('profile:lvlxp', user.get_guild()), value=profile['lvlxp'], inline=True)
        embed.add_field(name=lib.get_string('profile:words', user.get_guild()), value=profile['words'], inline=True)
        embed.add_field(name=lib.get_string('profile:wordssprints', user.get_guild()), value=profile['words_sprints'], inline=True)
        embed.add_field(name=lib.get_string('profile:sprintsstarted', user.get_guild()), value=profile['sprints_started'], inline=True)
        embed.add_field(name=lib.get_string('profile:sprintscompleted', user.get_guild()), value=profile['sprints_completed'], inline=True)
        embed.add_field(name=lib.get_string('profile:sprintswon', user.get_guild()), value=profile['sprints_won'], inline=True)
        embed.add_field(name=lib.get_string('profile:challengescompleted', user.get_guild()), value=profile['challenges_completed'], inline=True)
        embed.add_field(name=lib.get_string('profile:dailygoalscompleted', user.get_guild()), value=profile['daily_goals_completed'], inline=True)
        embed.add_field(name=lib.get_string('profile:weeklygoalscompleted', user.get_guild()), value=profile['weekly_goals_completed'], inline=True)
        embed.add_field(name=lib.get_string('profile:monthlygoalscompleted', user.get_guild()), value=profile['monthly_goals_completed'], inline=True)
        embed.add_field(name=lib.get_string('profile:yearlygoalscompleted', user.get_guild()), value=profile['yearly_goals_completed'], inline=True)


        # Send the message
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))