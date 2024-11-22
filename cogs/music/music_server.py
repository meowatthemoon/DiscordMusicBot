from discord import ButtonStyle, Interaction, TextChannel
from discord.ui import Button, View
import discord
from wavelink import Playable

from config import NOTIFICATION_EXPIRATION_TIME
from cogs.music.player import PlayerMenu
from cogs.music.pagination_menu import PaginationMenu
from cogs.music.search_modal import SongSearchModal

class SearchSongView(View):
    def __init__(self, callback : callable):
        super().__init__(timeout = None)

        self.callback_fn : callable = callback

    @discord.ui.button(emoji = "🔎", row = 0, style = ButtonStyle.green)
    async def button_search(self, interaction : Interaction, button : Button):
        song_search_modal = SongSearchModal(callback = self.callback_fn)
        await interaction.response.send_modal(song_search_modal)

class MusicServer:
    def __init__(self):
        self.server_name : str = "music-bot"
        self.player : PlayerMenu = None
        self.text_channel : TextChannel = None

    async def setup(self, interaction : Interaction):        
        text_channels = interaction.guild.text_channels
        await interaction.response.defer()
        #await interaction.response.send_message(content = "Started", delete_after = 1)

        channel_names = [str(channel) for channel in text_channels]
        if self.server_name not in channel_names:
            self.text_channel = await interaction.guild.create_text_channel(self.server_name)
        else:
            self.text_channel = text_channels[channel_names.index(self.server_name)]
        
        await self.text_channel.purge()

        dropdown_view = SearchSongView(callback = self.on_track_selection_callback)
        await self.text_channel.send(content = " ", view = dropdown_view)

        self.player = PlayerMenu()
        self.player.set_message(message = await self.text_channel.send(content = "", view = self.player))

    async def on_track_selection_callback(self, interaction : Interaction, track : list[Playable], object : PaginationMenu):
        del object            
        
        queued = await self.player.queue_track(track = track, user = interaction.user)
        await interaction.message.edit(content = "", delete_after = 0.1)
        if queued:            
            await interaction.channel.send(content = f"<@{interaction.user.id}> Added {track.title} to the Queue.", delete_after = NOTIFICATION_EXPIRATION_TIME)
        else:
            await interaction.channel.send(content = f"<@{interaction.user.id}> Failed to add {track.title} to the Queue.", delete_after = NOTIFICATION_EXPIRATION_TIME)

    async def song_ended_notification(self):
        await self.player.play_next_track()
        
