from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()
import os
from telebot import TeleBot, types
import time

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

bot = TeleBot(TOKEN, parse_mode="HTML")

# ========== НАРХҲО ==========
ff_almaz = {
    "105":  {"uz": "10 500 so'm",  "tj": "11 сомонӣ"},
    "326":  {"uz": "32 600 so'm",  "tj": "28 сомонӣ"},
    "546":  {"uz": "54 600 so'm",  "tj": "45 сомонӣ"},
    "1113": {"uz": "111 300 so'm", "tj": "95 сомонӣ"},
    "2398": {"uz": "239 800 so'm", "tj": "185 сомонӣ"},
    "5600": {"uz": "560 000 so'm", "tj": "495 сомонӣ"},
}

ff_voucher = {
    "day":   {"name_uz": "1 kunlik",  "name_tj": "1 рӯза",  "almaz": 90,   "uz": "7 000 so'm",   "tj": "7 сомонӣ"},
    "week":  {"name_uz": "1 haftalik","name_tj": "1 ҳафта", "almaz": 450,  "uz": "20 000 so'm",  "tj": "20 сомонӣ"},
    "month": {"name_uz": "1 oylik",   "name_tj": "1 моҳа",  "almaz": 2600, "uz": "100 000 so'm", "tj": "100 сомонӣ"},
}

cards = {
    "uz": "📌 Esxata Online: 928146627\n📌 Dushanbe Siti: 928139091",
    "tj": "📌 Эсҳата Онлайн: 928146627\n📌 Душанбе Сити: 928139091"
}

ADMIN_ID = int(os.environ.get("ADMIN_ID", "6281678077"))

# State dictionaries
user_lang = {}
selected_item = {}
selected_price = {}
waiting_for_id = {}
last_order_chat_id = {}

# ========== МАТНҲО ==========
TEXTS = {
    "uz": {
        "lang_choice":       "Tilni tanlang / Забонро интихоб кунед:",
        "product_choice":    "FreeFire mahsulot turini tanlang:",
        "almaz":             "💎 Almaz",
        "voucher":           "🎫 Voucher",
        "almaz_select":      "Almaz miqdorini tanlang:",
        "voucher_select":    "Voucher tanlang:",
        "selected":          "✅ Tanlangan:",
        "price":             "💰 Narxi:",
        "pay":               "💳 TO'LOV",
        "pay_info":          "💳 To'lov ma'lumotlari:\n\n{cards}\n\n📦 {item}\n💰 Narxi: {price}\n\n✅ To'lov qilganingizdan keyin tugmani bosing:",
        "pay_btn":           "✅ To'landi",
        "chek_request":      "📸 Iltimos, to'lov chekini (skrinshot) tashlang:",
        "chek_ok":           "✅ Chek qabul qilindi! Admin tekshiradi...",
        "chek_error":        "❌ Iltimos, rasm (skrinshot) tashlang!",
        "ask_id":            "📝 Iltimos, FreeFire ID raqamingizni yozing:",
        "id_ok":             "✅ ID qabul qilindi!\n📦 {item}\n🆔 ID: {user_id}\n\n⏳ 1-2 daqiqadan so'ng hisobingizga almaz tushadi. Rahmat!",
        "id_sent_admin":     "✅ Foydalanuvchiga ID so'rash yuborildi!",
        "no_order":          "❌ Hali hech qanday buyurtma yo'q!",
        "admin_caption":     "🆕 YANGI BUYURTMA!\n📦 {item}\n💰 {price}\n👤 Foydalanuvchi: {name}\n🔗 Chat ID: {chat_id}\n\n➡️ ID so'rash uchun 'id' deb yozing",
        "admin_id_received": "🆔 ID keldi!\n📦 {item}\n🆔 FreeFire ID: {user_id}\n👤 Foydalanuvchi: {name}",
        "admin_help":        "📌 Admin buyruqlari:\n\n• id — oxirgi buyurtmadan ID so'rash\n• help — yordam",
    },
    "tj": {
        "lang_choice":       "Забонро интихоб кунед:",
        "product_choice":    "Навъи маҳсулоти FreeFire-ро интихоб кунед:",
        "almaz":             "💎 Алмаз",
        "voucher":           "🎫 Ваучер",
        "almaz_select":      "Миқдори алмазро интихоб кунед:",
        "voucher_select":    "Ваучерро интихоб кунед:",
        "selected":          "✅ Интихоб шуд:",
        "price":             "💰 Нарх:",
        "pay":               "💳 ПАРДОХТ",
        "pay_info":          "💳 Маълумоти пардохт:\n\n{cards}\n\n📦 {item}\n💰 Нарх: {price}\n\n✅ Пас аз пардохт тугмаро пахш кунед:",
        "pay_btn":           "✅ Пардохт кардам",
        "chek_request":      "📸 Лутфан, чеки пардохтро (скриншот) фиристед:",
        "chek_ok":           "✅ Чек қабул карда шуд! Админ текширад...",
        "chek_error":        "❌ Лутфан, расм (скриншот) фиристед!",
        "ask_id":            "📝 Лутфан, ID-и FreeFire-и худро нависед:",
        "id_ok":             "✅ ID қабул карда шуд!\n📦 {item}\n🆔 ID: {user_id}\n\n⏳ 1-2 дақиқа пас ҳисобингизга алмаз мерасад. Раҳмат!",
        "id_sent_admin":     "✅ Ба корбар ID пурсидан фиристода шуд!",
        "no_order":          "❌ Ҳанӯз ҳеҷ фармоише нест!",
        "admin_caption":     "🆕 ФАРМОИШИ НАВ!\n📦 {item}\n💰 {price}\n👤 Корбар: {name}\n🔗 Chat ID: {chat_id}\n\n➡️ Барои пурсидани ID 'id' нависед",
        "admin_id_received": "🆔 ID омад!\n📦 {item}\n🆔 FreeFire ID: {user_id}\n👤 Корбар: {name}",
        "admin_help":        "📌 Фармонҳои админ:\n\n• id — аз корбари охирин ID пурсед\n• help — ёри",
    }
}


