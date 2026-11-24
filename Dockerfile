FROM python:3.14-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY ./data/ ./data/

CMD ["python", "inf1103-labs-smart-auditor.py"]