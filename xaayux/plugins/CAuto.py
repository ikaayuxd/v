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
                chat_username = parts[3]
                message_id = parts[4]

                # Get the entity of the channel from the link
                chat_entity = await client.get_input_entity(chat_username)

                # Get the message object
                message = await client.get_messages(chat_entity, ids=message_id)

                # Get the InputMessage object for forwarding
                input_message = client.get_input_entity(message)

            except Exception as e:
                logging.error(f"Error getting message from link: {e}")
                continue

            # Forward the message (handling media and text separately)
            try:
                if message.media: # Check if the message has media
                    if isinstance(message.media, types.MessageMediaPhoto):
                        await client.send_file(channel_id, message.media.photo, caption=message.text)
                    elif isinstance(message.media, types.MessageMediaDocument):
                        await client.send_file(channel_id, message.media.document, caption=message.text)
                    elif isinstance(message.media, types.MessageMediaVideo):
                        await client.send_file(channel_id, message.media.video, caption=message.text)
                    # Add more conditions for other media types as needed
                    else:
                        await client.send_message(channel_id, message.text, file=message.media) # For other media types
                else: # If the message doesn't have media
                    await client.send_message(channel_id, message.text) # Just send the text

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