# ========== HELPERS ==========
def get_lang(chat_id):
    return user_lang.get(chat_id, "uz")

def get_txt(chat_id):
    return TEXTS[get_lang(chat_id)]


# ========== START ==========
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🇺🇿 O'zbek",   callback_data="lang_uz"),
        types.InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj")
    )
    bot.send_message(message.chat.id, "Tilni tanlang / Забонро интихоб кунед:", reply_markup=keyboard)


# ========== CALLBACKS ==========
@bot.callback_query_handler(func=lambda call: True)
def query(call):
    chat_id = call.message.chat.id

    # --- Language selection ---
    if call.data in ["lang_uz", "lang_tj"]:
        lang = call.data.split("_")[1]
        user_lang[chat_id] = lang
        txt = TEXTS[lang]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(txt["almaz"],   callback_data="almaz"),
            types.InlineKeyboardButton(txt["voucher"], callback_data="voucher")
        )
        bot.edit_message_text(txt["product_choice"], chat_id, call.message.message_id, reply_markup=keyboard)

    # --- Almaz menu ---
    elif call.data == "almaz":
        txt = get_txt(chat_id)
        lang = get_lang(chat_id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for key in ["105", "326", "546", "1113", "2398", "5600"]:
            price = ff_almaz[key][lang]
            keyboard.add(types.InlineKeyboardButton(f"💎 {key} — {price}", callback_data=f"alm_{key}"))
        bot.edit_message_text(txt["almaz_select"], chat_id, call.message.message_id, reply_markup=keyboard)

    # --- Voucher menu ---
    elif call.data == "voucher":
        txt = get_txt(chat_id)
        lang = get_lang(chat_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for key in ["day", "week", "month"]:
            v = ff_voucher[key]
            name  = v["name_uz"] if lang == "uz" else v["name_tj"]
            price = v["uz"]      if lang == "uz" else v["tj"]
            keyboard.add(types.InlineKeyboardButton(
                f"🎫 {name} — {price} ({v['almaz']}💎)",
                callback_data=f"vou_{key}"
            ))
        bot.edit_message_text(txt["voucher_select"], chat_id, call.message.message_id, reply_markup=keyboard)

    # --- Almaz selected ---
    elif call.data.startswith("alm_"):
        key  = call.data.split("_")[1]
        lang = get_lang(chat_id)
        txt  = get_txt(chat_id)
        price = ff_almaz[key][lang]
        item  = f"FreeFire {key} almaz" if lang == "uz" else f"FreeFire {key} алмаз"
        selected_item[chat_id]  = item
        selected_price[chat_id] = price
        bot.answer_callback_query(call.id, f"{txt['selected']} {price}")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(txt["pay"], callback_data="pay"))
        bot.send_message(chat_id, f"{txt['selected']} {item}\n{txt['price']} {price}", reply_markup=keyboard)

    # --- Voucher selected ---
    elif call.data.startswith("vou_"):
        key  = call.data.split("_")[1]
        lang = get_lang(chat_id)
        txt  = get_txt(chat_id)
        v     = ff_voucher[key]
        name  = v["name_uz"] if lang == "uz" else v["name_tj"]
        price = v["uz"]      if lang == "uz" else v["tj"]
        item  = f"FreeFire {name} voucher ({v['almaz']}💎)" if lang == "uz" else f"FreeFire {name} ваучер ({v['almaz']}💎)"
        selected_item[chat_id]  = item
        selected_price[chat_id] = price
        bot.answer_callback_query(call.id, f"{txt['selected']} {price}")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(txt["pay"], callback_data="pay"))
        bot.send_message(chat_id, f"{txt['selected']} {item}\n{txt['price']} {price}", reply_markup=keyboard)

    # --- Pay button ---
    elif call.data == "pay":
        lang  = get_lang(chat_id)
        txt   = get_txt(chat_id)
        item  = selected_item.get(chat_id, "—")
        price = selected_price.get(chat_id, "—")
        text  = txt["pay_info"].format(cards=cards[lang], item=item, price=price)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(txt["pay_btn"], callback_data="chek"))
        bot.send_message(chat_id, text, reply_markup=keyboard)

    # --- Paid → ask screenshot ---
    elif call.data == "chek":
        txt = get_txt(chat_id)
        msg = bot.send_message(chat_id, txt["chek_request"])
        bot.register_next_step_handler(msg, receive_screenshot)


