import requests
from time import sleep
from sms import SendSms

token = ""
sahip = ""


def getUpdate():
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
    r = requests.get(url)
    x = 0
    while 1 :
        try:
            r.json()["result"][x]
            x+=1
        except IndexError:
            return (r.json()["result"][x-1]["message"]["chat"]["id"]), r.json()["result"][x-1]["message"]["text"], (r.json()["result"][x-1]["message"]["date"])

def sendMessage(text, id):
    requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text=" + text, timeout=3)
    
date_list = []
while 1:
    try:
        id, text, date = getUpdate()
        if text == "/sms" and date not in date_list:
            date_list.append(date)
            sendMessage("SMS göndermek istediğiniz numarayı %2B90 olmadan yazınız.", id)
            while True:
                id, text, date = getUpdate()
                if len(text) != 10 and date not in date_list:
                    date_list.append(date)
                    sendMessage("Lütfen 10 haneli telefon numarası giriniz.", id)
                elif text == sahip and date not in date_list:
                    date_list.append(date)
                    sendMessage("Bu önemli şahsiyeti rahatsız etmek istemiyorum.\nFarklı telefon numarası yazınız!", id)
                elif len(text) == 10 and date not in date_list:
                    date_list.append(date)
                    telno = text
                    sendMessage("Kaç adet SMS göndermek istiyorsunuz?", id)
                    while 1:
                        id, text, date = getUpdate()
                        if date not in date_list:
                            try:
                                intcheck_adet = int(text)
                                date_list.append(date)
                                sendMessage("Kaç saniye aralıklarla göndermek istiyorsunuz?", id)
                                while 1:
                                    id, text, date = getUpdate()
                                    if date not in date_list:
                                        try:
                                            intcheck_saniye = int(text)
                                            date_list.append(date)
                                            sendMessage(f"{intcheck_adet} adet SMS {intcheck_saniye} saniye aralıklarla gönderiliyor...", id)
                                            sms = SendSms(telno, "")
                                            while sms.adet < intcheck_adet:
                                                for attribute in dir(SendSms):
                                                    attribute_value = getattr(SendSms, attribute)
                                                    if callable(attribute_value):
                                                        if attribute.startswith('__') == False:
                                                            if sms.adet == intcheck_adet:
                                                                break
                                                            exec("sms."+attribute+"()")
                                                            sleep(intcheck_saniye)
                                            sendMessage(telno+" --> "+str(sms.adet)+" adet SMS gönderildi.", id)
                                            break
                                        except ValueError:
                                            date_list.append(date)
                                            sendMessage("Lütfen sayısal değer giriniz.", id)
                                    sleep(1)
                            except ValueError:
                                date_list.append(date)
                                sendMessage("Lütfen sayısal değer giriniz.", id)
                            break
                        sleep(1)
                    break
                sleep(1)      
        elif text == "/start" and date not in date_list:
            date_list.append(date)
            sendMessage("Merhaba!\nBirilerini rahatsız etmek istiyorsan doğru yere geldin.\n'/sms' komutu ile sms göndermeye başlayabilirsin\nİyi eğlenceler!\n\nKaynak kodu:https://gitlab.com/tingirifistik/enough/\nTwitter: @_tingirifistik\n\n ", id)        
        elif text != "/sms" and text != "/start" and date not in date_list:
            date_list.append(date)
            sendMessage("Yazdığınızı anlayamadım.", id)
        sleep(1)
    except:
        sleep(1)
