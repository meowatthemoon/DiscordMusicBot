import discord
from discord import ButtonStyle, Interaction, ButtonStyle, Interaction
from discord.ui import View
from wavelink import Playable
from config import NOTIFICATION_EXPIRATION_TIME
from cogs.music.utils import emote_from_index

class PaginationMenu(View):
    def __init__(self, tracks : list[Playable], callback : callable, items_per_page : int = NOTIFICATION_EXPIRATION_TIME):
        super().__init__(timeout = None)
        
        self.callback_fn : callable = callback
        self.items_per_page : int = items_per_page
        self.pivot : int = 0

        self.tracks : list[Playable] = tracks
        assert len(self.tracks) > 0, "[PaginationMenu] Received 0 options to display."

    def get_page(self, header : str = "") -> str:        
        start_idx = self.pivot
        end_idx = min(start_idx + self.items_per_page, len(self.tracks))
        
        content = ""
        for i in range(start_idx, end_idx):
            index = i - start_idx
            content += f"{emote_from_index(index = index)} - {self.tracks[i].title}\n"
            
        content = f"{header}\n{content}" if header != "" else content
        return content
    
    # ----------------------------------- Buttons ----------------------------------- 
    @discord.ui.button(emoji= "1️⃣",row = 0, style = ButtonStyle.blurple)
    async def button_1(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "2️⃣", row = 0, style = ButtonStyle.blurple)
    async def button_2(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 1]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "3️⃣", row = 0, style = ButtonStyle.blurple)
    async def button_3(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 2]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "4️⃣", row = 0, style = ButtonStyle.blurple)
    async def button_4(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 3]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "5️⃣", row = 0, style = ButtonStyle.blurple)
    async def button_5(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 4]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "6️⃣", row = 1, style = ButtonStyle.blurple)
    async def button_6(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 5]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "7️⃣", row = 1, style = ButtonStyle.blurple)
    async def button_7(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 6]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "8️⃣", row = 1, style = ButtonStyle.blurple)
    async def button_8(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 7]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "9️⃣", row = 1, style = ButtonStyle.blurple)
    async def button_9(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 8]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(emoji = "🔟", row = 1, style = ButtonStyle.blurple)
    async def button_10(self, interaction : Interaction, button : discord.ui.Button):
        track = self.tracks[self.pivot + 9]
        await self.callback_fn(interaction = interaction, track = track, object = self)

    @discord.ui.button(label = "▪️", row = 2, style = ButtonStyle.gray, disabled = True)
    async def button_placeholder1(self, interaction : Interaction, button : discord.ui.Button):
        pass

    @discord.ui.button(label = "⬅️", row = 2, style = ButtonStyle.green, disabled = True)
    async def button_previous(self, interaction : Interaction, button : discord.ui.Button):
        self.pivot = max(0, self.pivot - self.items_per_page)

        self.button_previous.disabled = self.pivot == 0
        self.button_next.disabled = self.pivot + self.items_per_page >= len(self.tracks)
        await interaction.response.edit_message(content = self.get_page(), view = self)
    
    @discord.ui.button(label = "▪️", row = 2, style = ButtonStyle.gray, disabled = True)
    async def button_placeholder2(self, interaction : Interaction, button : discord.ui.Button):
        pass

    @discord.ui.button(label = "➡️", row = 2, style = ButtonStyle.green)
    async def button_next(self, interaction : Interaction, button : discord.ui.Button):
        if self.pivot + self.items_per_page < len(self.tracks):
            self.pivot += self.items_per_page

        self.button_previous.disabled = self.pivot == 0
        self.button_next.disabled = self.pivot + self.items_per_page >= len(self.tracks)
        await interaction.response.edit_message(content = self.get_page(), view = self)

    @discord.ui.button(label = "▪️", row = 2, style = ButtonStyle.gray, disabled = True)
    async def button_placeholder3(self, interaction : Interaction, button : discord.ui.Button):
        pass
