from bs4 import BeautifulSoup as BS
from twilio.rest import Client
import requests

url = "https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/tatamotors/TM03"
twilio_sid = "YOUR TWILIO_SID"
twilio_auth_token = "YOUR TWILIO_AUTH_TOKEN"
threshold = "500"                                                                              # CHOOSE YOUR THRESHHOLD VALUE

while True:
    r = requests.get(url)
    soup = BS(r.text, features="html.parser")

    cp = soup.find("div", attrs={"class": "inprice1 nsecp"})
    print("current price : "+ cp.text)

    yp = soup.find(attrs ={"class": "nseprvclose bseprvclose"})
    print("yesterday price : " + yp.text)

    volume = soup.find(attrs={"class": "nsevol bsevol"})
    print("volume : "+ volume.text)

    movement = float(cp.text) - float(yp.text)
    print(round(movement,2))

    up_down = None

    if movement > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    mov_percent = round(((movement / float(cp.text)) * 100), 2)
    print(mov_percent)

    if cp.text <= threshold :
        message_string = "Stock : Tata Motors Ltd.\nCurrent Price : ₹ " + cp.text +"\nMovement : " + up_down + str(round(movement,2)) + "(" + str(mov_percent) + "%" + ")" + "\nVolume : " + volume.text + "\nHurry Up!!!"

        client = Client(twilio_sid, twilio_auth_token)

        message = client.messages.create(
            body=message_string,
            from_="+14342312749",
            to="ENTER YOUR MOBILE NUMBER"
        )
        
        print("Message Sent")
        break
