cat << 'EOF' > /sdcard/Download/bot.py
import os
import logging
import edge_tts
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = "8991252149:AAG-VqqMv6Kyxaoj6BIOBKWjC2psmRAf1oU"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Giuseppe Multilingual TTS Bot (Speechma Style) အဆင်သင့်ဖြစ်ပါပြီ။ စာသားပို့ပေးပါဗျာ။")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    chat_id = update.message.chat_id
    
    status_message = await update.message.reply_text("🔊 Speechma စတိုင် အဖြတ်အတောက်မှန်အောင် ဖန်တီးနေပါတယ်...")
    
    # Permission Denied မဖြစ်စေရန် အသံဖိုင်ကို Termux ရဲ့ internal home ထဲမှာ ယာယီသိမ်းခိုင်းထားပါတယ်
    filename = os.path.expanduser(f"~/giuseppe_multi_{chat_id}.mp3")
    
    try:
        voice_model = "it-IT-GiuseppeMultilingualNeural"
        
        # Speechma ဝဘ်ဆိုက်ကဲ့သို့ ဖြည်းဖြည်းမှန်မှန်နှင့် သဘာဝကျကျ ဖြတ်တောက်ရန် rate="-12%"
        communicate = edge_tts.Communicate(raw_text, voice_model, rate="-12%")
        await communicate.save(filename)
        
        with open(filename, 'rb') as audio:
            keyboard = [[InlineKeyboardButton("📥 Download Audio", callback_data="download_hint")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_audio(
                audio=audio, 
                title=f"TTS_Speechma_{chat_id}", 
                performer="Giuseppe Multilingual",
                reply_markup=reply_markup
            )
            
        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"❌ Error occurred: {str(e)}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="ညာဘက်က အစက် ၃ စက်ကိုနှိပ်ပြီး 'Save to music' လုပ်ပြီး ဖုန်းထဲ ဒေါင်းလုဒ်ဆွဲနိုင်ပါတယ်ဗျာ။", show_alert=True)

def main():
    application = Application.builder().token(BOT_TOKEN).connect_timeout(60).read_timeout(60).write_timeout(60).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot စတင်ပတ်မောင်းနေပါပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()
EOF
