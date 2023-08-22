import requests
from time import sleep
from sms import SendSms

token = "" #bot olarak kullanmak istediğiniz hesabın Discord token'i.
chat_id =   #sohbet id'si (int)

def getHeaders(token=None, content_type="application/json"):
    header = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        header.update({"Authorization": token})
    return header

def getChat(token, id):
    try:
        while 1:
            url = f"https://discord.com:443/api/v9/channels/{id}/messages?limit=100"
            r = requests.get(url, headers=getHeaders(token)).json()
            timestamp, content, id = r[0]["timestamp"], r[0]["content"], r[0]["author"]["id"]
            return timestamp, content, id
    except:
        print("Sohbet çekilirken sorun meydana geldi!")

def send(token, id:str, text):    
    url = f"https://discord.com:443/api/v9/channels/{id}/messages"
    headers = getHeaders(token)
    json={"content": text, "nonce": "", "tts": False}
    r = requests.post(url, headers=headers, json=json)
    if r.status_code == 200:
        return("Mesaj Gönderildi!")
    else:
        return("Mesaj gönderilemedi!")        

zaman = []

adet = 55#SMS sayısı

saniye = 0#aralık(saniye)

while 1:
    timestamp, content, id = getChat(token, chat_id)
    if len(content.split(" ")) == 2 and content.split(" ")[0] == ".sms":
        if len(content.split(" ")[1]) == 10:
            telno = content.split(" ")[1]
            send(token, chat_id, f"{telno} numaralı telefona sms gönderimi başlamıştır.\n<@{id}>")  
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
            send(token, chat_id, telno+" --> "+str(sms.adet)+f" adet SMS gönderildi.\n<@{id}>")                        
        else:
            send(token, chat_id, f"Geçerli komut yazınız!\nYardım için ' .help ' yazınız.\n<@{id}>")
            zaman.append(timestamp)
    elif ".help" == content and timestamp not in zaman:
        zaman.append(timestamp)
        send(token, chat_id, f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n.sms 5051234567\n.sms (telefon numarası)\n<@{id}>")
    elif ".status" == content and timestamp not in zaman:
        zaman.append(timestamp)
        mesaj = "" #mesajınızı yazınız
        send(token, chat_id, mesaj+f"\n<@{id}>")
    else:
        pass
