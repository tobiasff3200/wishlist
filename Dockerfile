FROM python:3.10

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN mkdir -p /app/db/
EXPOSE 8000
RUN chmod +x /app/start.sh
ENTRYPOINT ["./start.sh"]
