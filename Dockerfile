FROM registry.gitlab.fachschaften.org/tobiasff3200/django-core:v3.0.0 as core
WORKDIR /app
COPY . /app/wishlist
RUN pip install --no-cache-dir -r wishlist/requirements.txt && rm wishlist/requirements.txt && sed -i 's/{{app_to_install}}/wishlist/g' core/settings.py && sed -i 's/{{app_to_install}}/wishlist/g' core/urls.py


FROM node:21 AS node
WORKDIR /app/wishlist
COPY --from=core /app /app
RUN npm ci && npm run tailwind


FROM core
COPY --from=node /app/static/core/css/output.css /app/static/core/css/output.css
RUN rm /app/wishlist/static/wishlist/css/main.css