# ========== SCREENSHOT HANDLER ==========
def receive_screenshot(message):
    chat_id = message.chat.id
    txt   = get_txt(chat_id)
    lang  = get_lang(chat_id)
    item  = selected_item.get(chat_id, "—")
    price = selected_price.get(chat_id, "—")

    if message.photo:
        last_order_chat_id[ADMIN_ID] = chat_id
        caption = txt["admin_caption"].format(
            item=item,
            price=price,
            name=message.from_user.first_name or "—",
            chat_id=chat_id
        )
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
        bot.send_message(chat_id, txt["chek_ok"])
    else:
        msg = bot.send_message(chat_id, txt["chek_error"])
        bot.register_next_step_handler(msg, receive_screenshot)


# ========== ID RECEIVER (must be before admin_commands) ==========
@bot.message_handler(func=lambda message: waiting_for_id.get(message.chat.id, False))
def receive_id(message):
    chat_id  = message.chat.id
    ff_id    = message.text.strip()
    txt      = get_txt(chat_id)
    item     = selected_item.get(chat_id, "—")

    waiting_for_id[chat_id] = False
    bot.send_message(
        ADMIN_ID,
        txt["admin_id_received"].format(
            item=item,
            user_id=ff_id,
            name=message.from_user.first_name or "—"
        )
    )
    bot.send_message(chat_id, txt["id_ok"].format(item=item, user_id=ff_id))


# ========== ADMIN COMMANDS ==========
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def admin_commands(message):
    text = message.text.strip().lower() if message.text else ""
    lang = get_lang(ADMIN_ID)
    txt  = TEXTS.get(lang, TEXTS["uz"])

    if text in ["id", "/id"]:
        user_chat_id = last_order_chat_id.get(ADMIN_ID)
        if user_chat_id:
            user_txt = get_txt(user_chat_id)
            waiting_for_id[user_chat_id] = True
            bot.send_message(user_chat_id, user_txt["ask_id"])
            bot.send_message(ADMIN_ID, txt["id_sent_admin"])
        else:
            bot.send_message(ADMIN_ID, txt["no_order"])

    elif text in ["help", "/help", "yordam", "ёри"]:
        bot.send_message(ADMIN_ID, txt["admin_help"])


# ========== MAIN ==========
def start_bot():
    while True:
        try:
            print("✅ Bot ishga tushdi!")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            time.sleep(10)
            print("🔄 Bot qayta ishga tushmoqda...")

if __name__ == "__main__":
    start_bot()
