import discord

class DiscordBot(discord.Client):
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents(send_messages = True,
                                  change_nickname = True,
                                  emojis = True,
                                  guild_messages = True,)
        super(intents=intents)

    async def send_message(self, message):
        channel = self.get_channel(self.channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"Channel with ID {self.channel_id} not found.")

    def run(self):
        self.run(self.token)