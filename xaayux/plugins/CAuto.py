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

                # Create the InputMessage object for forwarding
                input_message = types.InputMessage(
                    peer=chat_entity, # The channel/group where the message is from
                    id=message_id, # The message ID
                    message=message.message, # The message text
                    entities=message.entities, # Any entities (e.g., links, hashtags)
                    reply_to_msg_id=message.reply_to_msg_id, # If it's a reply
                )

                # Handle media separately
                if message.media:
                    if isinstance(message.media, types.MessageMediaPhoto):
                        input_message.media = types.InputMediaPhoto(message.media.photo) 
                    elif isinstance(message.media, types.MessageMediaDocument):
                        input_message.media = types.InputMediaDocument(message.media.document)
                    elif isinstance(message.media, types.MessageMediaVideo):
                        input_message.media = types.InputMediaVideo(message.media.video)
                    # Add more conditions for other media types as needed
                    else:
                        input_message.media = message.media 

            except Exception as e:
                logging.error(f"Error getting message from link: {e}")
                continue

            # Forward the message (handling media and text separately)
            try:
                await client.send_message(channel_id, input_message) # Send with media
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
