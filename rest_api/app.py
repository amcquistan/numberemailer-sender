import os
import boto3
from flask import request, jsonify, json, render_template_string, current_app
from flask_lambda import FlaskLambda
from flask_cors import CORS
import sendgrid
from sendgrid.helpers.mail import Mail, CustomArg
import uuid
import psycopg2

app = FlaskLambda(__name__)

CORS(
    app,
    resources={
        "*": {"origins": os.getenv("ALLOWED_ORIGINS", "localhost:8000").split(",")}
    },
)

sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_KEY"])


def db_connection():
    from urllib.parse import urlparse
    result = urlparse(os.environ["DB_URL"])

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    return psycopg2.connect(
        dbname=database, user=username, password=password, host=hostname
    )


@app.route("/send-number-email/", methods=("POST",))
def send_number_email():
    data = request.get_json()
    num = data["number"]
    to_email = data["to_email"]

    # fetch email template from S3
    # - maybe figure this out later as its unneeded for this demo

    # render email template with number
    email_body = render_template_string(
        "Hello {{ email }} your generated number was {{ num }}", email=to_email, num=num
    )

    mail = Mail(
        from_email=os.environ["FROM_EMAIL"],
        to_emails=[to_email],
        subject="Flask SendGrid Demo: Random Number Generated",
        plain_text_content=email_body,
    )

    mail.add_custom_arg(CustomArg(key="custom_id", value=str(uuid.uuid4())))

    if os.environ["EXEC_ENV"] == "local":
        #return the email
        return jsonify({"email": str(mail)})
    else:
        # send email to SendGrid API passing it the template
        sg.client.mail.send.post(request_body=mail.get())

        # return status response
        return jsonify({"message": "Successful email push to SendGrid"})
