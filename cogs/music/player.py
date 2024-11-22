import discord
from discord import ButtonStyle, Interaction, Member, Message, VoiceChannel
from discord.ui import View
from wavelink import Playable, Player
from cogs.music.queue import Queue

class PlayerMenu(View):
    def __init__(self):
        super().__init__(timeout = None)
        self.__queue : Queue = Queue()
        self.__display_message : Message = None

        self.__is_playing = False
        self.__voice_channel : VoiceChannel = None
        self.__vc : Player = None

    def set_message(self, message : Message):
        self.__display_message = message

    async def queue_track(self, track : Playable, user : Member) -> bool:
        joined = await self.__join_voice_channel(user = user)
        if not joined:
            return False
        
        print("Joined vc")
     
        added = self.__queue.add_track(track)
        if not added:
            print("Failed to add track to queue.")
            return False
        
        print("Queing track...")

        return await self.__play()
    
    async def play_next_track(self) -> bool:
        self.__is_playing = False
        print("Playing next track...")
        if self.__queue.is_empty():
            await self.__display(text = "")
            print("Queue is empty.")
            return False

        return await self.__play()
    
    async def __join_voice_channel(self, user : Member) -> bool:
        if not getattr(user.voice, 'channel', None):
            return False
        
        new_channel = user.voice.channel
        if self.__voice_channel is None or new_channel.id != self.__voice_channel.id:
            self.__voice_channel = new_channel
            self.__vc : Player = await self.__voice_channel.connect(cls = Player)

        return True
    
    async def __display(self, text : str):
        await self.__display_message.edit(content = text)

    async def __play(self) -> bool:
        if self.__is_playing:
            return True
        
        track = self.__queue.get_next_track()

        url = track.uri

        print(f"Playing {url}")

        await self.__display(text = url)
        await self.__vc.play(track)
        self.__is_playing = True

        return True

    @discord.ui.button(emoji = "⏮", row = 0, style = ButtonStyle.blurple)
    async def button_previous(self, interaction : Interaction, button : discord.ui.Button):
        if self.__is_playing and len(self.__queue.get_history_tracks()) > 0:
            self.__queue.skip_by(jump = -2)
            await self.__vc.stop()
            self.__is_playing = False
        await interaction.response.defer()

    @discord.ui.button(emoji = "⏸", row = 0, style = ButtonStyle.blurple)
    async def button_pause(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None:
            await self.__vc.pause(True)
        await interaction.response.defer()
        
    @discord.ui.button(emoji = "▶", row = 0, style = ButtonStyle.blurple)
    async def button_resume(self, interaction : Interaction, button : discord.ui.Button):
        if self.__vc is not None:
            await self.__vc.pause(False)
        await interaction.response.defer()        

    @discord.ui.button(emoji = "⏭", row = 0, style = ButtonStyle.blurple)
    async def button_next(self, interaction : Interaction, button : discord.ui.Button):
        if self.__is_playing:
            await self.__vc.stop()
            self.__is_playing = False
        await interaction.response.defer()

    @discord.ui.button(emoji = "⏹", row = 0, style = ButtonStyle.blurple)
    async def button_stop(self, interaction : Interaction, button : discord.ui.Button):
        self.__queue.reset()

        if self.__vc is not None:
            await self.__vc.stop()
            await self.__vc.disconnect()

        self.__is_playing : bool = False
        self.__voice_channel : VoiceChannel = None
        self.__vc : Player = None

        await self.__display(text = "")
        await interaction.response.defer()

    @discord.ui.button(emoji = "🔄", row = 1, style = ButtonStyle.blurple)
    async def button_replay(self, interaction : Interaction, button : discord.ui.Button):
        if self.__is_playing:
            self.__queue.skip_by(jump = -1)
            await self.__vc.stop()
            self.__is_playing = False
        await interaction.response.defer()

    @discord.ui.button(emoji = "🔀", row = 1, style = ButtonStyle.blurple)
    async def button_shuffle(self, interaction : Interaction, button : discord.ui.Button):
        self.__queue.shuffle()
        await interaction.response.defer()
