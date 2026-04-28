import discord
from discord import app_commands
import math

# Konfigurasi Bot
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all()) # Mengaktifkan semua izin
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync() # Sinkronisasi perintah / ke Discord
        print(f"Slash Commands aktif untuk {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} Berhasil Online!')
    # Mengatur status bot (Playing Yass Store)
    await bot.change_presence(activity=discord.Game(name="Yass Store Tax Calc"))

# Perintah /after (Mencari Harga Jual)
@bot.tree.command(name="after", description="Cek harga jual agar kamu terima bersih")
async def after(interaction: discord.Interaction, net: int):
    gross = math.ceil(net / 0.7)
    embed = discord.Embed(
        title="📊 Kalkulator After Tax",
        description=f"Untuk menerima **{net:,} Robux**, harga jual harus:",
        color=0x2ecc71
    )
    embed.add_field(name="Harga Jual (Before Tax)", value=f"**{gross:,} Robux**", inline=False)
    await interaction.response.send_message(embed=embed)

# Perintah /before (Mencari Nominal Diterima)
@bot.tree.command(name="before", description="Cek berapa robux yang masuk ke akunmu")
async def before(interaction: discord.Interaction, gross: int):
    net = math.floor(gross * 0.7)
    embed = discord.Embed(
        title="📊 Kalkulator Before Tax",
        description=f"Jika pembeli membayar **{gross:,} Robux**, kamu menerima:",
        color=0x3498db
    )
    embed.add_field(name="Jumlah Bersih (After Tax)", value=f"**{net:,} Robux**", inline=False)
    await interaction.response.send_message(embed=embed)

# GANTI DENGAN TOKEN KAMU
bot.run('MASUKKAN_TOKEN_DISINI')
