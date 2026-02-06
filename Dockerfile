FROM browserless/chrome:latest

# यूजर को रूट (Root) बनाना ताकि फाइलें कॉपी हो सकें
USER root

WORKDIR /app

# पायथन और जरूरी टूल्स इंस्टॉल करना
RUN apt-get update && apt-get install -y python3 python3-pip

# फाइलें कॉपी करना
COPY . .

# लाइब्रेरी इंस्टॉल करना
RUN pip3 install --no-cache-dir -r requirements.txt

# बॉट चलाना और साथ में एक डमी सर्वर चालू करना ताकि Koyeb खुश रहे
# यह 9999 पोर्ट पर Koyeb को 'Healthy' सिग्नल देगा
CMD python3 main.py & python3 -m http.server 9999
