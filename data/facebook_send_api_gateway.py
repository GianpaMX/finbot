from data.http_client import HttpClient
from data.send_api_gateway import SendApiGateway

SEND_MESSAGE_URL = 'https://graph.facebook.com/v2.6/me/messages'


class FacebookSendApiGateway(SendApiGateway):
    def __init__(self, http_client: HttpClient, config):
        self.http_client = http_client
        self.config = config

    def send_text_message(self, recipient, message):
        data = {
            'recipient': {'id': recipient},
            'message': {'text': message}
        }
        self.http_client.post_json(SEND_MESSAGE_URL + "?access_token=" + self.config['token'], data)
