import discord
from discord.ext import commands
import requests
import json

TOKEN = "MTM1NzA2MTY4MDgwNjM2NzM5NA.G3ZulM.KYyND3qCp6acbPOwTeDisrhMWDu_DVG-ljX-ac"
EMAILJS_SERVICE_ID = "service_3dkjqmy"
EMAILJS_TEMPLATE_ID = "template_mbq9swe"
EMAILJS_USER_ID = "1T4ye5IrmAOZ2nNuS"

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# Simpan data buyer
buyers = {}

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} sudah aktif!")

@bot.command()
async def kirim(ctx, email: str, persen: int):
    activation_code = str(persen)  # Kode aktivasi sesuai persentase
    buyers[email] = activation_code

    # Data untuk dikirim ke EmailJS
    email_data = {
        "service_id": "service_3dkjqmy" ,
        "template_id": "template_mbq9swe" ,
        "user_id": "1T4ye5IrmAOZ2nNuS" ,
        "template_params": {
            "to_email": email,
            "activation_code": activation_code,
           
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post("https://api.emailjs.com/api/v1.0/email/send", data=json.dumps(email_data), headers=headers)

    if response.status_code == 200:
        await ctx.send(f"Kode aktivasi untuk {email} berhasil dikirim via EmailJS!")
    else:
        await ctx.send(f"Gagal mengirim email ke {email}, cek kembali konfigurasi EmailJS.")

@bot.command()
async def cekstats(ctx, email: str):
    if email in buyers:
        await ctx.send(f"{email} telah aktivasi dengan kode {buyers[email]}.")
    else:
        await ctx.send(f"{email} belum melakukan aktivasi.")

@bot.command()
async def listbuyer(ctx):
    if buyers:
        buyer_list = "\n".join([f"{email}: {code}%" for email, code in buyers.items()])
        await ctx.send(f"Daftar buyer yang sudah aktivasi:\n{buyer_list}")
    else:
        await ctx.send("Belum ada buyer yang aktivasi.")

@bot.command()
async def cekpenjualan(ctx):
    total = len(buyers)
    await ctx.send(f"Total penjualan saat ini: {total} buyer.")

@bot.command()
async def help(ctx):
    commands_list = """
    **Daftar Perintah Bot:**
    `/kirim <email> <persen>` - Kirim kode aktivasi ke email buyer via EmailJS
    `/cekstats <email>` - Cek status aktivasi buyer
    `/listbuyer` - List semua buyer yang sudah aktivasi
    `/cekpenjualan` - Lihat total penjualan
    `/help` - Lihat semua command yang tersedia
    """
    await ctx.send(commands_list)

bot.run(TOKEN)
