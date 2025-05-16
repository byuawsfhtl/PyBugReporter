import discord

HISTORY_LIMIT = 20
EMOJI = "‼"

class DiscordBot(discord.Client):
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = int(channel_id)
        self._message = None
        self._alreadySent = False

        intents = discord.Intents(emojis = True,
                                  guild_reactions = True,
                                  message_content = True,
                                  guild_messages = True,
                                  guilds = True)
        super().__init__(intents=intents)

    async def send_message(self, message, alreadySent = False):
        self._message = message
        self._alreadySent = alreadySent
        print("Starting bot...")
        await self.start(self.token)

    async def on_ready(self):
        channel = await self.fetch_channel(self.channel_id)
        if channel and not self._alreadySent:
            await channel.send(self._message)
            print(f"Sent message to channel {self.channel_id}")
        elif channel and self._alreadySent:
            historyIter = await channel.history(limit=HISTORY_LIMIT)
            for message in historyIter:
                if message.content == self._message:
                    await message.add_reaction(EMOJI)
                    break
        else:
            print(f"Channel with ID {self.channel_id} not found.")
        print("Shutting down bot...")
        await self.close()