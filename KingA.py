import os
import json
if not os.path.exists('king.json'):
    data = {}
    with open('king.json', 'w') as f:
        json.dump(data, f)
        print('Done Make DB')

import asyncio
import datetime
import json
import random
import re
import requests
import time
import telethon
from telethon import events
from telethon import TelegramClient, Button
from telethon.errors import FloodWaitError, SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl import functions, types
from telethon.tl.functions.channels import (
    JoinChannelRequest, LeaveChannelRequest, InviteToChannelRequest, GetParticipantRequest
)
import uuid
from telethon.tl.types import InputPeerChannel, PeerChannel
from telethon.utils import get_display_name
from telethon.tl.functions.messages import ImportChatInviteRequest
from LibHus.Telegram import TelegramBot
from telethon.tl.types import MessageActionGiftCode  
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import InputPeerUser
from collections import defaultdict
    

api_id = 21048240
api_hash = '9763ac67359380cfeee42f382b094ea9'
bot_token = "7540190288:AAEc6doRPArayrMA5DG9L8C0dMckU3sEsx8"
bot = TelegramClient('numper', api_id, api_hash).start(bot_token=bot_token)
client = TelegramBot(bot_token)
dev = '5530032728' #Your ID
#••••••••••••••••••#



def get_user_message(user_id):
    user_points = {'5530032728': 100, 'USER_ID_2': 50}  
    points = user_points.get(user_id, 0)
    return (
        f'🤖︙** مرحبا بك عزيزي في بوت الحسابات** \n'
        f'🚀︙بوت بيع و شراء الحسابات الوهميه \n'
        f'💰︙رصيدك : {points} $\n'
        f'**✅︙يرجي استخدام الازرار التالية :-**'
    )


user_buttons = [
    [Button.inline('-️ شراء رقم ✅ .', b'show_accounts')],
    [Button.inline('- الدعم الفني 🚀.', b'support'), Button.inline('- شراء نقاط 💰.', b'syaovoy')],
    [Button.inline('-️ تحويل رصيد ♻️', b'transfer_points')],
]


 
authorized_users = ["5530032728"]  


user_points = defaultdict(int)



authorized_users = {'5530032728'}


pending_admin_request = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = str(event.sender_id)  
    admin_message = '🚀︙** مرحبا بك عزيزي المالك**'
    admin_buttons = [
        [Button.inline('اضافة رقم بلد', b'addnum')],
        [Button.inline('حذف رقم بلد', b'delnum')],
        [Button.inline('إضافة نقاط لعضو', b'add_points')],
        [Button.inline('إضافة ادمن', b'add_admin')],
        [Button.inline('حذف ادمن', b'remove_admin')],
    ]
    
    
    user_points = {'5530032728': 100, 'USER_ID_2': 50}  
    points = user_points.get(user_id, 0)
    user_message = (
        f'🤖︙** مرحبا بك عزيزي في بوت الحسابات** \n'
        f'🚀︙بوت بيع و شراء الحسابات الوهميه \n'
        f'💰︙رصيدك : {points} $\n'
        f'**✅︙يرجي استخدام الازرار التالية :-**'
    )
    user_buttons = [
        [Button.inline('-️ شراء رقم ✅ .', b'show_accounts')],
        [Button.inline('- الدعم الفني 🚀.', b'support'), Button.inline('- شراء نقاط 💰.', b'syaovoy')],
        [Button.inline('-️ تحويل رصيد ♻️', b'transfer_points')],
    ]
    
    
    if user_id in authorized_users:
        await event.respond(admin_message, buttons=admin_buttons)
        await event.respond(user_message, buttons=user_buttons)
    else:
        await event.respond(user_message, buttons=user_buttons)

@bot.on(events.CallbackQuery(pattern=b'add_admin'))
async def add_admin(event):
    global pending_admin_request
    if str(event.sender_id) in authorized_users:
        pending_admin_request[event.sender_id] = 'add'
        await event.respond('🔄︙ الرجاء إرسال ID الشخص الذي تريد إضافته كإداري.')
    else:
        await event.respond('❌︙ ليس لديك الصلاحية لاستخدام هذا الأمر.')

