FROM python:3.10-slim AS builder

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY tuya/ /tuya

EXPOSE 9090/tcp

CMD ["python3", "main.py"]
