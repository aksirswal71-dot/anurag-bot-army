FROM browserless/chrome:latest

# यूजर को रूट (Root) बनाना ताकि फाइलें कॉपी हो सकें
USER root

WORKDIR /app

# पायथन इंस्टॉल करना (क्योंकि इस इमेज में सिर्फ क्रोम होता है)
RUN apt-get update && apt-get install -y python3 python3-pip

# फाइलें कॉपी करना
COPY . .

# लाइब्रेरी इंस्टॉल करना
RUN pip3 install --no-cache-dir -r requirements.txt

# बॉट शुरू करना
CMD ["python3", "main.py"]
