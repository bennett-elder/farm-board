FROM python:3.11.8 AS base

ARG DEBUG_MODE=True
ARG DB_URL
ARG DB_NAME
ARG API_KEYS
ARG APP_MODE="poster"

ENV DEBUG_MODE=$DEBUG_MODE
ENV DB_URL=$DB_URL
ENV DB_NAME=$DB_NAME
ENV API_KEYS=$API_KEYS
ENV APP_MODE=$APP_MODE
ENV FRONTEND_BUILD_PATH="frontend"

RUN mkdir -p /app
WORKDIR /app
RUN cd /app
# COPY backend/requirements.txt /app/requirements.txt
COPY /backend /app
RUN pip install -r requirements.txt

FROM node:16.17.0 as builder
COPY /frontend .
RUN npm install & npm run build

FROM base AS final
WORKDIR /app
COPY --from=builder ./build /app/frontend

EXPOSE 8000
WORKDIR /app
CMD ["python", "main.py"]
