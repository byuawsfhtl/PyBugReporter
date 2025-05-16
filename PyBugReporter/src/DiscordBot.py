import discord

class DiscordBot(discord.Client):
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = int(channel_id)
        self._message = None

        intents = discord.Intents(emojis = True,
                                  guild_reactions = True,
                                  message_content = True,
                                  guild_messages = True,
                                  guilds = True)
        super().__init__(intents=intents)

    async def send_message(self, message):
        self._message = message
        print("Starting bot...")
        await self.start(self.token)

    async def on_ready(self):
        channel = self.get_channel(self.channel_id)
        if channel:
            await channel.send(self._message)
            print(f"Sent message to channel {self.channel_id}")
        else:
            print(f"Channel with ID {self.channel_id} not found.")
        print("Shutting down bot...")
        await self.close()