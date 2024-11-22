import discord
from discord.ext import commands

from config import COGS_FOLDER, TOKEN, COMMAND_PREFIX

class Bot(commands.Bot):
    def __init__(self, prefix : str):
        super().__init__(command_prefix = prefix, case_insensitive = True, intents = discord.Intents.all())

    async def setup_hook(self):
        import os
        os.makedirs(COGS_FOLDER, exist_ok = True)

        cogs = [filename[:-3] for filename in os.listdir(COGS_FOLDER) if filename.endswith(".py")]
        for cog in cogs:
            await self.load_extension(f"cogs.{cog}")
            print(f"Loaded Cog : {cog}.")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        synced = await self.tree.sync() # To use slash commands
        print(f"#{len(synced)} Slash Commands Synched")
        print(f"Bot is ready, version: {discord.__version__}.")

def main():
    bot = Bot(prefix = COMMAND_PREFIX)
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
