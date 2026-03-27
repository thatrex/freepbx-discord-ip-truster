import discord
from discord import app_commands
import os
import ipaddress


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} is ready!")


bot = Bot()


def is_valid_ipv4(ip: str) -> bool:
    """Returns True if the string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


@bot.tree.command(name="iptrust", description="Trust an IPv4 address")
@app_commands.describe(ip="The IPv4 address to trust")
async def iptrust(interaction: discord.Interaction, ip: str):
    user = interaction.user
    is_valid = is_valid_ipv4(ip)

    if is_valid:
        print(f"IP trusted by {user} ({user.id}): {ip}")
        os.system(f'fwconsole firewall trust {ip}')
        os.system(f'fail2ban-client unban {ip}')
        await interaction.response.send_message(
            f"Successfully trusted (& unbanned) **`{ip}`**.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            'Please provide a valid IPv4 address. [Get your IP here.](https://api.ipify.org/?format=txt)',
            ephemeral=True
        )


@bot.tree.command(name="ipuntrust", description="Untrust an IPv4 address")
@app_commands.describe(ip="The IPv4 address to untrust")
async def ipuntrust(interaction: discord.Interaction, ip: str):
    user = interaction.user
    is_valid = is_valid_ipv4(ip)

    if is_valid:
        print(f"IP untrusted by {user} ({user.id}): {ip}")
        os.system(f'fwconsole firewall untrust {ip}')
        await interaction.response.send_message(
            f"Successfully untrusted **`{ip}`**.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            'Please provide a valid IPv4 address.',
            ephemeral=True
        )

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError(
            "DISCORD_TOKEN environment variable not set. Please set it before running the bot.")
    bot.run(token)
