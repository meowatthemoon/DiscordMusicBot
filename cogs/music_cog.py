import discord
from discord.ext import commands
from discord import Interaction, app_commands
import wavelink

from cogs.music.lavalink_utils import LavalinkManager
from cogs.music.music_server import MusicServer
from config import LAVALINK_LOCAL, LAVALINK_APPLICATION_FILE_PATH, LAVALINK_FILE_PATH, LAVALINK_HOST, LAVALINK_PASSWORD, LAVALINK_PORT

class MusicCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
        self.servers : dict = {}

        if LAVALINK_LOCAL:
            lavalink_manager : LavalinkManager = LavalinkManager(ip_address = LAVALINK_HOST, port = LAVALINK_PORT, password = LAVALINK_PASSWORD, application_yml_path = LAVALINK_APPLICATION_FILE_PATH, lavalink_file_path = LAVALINK_FILE_PATH)
            lavalink_manager.start_lavalink()

        self.bot.loop.create_task(self.node_connect())

    #-------------- Wave link block ----------------------------------#
    async def node_connect(self):
        await self.bot.wait_until_ready()

        node: wavelink.Node = wavelink.Node(
            uri = f"http://{LAVALINK_HOST}:{LAVALINK_PORT}", 
            password = LAVALINK_PASSWORD
        )
        await wavelink.Pool.connect(client = self.bot, nodes = [node])

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node : wavelink.Node):
        print(f'Bot and wavelink node ready.')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload):
        server = await self.__get_server_by_id(server_id = payload.player.guild.id)
        await server.song_ended_notification()

    #-------------- Servers -------------------------------------------#
    @app_commands.command(name = "setup_music", description = "Starts the Music Bot functionality.")
    async def setup_musicserver(self, interaction : Interaction):
        await self.__get_server(interaction = interaction)     

    async def __get_server(self, interaction : Interaction) -> MusicServer:
        server_id = str(interaction.guild.id)
        if server_id not in self.servers.keys():
            self.servers[server_id] = MusicServer()
            await self.servers[server_id].setup(interaction = interaction)
        return self.servers[server_id]
    
    async def __get_server_by_id(self, server_id : int) -> MusicServer:
        server_id = str(server_id)
        assert server_id in self.servers.keys()

        return self.servers[server_id]

    """
    # ---------------------- PROCESSING --------------------------#
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction : discord.Reaction, user : discord.Member):
        if user.bot:
            return
        server = await self.__get_server_by_id(server_id = reaction.message.guild.id)
        await server.process_reaction(reaction = reaction, user = user)
        await reaction.remove(user = user)

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        if message.author.bot:
            return
        server = await self.__get_server_by_id(server_id = message.guild.id)
        await server.process_message(message = message)
    """


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
