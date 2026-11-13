FROM python:3.14-slim

WORKDIR /app

COPY *.py .
COPY data/ ./data/

CMD ["python", "inf1103-labs-smart-auditor.py"]