@bot.on(events.CallbackQuery(pattern=b'remove_admin'))
async def remove_admin(event):
    global pending_admin_request
    if str(event.sender_id) in authorized_users:
        pending_admin_request[event.sender_id] = 'remove'
        await event.respond('🔄︙ الرجاء إرسال ID الشخص الذي تريد حذفه كإداري.')
    else:
        await event.respond('❌︙ ليس لديك الصلاحية لاستخدام هذا الأمر.')

@bot.on(events.NewMessage(pattern=r'^\d+$'))
async def handle_admin_management(event):
    global pending_admin_request
    user_id = str(event.sender_id)
    if user_id in pending_admin_request:
        action = pending_admin_request[user_id]
        target_id = event.text
        
        if action == 'add':
            authorized_users.add(target_id)
            await event.respond(f'✅︙ تم إضافة ID {target_id} كإداري.')
            await bot.send_message(int(target_id), '🚀︙** مرحبا بك عزيزي المالك**', buttons=[
                [Button.inline('اضافة رقم بلد', b'addnum')],
                [Button.inline('حذف رقم بلد', b'delnum')],
                [Button.inline('إضافة نقاط لعضو', b'add_points')],
                [Button.inline('تحويل تمبلر', b'tsdhk')],
                [Button.inline('إضافة ادمن', b'add_admin')],
                [Button.inline('حذف ادمن', b'remove_admin')],
            ])
        elif action == 'remove':
            if target_id in authorized_users:
                authorized_users.remove(target_id)
                await event.respond(f'✅︙ تم حذف ID {target_id} كإداري.')
            else:
                await event.respond('❌︙ هذا المستخدم ليس إداريًا.')
    
        pending_admin_request.pop(user_id, None)



pending_add_points_request = False

@bot.on(events.CallbackQuery(pattern=b'add_points'))
async def add_points(event):
    global pending_add_points_request
    if event.sender_id == int(dev):
        pending_add_points_request = True
        await event.respond('👤︙ الرجاء إرسال ID الشخص وعدد النقاط المراد إضافتها (بالتفصيل، مثال: "123456 50")')
    else:
        await event.respond('❌︙ ليس لديك الصلاحية لاستخدام هذا الأمر.')


@bot.on(events.NewMessage(pattern=r'^(\d+)\s+(\d+)$'))
async def handle_add_points(event):
    global pending_add_points_request
    if event.sender_id == int(dev) and pending_add_points_request:
        try:
            user_id, points_to_add = map(int, event.text.split())
            user_id = str(user_id)  
            user_points[user_id] += points_to_add  
            
            await event.respond(f'🌟︙ تمت إضافة {points_to_add} نقطة للمستخدم ذو الـ ID {user_id}.')
            pending_add_points_request = False  
        except Exception as e:
            await event.respond('❌︙ حدث خطأ أثناء معالجة الطلب. الرجاء المحاولة مرة أخرى.')
            pending_add_points_request = False  
    elif event.sender_id != int(dev):
        await event.respond('❌︙ ليس لديك الصلاحية لاستخدام هذا الأمر.')


@bot.on(events.CallbackQuery(pattern=b'back'))
async def numgpv_button(event):
    user_id = str(event.sender_id)
    points = user_points[user_id]  
    
    await event.answer('تم الرجوع بنجاح ✅')
    await event.edit(
        f'🤖︙**مرحبا بك عزيزي في بوت الحسابات**\n'
        f'🚀︙بوت بيع وشراء الحسابات الوهمية\n'
        f'💰︙رصيدك: {points} $\n'
        f'**✅︙يرجى استخدام الأزرار التالية :-**',
        buttons=[
            [Button.inline('-️ شراء رقم ✅ .', b'show_accounts')],
            [Button.inline('- الدعم الفني 🚀.', b'support'), Button.inline('- شراء نقاط 💰.', b'syaovoy')],
            [Button.inline('-️ تحويل رصيد ♻️.', b'transfer_points')],
        ]
    )
