FROM registry.gitlab.fachschaften.org/tobiasff3200/django-core:v2.0.2 as core
WORKDIR /app
COPY . /app/wishlist
RUN pip install -r wishlist/requirements.txt
RUN rm wishlist/requirements.txt

RUN sed -i 's/{{app_to_install}}/wishlist/g' core/settings.py
RUN sed -i 's/{{app_to_install}}/wishlist/g' core/urls.py


FROM node:18 AS node
WORKDIR /app/wishlist
COPY --from=core /app /app
RUN npm ci
RUN npm run tailwind


FROM core
COPY --from=node /app/static/core/css/output.css /app/static/core/css/output.css
RUN rm /app/wishlist/static/wishlist/css/main.css