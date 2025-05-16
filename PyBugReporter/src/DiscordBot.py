import asyncio
import discord

HISTORY_LIMIT = 20
EMOJI = "‼"

class DiscordBot(discord.Client):
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = int(channel_id)
        self._message = None
        self._alreadySent = False
        self._done_future = None

        intents = discord.Intents(emojis = True,
                                  guild_reactions = True,
                                  message_content = True,
                                  guild_messages = True,
                                  guilds = True)
        super().__init__(intents=intents)

    async def send_message(self, message, alreadySent = False):
        self._message = message
        self._alreadySent = alreadySent
        self._done_future = asyncio.get_running_loop().create_future()
        print("Starting bot...")
        # Start the bot as a background task
        asyncio.create_task(self.start(self.token))
        # Wait until the message is sent and the bot is closed
        await self._done_future

    async def on_ready(self):
        try:
            channel = await self.fetch_channel(self.channel_id)
            if channel and not self._alreadySent:
                await channel.send(self._message)
                print(f"Sent message to channel {self.channel_id}")
            elif channel and self._alreadySent:
                async for message in channel.history(limit=HISTORY_LIMIT):
                    if message.content == self._message:
                        await message.add_reaction(EMOJI)
                        break
            else:
                print(f"Channel with ID {self.channel_id} not found.")
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            print("Shutting down bot...")
            await self.close()
            # Mark the future as done so send_message can return
            if self._done_future and not self._done_future.done():
                self._done_future.set_result(True)