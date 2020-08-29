from discord.ext import tasks, commands
import os
import re
from dotenv import load_dotenv

from timer import is_wanted_hour
from scraper import find_new_sources
WANTED_HOUR = 2
TIME_FILE = 'time.txt'
SOURCE_FILE = 'sources.txt'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('BOUND_CHANNEL')
USERID = os.getenv('BOUND_USERID')


class MyCog(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = int(channel_id)
        self.channel = self.bot.get_channel(self.channel_id)
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    async def find_and_print(self):
        found_new_source = False
        sources = find_new_sources(SOURCE_FILE)
        if len(sources) > 0:
            found_new_source = True
            for source in sources:
                reformatted_source = reformat_source(source)
                self.channel = self.bot.get_channel(self.channel_id)
                await self.channel.send(reformatted_source)
        return found_new_source

    @tasks.loop(minutes=1)
    async def printer(self):
        if is_wanted_hour(WANTED_HOUR, TIME_FILE):
            await self.find_and_print()

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()


def reformat_source(source):
    new_string = source.replace('https://www.youtube.com/embed', 'https://youtu.be')
    reformatted_source = re.sub('(\\?ecver=\\d)', '', new_string)
    return reformatted_source


if __name__ == '__main__':
    discord_bot = commands.Bot(command_prefix='!')
    my_event = MyCog(discord_bot, CHANNEL)


    @discord_bot.command(name='update', help='force bot to look for sources')
    async def update(ctx):
        if ctx.author.id != int(USERID):
            await ctx.send("You dont have permission to do that.")
            return

        if await my_event.find_and_print():
            await ctx.send("Found new sources.")
        else:
            await ctx.send("Found nothing new.")


    @discord_bot.command(name='reset', help='resets bot storage')
    async def reset(ctx):
        if ctx.author.id != int(USERID):
            await ctx.send("You dont have permission to do that.")
            return

        if os.path.isfile(f'./{SOURCE_FILE}'):
            os.remove(SOURCE_FILE)

        if os.path.isfile(f'./{TIME_FILE}'):
            os.remove(TIME_FILE)

        await ctx.send("have successfully resetted the cache.")


    @discord_bot.event
    async def on_ready():
        print(f'Connected with user: {discord_bot.user.name}')


    discord_bot.run(TOKEN)

