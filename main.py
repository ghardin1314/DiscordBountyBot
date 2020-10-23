import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

bounties = []
bountyID = [0]
approvedRoles = []
approvedRoleNames = ['TestRole', 'Admin']

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    #  Add roles here!
    for roleName in approvedRoleNames:
        role = discord.utils.find(lambda r: r.name == roleName, guild.roles)
        approvedRoles.append(role)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msgList = message.content.split(", ")

    print(message.author.roles)
    print(approvedRoles)

    # TODO: Check role of sender
    if '!bounty ' in msgList[0]:

        for role in approvedRoles:
            if role in message.author.roles:
                msgList[0] = msgList[0].replace('!bounty ', "")
                bounties.append((bountyID[0], msgList[0], msgList[1]))
                await message.channel.send("Bounty Saved!")
                bountyID[0] += 1

                return
        
        await message.channel.send("You don't have perssion for this action!")
        

    if '!bountyList' in msgList[0]:
        msg = "Here are the list of open bounties: \n"
        i = 0
        for bounty in bounties:
            msg = msg + "ID: " +  str(bounty[0]) + "\n    Task: " + bounty[1] + "\n    Reward: " + bounty[2] + "\n"
            i += i
        await message.channel.send(msg)

    if '!fulfillBounty ' in msgList[0]:
        msgList[0] = msgList[0].replace('!fulfillBounty ', "")
        found = False
        try:
            _id = int(msgList[0])
            for bounty in bounties:
                if _id == bounty[0]:
                    await message.channel.send("Successfully fufilled bounty #" + str(_id))
                    bounties.remove(bounty)
                    found = True
                    break

            if not found:
                await message.channel.send("Bounty ID not found")
                
        except:
            await message.channel.send("Please enter valid bounty ID")

client.run(TOKEN)