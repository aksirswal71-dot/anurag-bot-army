FROM python:3.9-slim

# Chrome इंस्टॉलेशन
RUN apt-get update && apt-get install -y wget gnupg curl unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app
COPY . .

# यहाँ स्पेलिंग ठीक कर दी है (requirements)
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