@bot.on(events.CallbackQuery(pattern=b'syaovoy'))
async def nusjkvn(event):
    await event.edit(
        f'🤖︙**مرحبا بك عزيزي في قسم شراء نقاط**\n'
        f'**تواصل مع المالك لمعرفة الاسعار وشراء وتزويد رصيدك :-**',
        buttons=[
[Button.url('تواصل مع الدعم', url='https://t.me/kkin9')],

        ]
    )   
    

pending_transfer_request = {}

@bot.on(events.CallbackQuery(pattern=b'transfer_points'))
async def request_transfer_details(event):
    user_id = str(event.sender_id)
    pending_transfer_request[user_id] = 'awaiting_recipient'
    await event.respond('🔄︙ الرجاء إرسال ID الشخص المستلم.')

@bot.on(events.NewMessage(pattern=r'^\d+$'))
async def handle_transfer_request(event):
    global pending_transfer_request
    user_id = str(event.sender_id)
    
    if user_id in pending_transfer_request:
        request_status = pending_transfer_request[user_id]
        
        if request_status == 'awaiting_recipient':
            pending_transfer_request[user_id] = {'recipient_id': event.text, 'status': 'awaiting_amount'}
            await event.respond('🔄︙ الرجاء إرسال عدد النقاط التي تريد تحويلها.')
        elif request_status['status'] == 'awaiting_amount':
            recipient_id = pending_transfer_request[user_id]['recipient_id']
            amount = int(event.text)
            
            if amount < 1:
                await event.respond('❌︙ الحد الأدنى للتحويل هو 1 نقطة.')
                pending_transfer_request.pop(user_id, None)
                return
            
            sender_points = user_points.get(user_id, 0)
            
            if sender_points < amount:
                await event.respond('❌︙ ليس لديك نقاط كافية لإتمام التحويل.')
                pending_transfer_request.pop(user_id, None)
                return
            
            
            user_points[user_id] = sender_points - amount
            user_points[recipient_id] = user_points.get(recipient_id, 0) + amount
            
            await event.respond(f'✅︙ تم تحويل {amount} نقطة إلى ID {recipient_id}.')
            await bot.send_message(int(recipient_id), f'✅︙ لقد استلمت {amount} نقطة من ID {user_id}.')
            
            pending_transfer_request.pop(user_id, None)


@bot.on(events.NewMessage)
async def cancel_pending_requests(event):
    global pending_transfer_request
    user_id = str(event.sender_id)
    if user_id in pending_transfer_request:
        pending_transfer_request.pop(user_id, None)
            


async def initialize_client(apd, aph, ses):
    client = TelegramClient(StringSession(ses), apd, aph)
    await client.connect()
    return client
   

@bot.on(events.CallbackQuery(pattern=r"support"))
async def on_support(event):
    user_id = str(event.sender_id)
    
    async with bot.conversation(event.sender_id, timeout=300) as conv:
        try:
            await conv.send_message("ارسل الرسالة التي تريد إرسالها للمالك:")
            

            response = await conv.get_response()
            

            await bot.send_message(dev, f"رسالة جديدة من المستخدم {user_id}:\n{response.text}")
            

            await conv.send_message("تم إرسال رسالتك إلى المالك بنجاح!")
        except Exception as e:
            await conv.send_message(f"حدث خطأ أثناء محاولة الاتصال بالدعم: {str(e)}")
                               

def save_user_points():
    with open('points.json', 'w') as file:
        json.dump(user_points, file, indent=4)
        
