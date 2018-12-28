import os
import shutil
import time
import zipfile

import discord
import requests
import schedule
from discord import RequestsWebhookAdapter, Webhook


def date():
    return time.strftime("%d_%B_%Y")

def webhook(project,failed):
    webhook = Webhook.partial(Webhook ID, 'TOKEN', adapter=RequestsWebhookAdapter())
    if failed == True:
        embed=discord.Embed(title="Build Failed.",color=0xFF0000)
        embed.add_field(name=project,value="Nightly failed to build")
        embed.set_footer(text="Made by Apple#1337")
        webhook.send(embed=embed, username='Nightly Builder')
    else:
        embed=discord.Embed(title="Building done",color=0x00FF00)
        embed.add_field(name=project,value="Nightly successfully built")
        embed.set_footer(text="Made by Apple#1337")
        webhook.send(embed=embed, username='Nightly Builder')
        webhook.send(file=discord.File(f"../../Build/Goldleaf.nro_{date()}.zip"),username='Nightly Builder')
        webhook.send(file=discord.File(f"../../Build/Goldleaf.nsp_{date()}.zip"),username='Nightly Builder')


def GoldLeaf():
    print("[SCRIPT] Changing Dir")
    os.chdir("Goldleaf/Goldleaf")
    print("[SCRIPT] Making clean")
    os.system("make clean")
    print("[SCRIPT] Git pull")
    os.system("git pull --all")
    print("[SCRIPT] Building")
    os.system("./Generate-linux.sh")
    print("[SCRIPT] Making Goldleaf zip")
    try:
        shutil.move("Output/Goldleaf.nro","../../Build/nro/Goldleaf.nro")
        shutil.move("Output/Goldleaf.nsp","../../Build/nsp/Goldleaf.nsp")
        shutil.make_archive(f"../../Build/Goldleaf.nsp_{date()}","zip","../../Build/nsp")
        shutil.make_archive(f"../../Build/Goldleaf.nro_{date()}","zip","../../Build/nro")
        webhook("Goldleaf",failed=False)
        os.chdir("../..")
    except FileNotFoundError:
        print("[SCRIPT] No files to move")
        webhook("Goldleaf",failed=True)
        return

#Build GoldLeaf at 21:00
schedule.every().day.at("21:00").do(GoldLeaf)
print("Script is now running")
while True:
    schedule.run_pending()
    time.sleep(60) 
