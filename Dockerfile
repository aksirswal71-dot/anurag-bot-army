FROM python:3.9-slim

# जरूरी टूल्स इंस्टॉल करना
RUN apt-get update && apt-get install -y wget gnupg gnupg2 curl unzip

# गूगल क्रोम इंस्टॉल करने का पक्का तरीका
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
