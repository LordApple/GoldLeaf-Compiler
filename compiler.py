import os
import shutil
import time
import subprocess

import discord
import requests
import schedule
from discord import RequestsWebhookAdapter, Webhook


webhook_id = 1111111111111
webhook_token = "TOKEN"

def date():
    return time.strftime("%d_%B_%Y")

def SendWebhook(project,failed):
    webhook = Webhook.partial(webhook_id, webhook_token, adapter=RequestsWebhookAdapter())
    if failed == True:
        embed=discord.Embed(title="Build Failed.",color=0xFF0000)
        embed.add_field(name=project,value="Commit failed to build")
        embed.set_footer(text="Made by Apple#1337")
        webhook.send(embed=embed, username='GoldLeaf Builder')
    else:
        embed=discord.Embed(title="Building done",color=0x00FF00)
        embed.add_field(name=project,value="Commit successfully built")
        embed.set_footer(text="Made by Apple#1337")
        webhook.send(embed=embed, username='GoldLeaf Builder')
        webhook.send(file=discord.File(f"../../Build/Goldleaf.nro_{date()}.zip"), username='GoldLeaf Builder')
        webhook.send(file=discord.File(f"../../Build/Goldleaf.nsp_{date()}.zip"), username='GoldLeaf Builder')


def GoldLeaf():
    print("[SCRIPT] Changing Dir")
    os.chdir("Goldleaf/Goldleaf")
    print("[SCRIPT] Making clean")
    os.system("make clean")
    print("[SCRIPT] Building")
    os.system("rm -r ExeFs/main &> /dev/null")
    os.system("make")
    os.system("cp Output/Goldleaf.nso ExeFs/main")
    os.system("rm Output/Goldleaf.nso Output/Goldleaf.nsp")
    os.system("./BuildTools/hacbrewpack-linux -k BuildTools/keys.dat --exefsdir=ExeFs --romfsdir=RomFs --logodir=Logo --controldir=Control --nspdir=Output")
    os.system("mv Output/050032a5cf12e000.nsp Output/Goldleaf.nsp")
    print("[SCRIPT] Making Goldleaf zip")
    try:
        shutil.move("Output/Goldleaf.nro","../../Build/nro/Goldleaf.nro")
        shutil.move("Output/Goldleaf.nsp","../../Build/nsp/Goldleaf.nsp")
        shutil.make_archive(f"../../Build/Goldleaf.nsp_{date()}","zip","../../Build/nsp")
        shutil.make_archive(f"../../Build/Goldleaf.nro_{date()}","zip","../../Build/nro")
        SendWebhook("Goldleaf",failed=False)
        os.chdir("../..")
    except FileNotFoundError:
        print("[SCRIPT] No files to move")
        SendWebhook("Goldleaf",failed=True)
        os.chdir("../..")
        return

os.makedirs("Build",exist_ok=True)
os.makedirs("Build/nro",exist_ok=True)
os.makedirs("Build/nsp",exist_ok=True)
print("Script is now running")
while True:
    os.chdir("Goldleaf/Goldleaf")
    output = subprocess.check_output("git pull",shell=True)
    output = output.decode('utf-8').strip()
    if output == "Already up to date.":
        os.chdir("../..")
    else:
        webhook = Webhook.partial(webhook_id, webhook_token, adapter=RequestsWebhookAdapter())
        r = requests.get("https://api.github.com/repos/XorTroll/Goldleaf/git/refs/heads/master")
        if r.status_code == 200:
            try:
                js = r.json()
                Commit_SHA = js["object"]["sha"]
                embed=discord.Embed(title="Started Building",color=0x00FF00)
                embed.add_field(name="GoldLeaf",value="Started compiling latest commit",inline=False)
                embed.add_field(name="Commit SHA:",value=Commit_SHA,inline=False)
                webhook.send(embed=embed, username='GoldLeaf Builder')
            except:
                webhook.send("Failed to get commit SHA (Still going to compile)", username='GoldLeaf Builder')
        os.chdir("../..")
        GoldLeaf()
    time.sleep(120) 
