#!/bin/bash

if [ ! -f .env.local ]; then
  echo "!!! missing .env.local environment variables file"
  echo "see .env.example for list of environment variables required"
  exit 1
fi

source .env.local

if [[ -z $DB_URL ]]; then
  echo "!!! Missing environment variable DB_URL"
  exit 1
fi

if [[ -z $FROM_EMAIL ]]; then
  echo "!!! Missing environment variable FROM_EMAIL"
  exit 1
fi

if [[ -z $SENDGRID_KEY ]]; then
  echo "!!! Missing environment variable SENDGRID_KEY"
  exit 1
fi

if [[ -z $CORS_ORIGINS ]]; then
  echo "!!! Missing environment variable CORS_ORIGINS"
  exit 1
fi

sam build --use-container

sam local start-api --parameter-overrides \
  DBUrl=$DB_URL \
  SendGridKey=$SENDGRID_KEY \
  FromEmail=$FROM_EMAIL \
  CorsOrigins=$ALLOWED_ORIGINS
