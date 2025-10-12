FROM python:3.14 AS core
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM node:22 AS node
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm ci
COPY . /app
RUN npm run tailwind

FROM core
COPY . /app
COPY --from=node /app/static/core/css/output.css /app/static/core/css/output.css
RUN mkdir -p /app/db/ && \
    chmod +x /app/start.sh && \
    rm requirements.txt && \
    rm /app/static/core/css/main.css && \
    rm package.json && \
    rm package-lock.json && \
    chown -R 1000:1000 /app

USER 1000
EXPOSE 8000
ENTRYPOINT ["./start.sh"]
