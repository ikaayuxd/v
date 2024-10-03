from .. import client, DELAY
from telethon import events, types, Button
import logging 
import asyncio
import random
from xaayux.config import channel_ids, messages, DELAY

logging.basicConfig(level=logging.INFO)

@client.on(events.NewMessage(outgoing=True, pattern='!ccancel'))
async def handle_cancel(event):
    await event.respond('Cancelling Auto Message Forwarding...')
    global send_task
    send_task.cancel()

@client.on(events.NewMessage(outgoing=True, pattern='!cstart'))
async def handle_start(event):
    await event.respond("Starting Auto Message Forwarding...")
    global send_task
    send_task = asyncio.create_task(send_messages())

async def forward_message(link):
    # Extract the channel username and message ID from the link
    parts = link.split('/')
    username = parts[-2]
    message_id = int(parts[-1])
    
    entity = await client.get_entity(username)
    
    message = await client.get_messages(entity, ids=message_id)
    
    if message.media:
        # Forward the message with media (images/videos) to all channels
        for channel_id in channel_ids:
            await client.forward_messages(channel_id, message)
    else:
        # Forward the text-only message without the "Forwarded from" tag to all channels
        for channel_id in channel_ids:
            await client.send_message(channel_id, message.text)

async def send_messages():
    while True:
        link = 'https://t.me/ghjjhddh/307'  # Replace with your desired link
        
        # Call the function to forward the message from the link
        await forward_message(link)
        
        await asyncio.sleep(DELAY)  # Send a message every 30 minutes 

with client:
    client.run_until_disconnected()
