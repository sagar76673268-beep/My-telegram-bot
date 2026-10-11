import telebot
from telebot import types

# 1. आपका Telegram Bot टोकन
BOT_TOKEN = "8955508436:AAEeTajqNhqfv0PYwkjv7Yzuo4-qpugxBzw"

# 2. आपका Telegram Chat ID (ऑर्डर का मैसेज पाने के लिए @userinfobot से आईडी लेकर यहाँ डालें)
ADMIN_CHAT_ID = 8749753272

# 3. आपकी PhonePe UPI ID
MY_UPI_ID = "7781882533@ybl"

bot = telebot.TeleBot(BOT_TOKEN)

# यूज़र डेटा स्टोर करने के लिए
user_orders = {}

# /start कमांड
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_followers = types.InlineKeyboardButton("❤️ Instagram Followers", callback_data="service_followers")
    btn_likes = types.InlineKeyboardButton("👍 Instagram Likes", callback_data="service_likes")
    btn_views = types.InlineKeyboardButton("👁️ Reels Views", callback_data="service_views")
    btn_help = types.InlineKeyboardButton("💬 Help / सहायता", callback_data="service_help")
    markup.add(btn_followers, btn_likes, btn_views, btn_help)

    bot.send_message(
        message.chat.id,
        f"नमस्ते {message.from_user.first_name}! 👋\nहमारे सोशल मीडिया स्टोर में आपका स्वागत है।\n\nनीचे से सर्विस चुनें और तुरंत ऑर्डर पाएँ:",
        reply_markup=markup
    )

# सर्विस सेलेक्ट करने पर
@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def handle_service(call):
    chat_id = call.message.chat.id

    if call.data == "service_followers":
        user_orders[chat_id] = {"service": "1000 Instagram Followers", "price": "50"}
    elif call.data == "service_likes":
        user_orders[chat_id] = {"service": "1000 Instagram Likes", "price": "20"}
    elif call.data == "service_views":
        user_orders[chat_id] = {"service": "10,000 Reels Views", "price": "30"}
    elif call.data == "service_help":
        bot.send_message(chat_id, "सहायता के लिए यहाँ संपर्क करें: @h4xeidtar")
        return

    order = user_orders[chat_id]
    msg = f"आपने चुना: *{order['service']}*\nकीमत: *₹{order['price']}*\n\nकृपया अपना Instagram प्रोफ़ाइल या पोस्ट का लिंक यहाँ भेजें:"
    bot.send_message(chat_id, msg, parse_mode="Markdown")

# लिंक और पेमेंट स्क्रीनशॉट हैंडल करना
@bot.message_handler(content_types=['text', 'photo'])
def handle_user_input(message):
    chat_id = message.chat.id

    # अगर यूज़र ने लिंक भेजा है
    if message.content_type == 'text' and ("instagram.com" in message.text or "http" in message.text):
        if chat_id in user_orders:
            user_orders[chat_id]["link"] = message.text
            order = user_orders[chat_id]

            upi_pay_text = (
                f"✅ लिंक मिल गया!\n\n"
                f"कृपया *₹{order['price']}* इस UPI ID पर ट्रांसफर करें:\n"
                f"`{MY_UPI_ID}`\n\n"
                f"पेमेंट करने के बाद स्क्रीनशॉट यहाँ भेजें।"
            )
            bot.send_message(chat_id, upi_pay_text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "पहले /start दबाकर सर्विस चुनें।")

    # अगर यूज़र ने पेमेंट का स्क्रीनशॉट भेजा है
    elif message.content_type == 'photo':
        if chat_id in user_orders and "link" in user_orders[chat_id]:
            order = user_orders[chat_id]
            file_id = message.photo[-1].file_id

            # एडमिन को मैसेज भेजना
            admin_text = (
                f"🚨 *नया ऑर्डर आया है!*\n\n"
                f"👤 यूज़र: @{message.from_user.username} (ID: `{chat_id}`)\n"
                f"📌 सर्विस: {order['service']}\n"
                f"💰 अमाउंट: ₹{order['price']}\n"
                f"🔗 लिंक: {order['link']}\n"
                f"पेमेंट स्क्रीनशॉट नीचे है 👇"
            )
            if ADMIN_CHAT_ID != "YOUR_NUMERIC_ID":
                bot.send_photo(ADMIN_CHAT_ID, file_id, caption=admin_text, parse_mode="Markdown")

            # ग्राहक को कन्फर्मेशन
            bot.send_message(chat_id, "✅ आपका पेमेंट और ऑर्डर प्राप्त हो गया है!\n\nकुछ ही मिनटों में आपकी सर्विस शुरू हो जाएगी।")
            del user_orders[chat_id]
        else:
            bot.send_message(chat_id, "कृपया पहले सर्विस चुनें और लिंक भेजें।")

# बोट को चालू रखना
bot.infinity_polling()

          