def load_accounts():
    try:
        with open('king.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_accounts(accounts):
    with open('king.json', 'w') as file:
        json.dump(accounts, file, indent=4)


def get_accounts():
    return load_accounts()


def delete_account(phone_number):
    accounts = load_accounts()
    if phone_number in accounts:
        del accounts[phone_number]
        save_accounts(accounts)


def add_account(phone_number, info):
    accounts = load_accounts()
    accounts[phone_number] = info
    save_accounts(accounts)


def update_account(phone_number, info):
    accounts = load_accounts()
    if phone_number in accounts:
        accounts[phone_number].update(info)
        save_accounts(accounts)

async def show_accounts(event, user_id, page=0):
    accounts = get_accounts()
    if not accounts:
        return await event.answer("- لم يتم اضافة اي حسابات في البوت.", alert=True)
    
    
    per_row = 2  
    per_page = 90
    start = page * per_page
    end = start + per_page
    current_accounts = list(accounts.keys())[start:end]

    text = f"- اليك قائمة بحسابات البوت (صفحة {page + 1})\n"
    buttons = []
    
    row = []
    for count, phone_number in enumerate(current_accounts, start + 1):
        info = accounts[phone_number]
        country = info.get('country', 'غير محدد')
        price = int(info.get('price', 0))  
        
        
        if user_points.get(user_id, 0) >= price:
            button_text = f"{count}: {country} - ${price}"
            row.append(Button.inline(button_text, data=f"v:{phone_number}:{price}"))
        else:
            button_text = f"{count}: {country} - ${price} (نقاطك غير كافية)"
            row.append(Button.inline(button_text, data="disabled"))
        
        
        if len(row) >= per_row:
            buttons.append(row)
            row = []
    
    
    if row:
        buttons.append(row)
    
    nav_buttons = []
    if start > 0:
        nav_buttons.append(Button.inline("السابق", data=f"show_accounts:{page - 1}"))
    if end < len(accounts):
        nav_buttons.append(Button.inline("التالي", data=f"show_accounts:{page + 1}"))
    
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Button.inline("رجوع", data="back")])
    
    await event.edit(text, parse_mode='markdown', buttons=buttons)


@bot.on(events.CallbackQuery(pattern=r"show_accounts"))
async def on_show_accounts(event):
    user_id = str(event.sender_id)
    page_data = event.data.decode().split(":")
    page = int(page_data[1]) if len(page_data) > 1 else 0
    
    await show_accounts(event, user_id, page)



async def handle_phone_number_button(event, phone_number):
    accounts = get_accounts()
    if phone_number in accounts:
        info = accounts[phone_number]
        text = (
            f"- الحساب : `+{phone_number}`\n"
            f"- API ID : `{info.get('apd', 'N/A')}`\n"
            f"- API Hash : `{info.get('aph', 'N/A')}`\n"
            f"- Password : `{info.get('apoo', 'N/A')}`\n\n"
            "**• اختر من الأزرار ما تود فعله بهذا الحساب**"
        )

        keyboard = [
            [Button.inline("الحصول على الكود", data=f"get:{phone_number}")],
            [Button.inline(f"+{phone_number} | Delete ❌", data=f"del:{phone_number}")],
            [Button.inline("رجوع", data="back")]
        ]
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
    else:
        await event.answer("حدثت مشكلة أثناء جلب معلومات الحساب.", alert=True)

@bot.on(events.CallbackQuery(pattern=r"v:(.*)"))
async def on_buy_account(event):
    user_id = str(event.sender_id)
    data = event.data.decode().split(":")
    phone_number = data[1]
    price = int(data[2])
    
    if user_points.get(user_id, 0) < price:
        await event.answer("نقاطك غير كافية لشراء هذا الرقم.", alert=True)
    else:
        
        user_points[user_id] -= price
        save_user_points()
        
        await event.answer(f"لقد قمت بشراء الرقم {phone_number}.")
        await handle_phone_number_button(event, phone_number)
         

async def handle_delete_confirmation(event, phone_number):
    text = f"- الرقم : `+{phone_number}`\n\n**- هل أنت متأكد من حذف الرقم؟**"
    keyboard = [
        [Button.inline("الغاء ↩️", data="back"), Button.inline("حذف ❌", data=f"del_done:{phone_number}")]
    ]
    await event.edit(text, parse_mode='markdown', buttons=keyboard)

