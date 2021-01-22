#!/bin/bash

if [ ! -f .env ]; then
  echo "!!! missing .env environment variables file"
  echo "see .env.example for list of environment variables required"
  exit 1
fi

source .env

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

if [[ -z $SUBMISSION_ENDPOINT ]]; then
  echo "!!! Missing environment variable SUBMISSION_ENDPOINT"
  exit 1
fi

if [[ -z $SUBMISSION_APIKEY ]]; then
  echo "!!! Missing environment variable SUBMISSION_APIKEY"
  exit 1
fi

if [[ -z $DEPLOY_BUCKET ]]; then
  echo "!!! Missing environment variable DEPLOY_BUCKET"
  exit 1
fi

if [[ -z $STACK_NAME ]]; then
  echo "!!! Missing environment variable STACK_NAME"
  exit 1
fi

sam build

set -x 

sam deploy --profile $AWS_PROFILE \
  --region $AWS_REGION \
  --stack-name $STACK_NAME \
  --s3-bucket $DEPLOY_BUCKET \
  --parameter-overrides SendGridKey=$SENDGRID_KEY \
      FromEmail=$FROM_EMAIL \
      CorsOrigins=$CORS_ORIGINS \
      SubmissionEndpoint=$SUBMISSION_ENDPOINT \
      SubmissionApiKey=$SUBMISSION_APIKEY \
  --confirm-changeset \
  --capabilities CAPABILITY_IAM
