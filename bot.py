import requests
import time
import random
from collections import Counter
from bs4 import BeautifulSoup
import os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

URL="https://onbit.vn/ket-qua-xo-so/vietlott-keno"

def get_results():

    r=requests.get(URL)
    soup=BeautifulSoup(r.text,"html.parser")

    results=[]
    ky_quay=""

    rows=soup.select("table tr")

    for row in rows:

        text=row.text.split()

        nums=[int(x) for x in text if x.isdigit()]

        if len(nums)>=20:
            results.append(nums[:20])

        for t in text:
            if t.isdigit() and len(t)>=5:
                ky_quay=t

    return results[:100],ky_quay


def analyze(data):

    flat=[]

    for draw in data:
        flat.extend(draw)

    count=Counter(flat)

    hot=[x[0] for x in count.most_common(10)]

    cold=[x[0] for x in count.most_common()[-10:]]

    pool=hot[:7]+cold[:3]

    predict=sorted(random.sample(pool,8))

    return hot,cold,predict


def send():

    data,ky=get_results()

    hot,cold,predict=analyze(data)

    msg="🎯 KENO AI\n\n"
    msg+=f"🎰 KY QUAY: {ky}\n\n"

    msg+="🔥 HOT\n"
    msg+=" ".join(map(str,hot))

    msg+="\n\n❄️ COLD\n"
    msg+=" ".join(map(str,cold))

    msg+="\n\n🎲 PREDICT\n"
    msg+=" ".join(map(str,predict))

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id":CHAT_ID,
        "text":msg
    })


while True:

    try:
        send()
    except Exception as e:
        print(e)

    time.sleep(480)