async def handle_delete_done(event, phone_number):
    accounts = get_accounts()
    if phone_number in accounts:
        del accounts[phone_number]
        save_accounts(accounts)
        await event.edit(f"- تم حذف الرقم `+{phone_number}` من قائمة الأرقام ✅", parse_mode='markdown', buttons=[[Button.inline("رجوع", data="back")]])
    else:
        await event.edit(f"- فشل حذف الرقم `+{phone_number}` من قائمة الأرقام ❌", parse_mode='markdown', buttons=[[Button.inline("رجوع", data="back")]])

async def get_code(api_id, api_hash, session):
    async with TelegramClient(StringSession(session), api_id, api_hash) as bot:
        async for message in bot.iter_messages(777000, limit=1):
            code_match = re.search(r'\b(\d{5})\b', message.text)
            if code_match:
                return code_match.group(1)
            else:
                return "لم يتم العثور"

async def handle_get_code(event, phone_number):
    accounts = get_accounts()
    if phone_number in accounts:
        info = accounts[phone_number]
        keyboard = [
            [Button.inline(f"+{phone_number} | Delete ❌", data=f"del:{phone_number}")],
            [Button.inline("العودة للقائمة الرئيسية", data="back")]
        ]
        try:
            api_id = info['apd']
            api_hash = info['aph']
            session = info['ses']
            code = await get_code(api_id, api_hash, session)
            
            
            delete_account(phone_number)
            
            text = (
                f"- الحساب : `+{phone_number}`\n"
                f"- API ID : `{info.get('apd', 'N/A')}`\n"
                f"- API Hash : `{info.get('aph', 'N/A')}`\n"
                f"- Password : `{info.get('apoo', 'N/A')}`\n"
                f"✅ الكود : `{code}`\n\n"
                "تم إيجاد الكود، سيتم إيقاف الاتصال بالحساب.. اختر إحدى الخيارات التي تناسبك"
            )
        except Exception as e:
            text = (
                f"- الحساب : `+{phone_number}`\n"
                f"- API ID : `{info.get('apd', 'N/A')}`\n"
                f"- API Hash : `{info.get('aph', 'N/A')}`\n"
                f"- Password : `{info.get('apoo', 'N/A')}`\n"
                "❌ لم يتم العثور على الكود."
            )
            print(e)  
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
    else:
        await event.answer("حدثت مشكلة أثناء جلب معلومات الحساب.", alert=True)

@bot.on(events.CallbackQuery(pattern=r"get:(.+)"))
async def on_get_code(event):
    phone_number = event.data.decode().split(":")[1]
    await handle_get_code(event, phone_number)

@bot.on(events.CallbackQuery(pattern='addnum'))
async def callback(event):
    mes = await event.edit('🚀︙Loading add number .....', buttons=[
        Button.inline("⦉ رجوع ✅ ⦊", b'back')
    ])  
    
    data = await mainlogin(event)
    with open('king.json', 'r+') as f:
        old_data = json.load(f)
        old_data.update(data)
        f.seek(0)
        json.dump(old_data, f, ensure_ascii=False, indent=4)

@bot.on(events.CallbackQuery(pattern='delnum'))
async def callback(event):
    global drunning
    drunning = True
    async with bot.conversation(event.sender_id, timeout=300) as conv:
        mes = await conv.send_message('**✅︙ارسل الرقم الذي تريد حذفه**', buttons=[[Button.inline("⦉ رجوع ⬅️ ⦊", data='back')]])
        
        while True:
            response = await conv.get_response()
            code = response.text
            
            with open('king.json', 'r') as f:
                data = json.load(f)
            
            if code in data:
                del data[code]
                with open('king.json', 'w') as f:
                    json.dump(data, f)
                await mes.edit('**⛔︙تم حذف الـرقم بنجاح**', buttons=[])
                break
            else:
                await mes.edit('**الـرقم غير موجود. حاول مرة أخرى أو اضغط على رجوع**', buttons=[[Button.inline("رجوع", data='back')]])

                

