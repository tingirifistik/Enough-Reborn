from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from sms import SendSms
from time import sleep

TOKEN = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Merhaba\!\nBirilerini rahatsız etmek istiyorsan doğru yere geldin\.\n*_/help_* yazarak komutları görebilirsin\.\nİyi eğlenceler\!\n\n[_Kaynak Kodu_](https://gitlab.com/tingirifistik/enough/)\n[_Twitter_](https://twitter.com/_tingirifistik)", parse_mode='MarkdownV2')

async def sms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text.split(" ")) == 2 and update.message.text.split(" ")[0] == "/sms":
        if len(update.message.text.split(" ")[1]) == 10:
            with open("config", "r") as f:
                r = f.read()
            try:
                adet, saniye = int(r.split(":")[0]), int(r.split(":")[1])
            except:
                await update.message.reply_text("Config dosyası ayarlanmamış\!\nConfig dosyasını ayarlamak için *_/config_* komutunu kullanın\.", parse_mode="MarkdownV2")
                return 
            telno = update.message.text.split(" ")[1]
            await update.message.reply_document("https://media.tenor.com/SWiGXYOM8eMAAAAC/russia-soviet.gif", f"*{adet} adet SMS Gönderiliyor \-\-\> {telno}*", parse_mode="MarkdownV2")
            sms = SendSms(telno, "")
            while sms.adet < adet:
                for attribute in dir(SendSms):
                    attribute_value = getattr(SendSms, attribute)
                    if callable(attribute_value):
                        if attribute.startswith('__') == False:
                            if sms.adet == adet:
                                break
                            exec("sms."+attribute+"()")
                            sleep(saniye)
            await update.message.reply_text(f"*{telno} \-\-\> {sms.adet} adet SMS gönderildi\.*", parse_mode='MarkdownV2')                        
        else:
            await update.message.reply_text(f"Geçerli komut yazınız\!\nYardım için *_/help_* yazınız\.", parse_mode='MarkdownV2')
    else:
        await update.message.reply_text(f"Sms göndermek için komutu aşağıdaki gibi yazınız\.\n*_/sms_* _telefon numarası_\n ``` /sms 5051234567```", parse_mode='MarkdownV2')
        
async def help_command(update: Update, conext: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"*_/sms_* \-\-\> SMS Gönderir\.\n*_/sms_* _telefon numarası_\n``` /sms 5051234567```\n\n*_/config_* \-\-\> Gönderilecek SMS adeti ve gönderim sıklığını ayarlar\.\n*_/config_* _adet\:saniye_\n``` /config 57:3```", parse_mode='MarkdownV2')
    
async def ne(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Yazdığınızı anlayamadım.")

async def ayarla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text.split(":")) == 2 and update.message.text.strip("/config ").split(":")[0].isdigit() and update.message.text.split(":")[1].isdigit():
        with open("config", "w") as f:
            f.write(update.message.text.strip("/config "))
        await update.message.reply_text("Ayarlar kaydedildi.")
    else:
        await update.message.reply_text(f"Geçerli komut yazınız\!\nYardım için *_/help_* yazınız\.", parse_mode='MarkdownV2')
    
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("sms", sms))
    application.add_handler(CommandHandler("config", ayarla))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, ne))

    application.run_polling()


if __name__ == "__main__":
    main()
