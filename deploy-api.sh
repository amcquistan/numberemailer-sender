#!/bin/bash

if [ ! -f .env ]; then
  echo "!!! missing .env environment variables file"
  echo "see .env.example for list of environment variables required"
  exit 1
fi

source .env

if [[ -z $DB_URL ]]; then
  echo "!!! Missing environment variable DB_URL"
  exit 1
fi

if [[ -z $AWS_PROFILE ]]; then
  echo "!!! Missing environment variable AWS_PROFILE"
  exit 1
fi

if [[ -z $AWS_REGION ]]; then
  echo "!!! Missing environment variable AWS_REGION"
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

sam build

set -x 

sam deploy --profile $AWS_PROFILE \
  --region $AWS_REGION \
  --parameter-overrides DBUrl=$DB_URL SendGridKey=$SENDGRID_KEY FromEmail=$FROM_EMAIL CorsOrigins=$CORS_ORIGINS \
  --guided
