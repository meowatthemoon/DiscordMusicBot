import discord
from discord import Interaction
from discord.ui import  Modal, TextInput
import wavelink

from config import SEARCH_SONG_ITEMS_PER_PAGE
from cogs.music.pagination_menu import PaginationMenu

class SongSearchModal(Modal, title = "What song do you want to search for?"):
    def __init__(self, callback : callable):
        super().__init__(timeout = None)
        self.callback_fn : callable = callback

    song_name = TextInput(
        style = discord.TextStyle.short,
        label = "Song Name",
        required = True,
        placeholder = "Name"
    )

    async def on_submit(self, interaction : Interaction):
        user = interaction.user
        query = self.song_name.value

        tracks = await wavelink.Playable.search(query)

        if len(tracks) == 0:
            return await interaction.response.send_message(f"<@{user.id}>  I did not find any songs that match your query.", ephemeral = True, delete_after = 5)
        
        pagination_menu = PaginationMenu(tracks = tracks, items_per_page = SEARCH_SONG_ITEMS_PER_PAGE, callback = self.callback_fn)
        await interaction.response.send_message(content = pagination_menu.get_page(), view = pagination_menu)

    async def on_error(self, interaction : Interaction, error):
        print("MODAL error", error)

    async def on_timeout(self, interaction : Interaction):
        print("MODAL tiemout")
