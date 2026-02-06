FROM joyzoursky/python-selenium:latest

WORKDIR /app

# फाइलें कॉपी करना
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# बॉट शुरू करना
CMD ["python", "main.py"]
