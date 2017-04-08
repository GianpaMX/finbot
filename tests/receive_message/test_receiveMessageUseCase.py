from unittest import TestCase
from unittest.mock import Mock

from import_url.usecase import ImportUrlUseCase
from receive_message.usecase import ReceiveMessageUseCase


class TestReceiveMessageUseCase(TestCase):
    def setUp(self):
        self.import_url_usecase = Mock(ImportUrlUseCase)
        self.usecase = ReceiveMessageUseCase(self.import_url_usecase)

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

        self.import_url_usecase.import_url.assert_called_with(EXPECTED_URL)
