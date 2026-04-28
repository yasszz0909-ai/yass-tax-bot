import discord
from discord import app_commands
import math
import os
from flask import Flask
from threading import Thread

# 1. SERVER UNTUK MENJAGA BOT TETAP HIDUP (KEEP ALIVE)
app = Flask('')

@app.route('/')
def home():
    return "Bot Yass Store sedang berjalan!"

def run():
    # Render menggunakan port 8080 secara default
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. KONFIGURASI BOT DISCORD
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Slash Commands aktif untuk {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} Berhasil Online!')
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
    embed.set_footer(text="Yass Store")
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
    embed.set_footer(text="Yass Store")
    await interaction.response.send_message(embed=embed)

# 3. JALANKAN SEMUANYA
if __name__ == "__main__":
    keep_alive() # Menjalankan server Flask di background
    # Gunakan os.getenv agar lebih aman di Render
    # Masukkan token baru hasil reset kamu di sini sementara
    bot.run('MTQ5ODUyMTkwNjc3MTM5ODgyNw.Gv5xjt.zFqZIacEcYNmPoe3kzrSJTJx8zx8Vg5jCimmfg')
