import discord, lib, time
from discord.ext import commands
from structures.generator import NameGenerator
from structures.user import User
from structures.wrapper import CommandWrapper
from structures.guild import Guild

class Generate(commands.Cog, CommandWrapper):

    def __init__(self, bot):
        self.bot = bot
        self._supported_types = ['char', 'place', 'land', 'idea', 'book', 'book_fantasy', 'book_horror', 'book_hp', 'book_mystery', 'book_rom', 'book_sf', 'prompt', 'face']
        self._urls = {
            'face': 'https://thispersondoesnotexist.com/image'
        }
        self._arguments = [
            {
                'key': 'type',
                'prompt': 'generate:argument:type',
                'required': True,
                'check': lambda content : content in self._supported_types,
                'error': 'generate:err:type'
            },
            {
                'key': 'amount',
                'required': False,
                'prompt': 'generate:argument:amount',
                'type': int
            }
        ]

    @commands.command(name="generate")
    @commands.guild_only()
    async def generate(self, context, type=None, amount=None):
        """
        Random generator for various things (character names, place names, land names, book titles, story ideas, prompts).
        Define the type of item you wanted generated and then optionally, the amount of items to generate.

        Examples:
            !generate char - generates 10 character names
            !generate place 20 - generates 20 fantasy place names
            !generate land - generates 10 fantasy land/world names
            !generate book - generates 10 general fiction book titles
            !generate book_fantasy - generates 10 fantasy book titles
            !generate book_sf - generates 10 sci-fi book titles
            !generate book_horror - generates 10 horror book titles
            !generate book_rom - generates 10 romance/erotic book titles
            !generate book_mystery - generates 10 mystery book titles
            !generate book_hp - generates 10 Harry Potter book title
            !generate idea - generates a random story idea
            !generate prompt - generates a story prompt
            !generate face - generates a random person's face
        """
        if not Guild(context.guild).is_command_enabled('generate'):
            return await context.send(lib.get_string('err:disabled', context.guild.id))

        user = User(context.message.author.id, context.guild.id, context)

        # If no amount specified, use the default
        if amount is None:
            amount = NameGenerator.DEFAULT_AMOUNT

        # Check the arguments are valid
        args = await self.check_arguments(context, type=type, amount=amount)
        if not args:
            return

        type = args['type'].lower()
        amount = int(args['amount'])

        # For faces, we want to just call an API url.
        if type == 'face':
            return await context.send(self._urls['face'] + '?t=' + str(int(time.time())))

        generator = NameGenerator(type, context)
        results = generator.generate(amount)
        join = '\n'

        # For prompts, add an extra line between them.
        if type == 'prompt':
            join += '\n'

        names = join.join(results['names'])

        return await context.send(user.get_mention() + ', ' + results['message'] + names)



def setup(bot):
    bot.add_cog(Generate(bot))