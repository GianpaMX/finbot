from unittest import TestCase
from unittest.mock import Mock

from data.send_api_gateway import SendApiGateway
from entities.book import Book
from import_url.usecase import ImportUrlUseCase
from receive_message.usecase import ReceiveMessageUseCase


class TestReceiveMessageUseCase(TestCase):
    def setUp(self):
        self.import_url_usecase = Mock(ImportUrlUseCase)
        self.send_api_gateway = Mock(SendApiGateway)
        self.usecase = ReceiveMessageUseCase(self.import_url_usecase, self.send_api_gateway)

    def test_url_received(self):
        ANY_ID = "ANY_ID"
        ANY_TIME = 1491670288081
        EXPECTED_URL = 'EXPECTED_URL'
        event = {
            'message': {
                'attachments': [{
                    'url': EXPECTED_URL
                }]
            }
        }

        self.usecase.received(ANY_ID, ANY_TIME, event)

        self.import_url_usecase.import_url.assert_called_with(EXPECTED_URL, self.usecase)

    def test_on_success(self):
        EXPECTED_SENDER = 'ANY_SENDER'
        self.usecase.event = {'sender': {'id': EXPECTED_SENDER}}
        book = Book()

        self.usecase.on_success(book)

        assert self.send_api_gateway.send_text_message.call_args[0][0] == EXPECTED_SENDER

    def test_on_error(self):
        EXPECTED_SENDER = 'ANY_SENDER'
        self.usecase.event = {'sender': {'id': EXPECTED_SENDER}}

        self.usecase.on_error()

        assert self.send_api_gateway.send_text_message.call_args[0][0] == EXPECTED_SENDER
