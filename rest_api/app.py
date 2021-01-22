import os

from flask import request, jsonify, json, render_template_string, current_app
from flask_lambda import FlaskLambda
from flask_cors import CORS
import sendgrid
from sendgrid.helpers.mail import Mail, CustomArg

import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FlaskLambda(__name__)

CORS(
    app,
    resources={
        "*": {"origins": os.getenv("ALLOWED_ORIGINS", "localhost:8000").split(",")}
    },
)

sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_KEY"])


@app.route("/send-number-email/", methods=("POST",))
def send_number_email():
    logger.info({
        'resource': 'numberemailer-sender',
        'operation': 'send_number_email'
    })
    data = request.get_json()
    num = data["number"]
    to_emails = data["to_emails"].split('\n')
    submission_id = None
    try:
        url = os.environ['SUBMISSION_URL']
        api_key = os.environ['SUBMISSION_APIKEY']
        resp = requests.post(url, json={'recipient_count': len(to_emails)}, headers={'X-API-Key': api_key})
        if resp.status_code == 201:
            resp_data = resp.json()
            submission_id = resp_data['submission_id']
        logger.info({
            'resource': 'numberemailer-sender',
            'operation': 'send_number_email',
            'details': {
                'action': 'Fetched submission_id',
                'submission_id': submission_id,
                'api-key': api_key
            }
        })
    except Exception as e:
        logger.error({
            'message': 'Error fetching submission_id',
            'error': str(e),
            'details': {
                'recipient_count': len(to_emails)
            }
        })
        return jsonify('failed to fetch submission_id'), 404

    # fetch email template from S3
    # - maybe figure this out later as its unneeded for this demo

    # render email template with number
    email_body = render_template_string(
        "<html><h1>Hello Friend,</h1><p>Your randomly generated number was {{ num }}.</p><p>Enjoy!</p></html>",
        num=num
    )

    mail = Mail(
        from_email=os.environ["FROM_EMAIL"],
        to_emails=to_emails,
        subject="SendGrid Demo / Random Number Generating Emailer",
        html_content=email_body,
    )

    mail.add_custom_arg(CustomArg(key="submission_id", value=int(submission_id)))

    # send email to SendGrid API passing it the template
    sg.client.mail.send.post(request_body=mail.get())

    # return status response
    return jsonify({"message": "Successful email push to SendGrid", "submission_id": submission_id})