async def mainlogin(event):
    async with bot.conversation(event.sender_id, timeout=300) as conv:
        await conv.send_message(" ارسل الـ API ID لبدء تأكيد العملية •", buttons=[[Button.inline("رجوع ⬅️ ", data='back')]])
        api_id = (await conv.get_response()).text.strip()
        
        if api_id.lower() == "/start":
            return
        
        
        if not api_id.isdigit():
            await conv.send_message("API ID غير صالح. يرجى إدخال رقم صحيح.", buttons=[[Button.inline("رجوع", data='back')]])
            return
        
        await conv.send_message("- ارسل الـ API HASH لاكمال تأكيد العملية •", buttons=[[Button.inline("رجوع ", data='back')]])
        api_hash = (await conv.get_response()).text.strip()
        
        if api_hash.lower() == "/start":
            return
        
        
        if not api_hash.isalnum():
            await conv.send_message("API HASH غير صالح. يرجى إدخال رمز صحيح.", buttons=[[Button.inline("رجوع", data='back')]])
            return
        
        try:
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.connect()
            
            if not client.is_connected():
                await conv.send_message("لا يمكن إرسال الطلبات أثناء عدم الاتصال", buttons=[[Button.inline("رجوع", data='back')]])
                return
            
            if not await client.is_user_authorized():
                await conv.send_message("️- ارسل رقم الهاتف ", buttons=[[Button.inline("رجوع ⬅️ ", data='back')]])
                phone_number = (await conv.get_response()).text.strip()
                
                
                if not phone_number.startswith('+') or not phone_number[1:].isdigit():
                    await conv.send_message("رقم الهاتف غير صالح. يرجى إدخال رقم هاتف صحيح مع رمز الدولة (+).", buttons=[[Button.inline("رجوع", data='back')]])
                    return
                
                await client.send_code_request(phone_number)
                
                try:
                    await conv.send_message("- ارسل الكود المرسل للرقم من تطبيق Telegram •", buttons=[[Button.inline("رجوع ", data='back')]])
                    verification_code = (await conv.get_response()).text.strip()
                    
                    
                    if not verification_code.isdigit():
                        await conv.send_message("رمز التحقق غير صالح. يرجى إدخال رمز صحيح.", buttons=[[Button.inline("رجوع", data='back')]])
                        return
                    
                    await client.sign_in(phone_number, verification_code)
                
                except SessionPasswordNeededError:
                    await conv.send_message("- ارسل باسورد التحقق بخطوتين •", buttons=[[Button.inline("رجوع ⬅️ ", data='back')]])
                    password = (await conv.get_response()).text.strip()
                    await client.sign_in(password=password)
            
            session = client.session.save()
            
            
            await conv.send_message("- ارسل بلد الرقم", buttons=[[Button.inline(" رجوع ⬅️ ", data='back')]])
            country = (await conv.get_response()).text.strip()
            
            await conv.send_message(" ارسل سعر الرقم", buttons=[[Button.inline("رجوع ⬅️", data='back')]])
            price = (await conv.get_response()).text.strip()
            
            
            await conv.send_message("︙تم تاكيد الرقم بنجاح •", buttons=[[Button.inline(" رجوع ⬅️ ", data='back')]])
            
            return {phone_number: {'apd': api_id, 'aph': api_hash, 'ses': session, 'apoo': password, 'country': country, 'price': price}}
        
        except ValueError:
            await conv.send_message("API ID أو API HASH غير صالح. يرجى التحقق والمحاولة مرة أخرى.", buttons=[[Button.inline("رجوع", data='back')]])
        
        except Exception as e:
            await conv.send_message(f"حدث خطأ: {str(e)}", buttons=[[Button.inline("رجوع", data='back')]])
        
        finally:
            if client and client.is_connected():
                await client.disconnect()

bot.run_until_disconnected()
