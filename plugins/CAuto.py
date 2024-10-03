from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetMessagesRequest
import asyncio
import random
from xaayux.config import channel_ids, message_links, DELAY

# ... (Your client initialization and other imports)

async def send_messages():
    while True:
        for channel_id in channel_ids:
            message_link = random.choice(message_links)

            try:
                # Extract message ID and peer from the link
                parts = message_link.split("/")
                message_id = int(parts[-1])
                peer = parts[-2]

                # Fetch the message using its ID and peer
                original_message = await client(GetMessagesRequest(
                    peer=peer,
                    id=[message_id]
                ))
                original_message = original_message.messages[0]

                # Forward the message to the current channel
                await client.forward_messages(channel_id, original_message)

            except Exception as e:
                print(f"Error forwarding message from link '{message_link}': {e}")

        await asyncio.sleep(DELAY)

@client.on(events.NewMessage(outgoing=True, pattern='!ccancel'))
# ... (Your handle_cancel function - no changes needed) 

@client.on(events.NewMessage(outgoing=True, pattern='!cstart'))
# ... (Your handle_start function - no changes needed)

with client:
    client.run_until_disconnected()