import json
import os
import pytest

"""
Using the mock library. It has the benifit of starting and stoping the mock os.environ
#import mock

@pytest.mark.event_json_file_name("./events/event_test_send_number_email.json")
def test_send_number_email_email_contents(mocker, apigw_event_fixt, lambda_context):
    mock_env = mock.patch.dict(
        os.environ, {"FROM_EMAIL": "test@west.com", "SENDGRID_KEY": "local", "EXEC_ENV": "local"}
    )
    mock_env.start()
    from rest_api import app as flask_app
    ret = flask_app.app(apigw_event_fixt, lambda_context)
    mock_env.stop()

    body = json.loads(ret["body"])
    email = json.loads(body["email"].replace("'", '"'))
    assert email["from"] == {"email": "test@west.com"}
    assert email["subject"] == "Flask SendGrid Demo: Random Number Generated"
    assert email["personalizations"] == [{"to": [{"email": "donovan.orn@west.com"}]}]
    assert email["content"] == [
        {
            "type": "text/plain",
            "value": "Hello donovan.orn@west.com your generated number was 12",
        }
    ]
"""

@pytest.mark.event_json_file_name("./events/event_test_send_number_email.json")
def test_send_number_email_email_contents(mocker, apigw_event_fixt, lambda_context):
    monkeypatch.setenv("FROM_EMAIL", "test@west.com")
    monkeypatch.setenv("SENDGRID_KEY", "local")
    monkeypatch.setenv("EXEC_ENV", "local")

    from rest_api import app as flask_app
    ret = flask_app.app(apigw_event_fixt, lambda_context)

    body = json.loads(ret["body"])
    email = json.loads(body["email"].replace("'", '"'))
    assert email["from"] == {"email": "test@west.com"}
    assert email["subject"] == "Flask SendGrid Demo: Random Number Generated"
    assert email["personalizations"] == [{"to": [{"email": "donovan.orn@west.com"}]}]
    assert email["content"] == [
        {
            "type": "text/plain",
            "value": "Hello donovan.orn@west.com your generated number was 12",
        }
    ]
