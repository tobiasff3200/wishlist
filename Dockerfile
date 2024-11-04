FROM registry.gitlab.fachschaften.org/tobiasff3200/django-core:v3.0.2 AS core
WORKDIR /app
COPY . /app/wishlist
RUN sed -i 's/{{app_to_install}}/wishlist/g' core/settings.py && sed -i 's/{{app_to_install}}/wishlist/g' core/urls.py


FROM node:22 AS node
WORKDIR /app/wishlist
COPY --from=core /app /app
RUN npm ci && npm run tailwind


FROM core
COPY --from=node /app/static/core/css/output.css /app/static/core/css/output.css
USER root
RUN chown -R 1000:1000 /app && rm /app/wishlist/static/wishlist/css/main.css
USER 1000
