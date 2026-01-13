import pytz
import datetime
import asyncio
from Script import script 
from info import *
from utils import get_seconds, temp
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
PREMIUM_BOT_USERNAME = "PaymentGuardianBot" # Yahan apne Pay Bot ka username lagayein (bina @ ke)
# ---------------------

# ---------------------------------------------------------------
# READ-ONLY COMMANDS (Gatekeeper Logic)
# ---------------------------------------------------------------

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    try:
        user = message.from_user.mention
        user_id = message.from_user.id
        data = await db.get_user(user_id)

        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"

            caption = (
                f"⚜️ <b>ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :</b>\n\n"
                f"👤 <b>ᴜꜱᴇʀ :</b> {user}\n"
                f"⚡ <b>ᴜꜱᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n"
                f"⏰ <b>ᴛɪᴍᴇ ʟᴇꜰᴛ :</b> {time_left_str}\n"
                f"⌛️ <b>ᴇxᴘɪʀʏ ᴅᴀᴛᴇ :</b> {expiry_str_in_ist}"
            )
            # Extend Plan button now redirects to Pay Bot
            redirect_url = f"https://t.me/{PREMIUM_BOT_USERNAME}?start={user_id}"
            await message.reply_photo(
                photo=SUBSCRIPTION, 
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔥 ᴇxᴛᴇɴᴅ ᴘʟᴀɴ (Go to PayBot)", url=redirect_url)]]
                )
            )
        else:
            redirect_url = f"https://t.me/{PREMIUM_BOT_USERNAME}?start={user_id}"
            await message.reply_photo(
                photo="https://i.ibb.co/gMrpRQWP/photo-2025-07-09-05-21-32-7524948058832896004.jpg", 
                caption=(
                    f"<b>ʜᴇʏ {user},\n\n"
                    f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ.\n"
                    f"ʙᴜʏ ᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇꜰɪᴛꜱ.</b>"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("💎 ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ (Go to PayBot)", url=redirect_url)]]
                )
            )
    except Exception as e:
        print(f"Error in myplan: {e}")

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")
        else:
            await message.reply_text("ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /get_premium user_id")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>ꜰᴇᴛᴄʜɪɴɢ...</i>")
    new = f" ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ʟɪꜱᴛ :\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            try:
                expiry = data.get("expiry_time") 
                expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
                expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
                current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                time_left = expiry_ist - current_time
                days = time_left.days
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
                # Handling deleted accounts safely
                try:
                    user_obj = await client.get_users(user['id'])
                    user_mention = user_obj.mention
                except:
                    user_mention = "Deleted Account"
                    
                new += f"{user_count}. {user_mention}\n👤 ᴜꜱᴇʀ ɪᴅ : {user['id']}\n⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n\n"
                user_count += 1
            except Exception as e:
                print(f"Error fetching specific user: {e}")
                pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")

# ---------------------------------------------------------------
# REDIRECT LOGIC (The New "Plan" Command)
# ---------------------------------------------------------------

@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id
    
    # 1. Check DB (Read Only)
    # Agar user pehle se premium hai, toh usse khareedne ki zaroorat nahi
    data = await db.get_user(user_id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time")
        if expiry > datetime.datetime.now():
            await message.reply_text("✅ **You are already a Premium Member!**\nUse /myplan to check details.")
            return

    # 2. Redirect Link
    # Hum deep-linking use karenge: https://t.me/PayBot?start=userID
    redirect_url = f"https://t.me/{PREMIUM_BOT_USERNAME}?start={user_id}"

    btn = [
        [
            InlineKeyboardButton('💎 Buy Premium (Go to Cashier Bot)', url=redirect_url),
        ],
        [
            InlineKeyboardButton('🚫 Close', callback_data='close_data')
        ]
    ]
    
    await message.reply_photo(
        photo="https://graph.org/file/86da2027469565b5873d6.jpg",
        caption=script.BPREMIUM_TXT, # Make sure text doesn't say "Click button to pay here"
        reply_markup=InlineKeyboardMarkup(btn)
    )

# Note: add_premium, remove_premium, buy_callback, send_invoice, 
# successful_payment sab REMOVE kar diye gaye hain.
# Wo sab ab Premium Bot handle karega.
