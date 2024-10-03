from .. import client, DELAY
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputPeerChannel
from telethon import events, types
import logging 
import asyncio
import random
from xaayux.config import channel_ids, messages, DELAY, group_ids

groups = 'groups.txt'
with open(groups, 'r') as file:
        group_ids = [line.strip() for line in file]
    
async def send_messages():
    while True:
        for group_id in group_ids:
            try:
                message = random.choice(messages)
                await client.send_message(int(group_id), message)
                await asyncio.sleep(2)
                await client.send_message(5488677608, f" Sent message to group {group_id}")
            except Exception as e:
                await client.send_message(5488677608, f"Error sending message to group {group_id}: {e}")
                
                
@client.on(events.NewMessage(outgoing=True, pattern='!cancel'))
async def handle_cancel(event):
    await event.respond('Cancelling Auto Message Forwarding...')
    global send_task
    send_task.cancel()

@client.on(events.NewMessage(outgoing=True, pattern='!start'))
async def handle_start(event):
    await event.respond("Starting Auto Message Forwarding...")
    global send_task
    send_task = asyncio.create_task(send_messages())

logging.basicConfig(level=logging.WARNING)

with client:
    client.run_until_disconnected()
