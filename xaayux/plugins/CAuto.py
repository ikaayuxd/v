from .. import client, DELAY
from telethon import events, types, Button
import logging 
import asyncio
import random
from xaayux.config import channel_ids, messages, DELAY

async def send_messages():
    while True:
        for channel_id in channel_ids:
            # Get the message from the link
            try:
                message_link = "https://t.me/ghjjhddh/307" # Replace with the actual link
                parts = message_link.split('/')
                chat_id = parts[3]
                message_id = parts[4]
                message = await client.get_messages(chat_id, ids=message_id)
            except Exception as e:
                logging.error(f"Error getting message from link: {e}")
                continue

            # Forward the message with media
            try:
                await client.forward_messages(channel_id, message)
            except Exception as e:
                logging.error(f"Error forwarding message: {e}")
                continue

        await asyncio.sleep(DELAY) # Send a message every 30 minutes 

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

with client:
    client.run_until_disconnected()
