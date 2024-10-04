from .. import client, DELAY
from telethon import events, types, Button
import logging 
import asyncio
import random
from xaayux.config import channel_ids, messages, DELAY
link = 'https://t.me/ghjjhddh/307'

logging.basicConfig(level=logging.INFO)

@client.on(events.NewMessage(outgoing=True, pattern='!cstop'))
async def handle_cancel(event):
    await event.respond('Stopping Auto Message Sending...')
    global send_task
    send_task.cancel()

@client.on(events.NewMessage(outgoing=True, pattern='!acsend'))
async def handle_start(event):
    await event.respond("Started Auto Message Sending...")
    global send_task
    send_task = asyncio.create_task(send_messages())

@client.on(events.NewMessage(outgoing=True, pattern='!csend'))
async def handle_start(event):
    await event.respond("Started Message Sending...")
    parts = link.split('/')
    username = parts[-2]
    message_id = int(parts[-1])
    
    entity = await client.get_entity(username)
    
    message = await client.get_messages(entity, ids=message_id)
    
    if message.media:
        # Send the media message without any forwarding information to all channels
        for channel_id in channel_ids:
            await client.send_file(channel_id, message.media, caption=message.text)
    else:
        # Send the text-only message without any forwarding information to all channels
        for channel_id in channel_ids:
            await client.send_message(channel_id, message.text, forward=False)
            
async def send_messages():
    while True:
        # Call the function to forward the message from the link
        await forward_message(link)
        
#---------------------------------------
async def forward_message(link):
    # Extract the channel username and message ID from the link
    parts = link.split('/')
    username = parts[-2]
    message_id = int(parts[-1])
    
    entity = await client.get_entity(username)
    
    message = await client.get_messages(entity, ids=message_id)
    
    if message.media:
        # Send the media message without any forwarding information to all channels
        for channel_id in channel_ids:
            await client.send_file(channel_id, message.media, caption=message.text)
    else:
        # Send the text-only message without any forwarding information to all channels
        for channel_id in channel_ids:
            await client.send_message(channel_id, message.text, forward=False)
            
async def send_messages():
    while True:
        await forward_message(link)
        
        await asyncio.sleep(DELAY)  # Send a message every 30 minutes 


#-------------------------

# -- Constants -- #
HELP = """
𝗔𝘂𝘁𝗼 𝗦𝗰𝗵𝗲𝗱𝘂𝗹𝗲𝗿 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
!start - Start Auto Scheduler 
!cancel - Stop Auto Scheduler 
!alive - Check If Bot Is Alive
!about - About The Bot 
!help - Help Message
"""

ABOUT_TXT = """
᪥ Name: 𝗔𝘂𝘁𝗼 𝗦𝗰𝗵𝗲𝗱𝘂𝗹𝗲𝗿 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗕𝘆 @xAaYux • @LegendxTricks
᪥ Library: [Telethon](https://docs.telethon.dev/)
᪥ Language: Python 3 
᪥ Dev: [⏤‌ＫＡＲＴＩＫ𓆩♡𓆪™|🇮🇳](https://t.me/xAaYux)
"""

@client.on(events.NewMessage(pattern='@LegendxTricks'))
async def get_group_id(event):
    # Get the group ID
    group_id = event.chat_id
    
    # Save the group ID to saved messages
    await client.send_message('me', f'Saved Group ID:`{group_id}`')
      
@client.on(events.NewMessage(outgoing=True, pattern='!about'))
async def about(event):
    await event.edit(ABOUT_TXT, link_preview=False)


@client.on(events.NewMessage(outgoing=True, pattern='!help'))
async def help_me(event):
    await event.edit(HELP)


@client.on(events.NewMessage(outgoing=True, pattern='!alive'))
async def alive(event):
    txt = await event.edit("▢▢▢▢▢▢")
    await event.edit("▣▢▢▢▢▢")
    await event.edit("▣▣▢▢▢▢")
    await event.edit("▣▣▣▢▢▢")
    await event.edit("▣▣▣▣▢▢")
    await event.edit("▣▣▣▣▣▢")
    await event.edit("▣▣▣▣▣▣")
    
    await event.edit(f"𝗔𝘂𝘁𝗼 𝗦𝗰𝗵𝗲𝗱𝘂𝗹𝗲𝗿 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗜𝘀 𝗔𝗰𝘁𝗶𝘃𝗲.\n\n𝗗𝗲𝗮𝗹𝘆 𝗜𝘀 𝗦𝗲𝘁 𝗧𝗼 {DELAY}(𝗦𝗲𝗰𝗼𝗻𝗱𝘀). \n\n @LegendxTricks")


with client:
    client.run_until_disconnected()
