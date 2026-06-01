from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8636112430:AAGyVD4y2Blfe4RX44KTVFdOaVrSIaaIK04"
CHANNEL_ID = "-1002004614772"

NAME, PRICE, DESC, PHOTO = range(4)

async def start(update, context):
    await update.message.reply_text("سلام! 👋\nنام محصول را بنویسید:")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("💰 قیمت را بنویسید:")
    return PRICE

async def get_price(update, context):
    context.user_data["price"] = update.message.text
    await update.message.reply_text("📝 توضیحات را بنویسید:")
    return DESC

async def get_desc(update, context):
    context.user_data["desc"] = update.message.text
    await update.message.reply_text("📸 عکس محصول را ارسال کنید:")
    return PHOTO

async def get_photo(update, context):
    photo = update.message.photo[-1].file_id
    name = context.user_data["name"]
    price = context.user_data["price"]
    desc = context.user_data["desc"]
    caption = f"🕐 *{name}*\n\n💰 قیمت: {price}\n\n📝 {desc}\n\n📞 برای سفارش پیام دهید\n🆔 @SAATMOGHADAMO"
    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption, parse_mode="Markdown")
    await update.message.reply_text("✅ محصول در کانال ارسال شد!")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("❌ لغو شد.")
    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desc)],
        PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
app.add_handler(conv)
print("ربات در حال اجراست...")
app.run_polling()
