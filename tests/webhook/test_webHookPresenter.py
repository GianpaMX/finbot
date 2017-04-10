from unittest import TestCase
from unittest.mock import Mock

from receive_message.usecase import ReceiveMessageUseCase
from webhook.callback import WebHookUseCaseCallback
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class TestWebHookPresenter(TestCase):
    EXPECTED_CHALLENGE = '123'

    def setUp(self):
        self.view = Mock(WebHookView)
        self.usecase = Mock(WebHookUseCase)
        self.receive_message_usecase = Mock(ReceiveMessageUseCase)
        self.presenter = WebHookPresenter(self.view, self.usecase, self.receive_message_usecase)

    def test_subscribe(self):
        EXPECTED_TOKEN = '456'

        self.presenter.subscribe(self.EXPECTED_CHALLENGE, EXPECTED_TOKEN)

        self.assertEqual(self.usecase.verify.call_args[0][0], self.EXPECTED_CHALLENGE)
        self.assertEqual(self.usecase.verify.call_args[0][1], EXPECTED_TOKEN)
        self.assertIsInstance(self.usecase.verify.call_args[0][2], WebHookUseCaseCallback)

    def test_on_success(self):
        self.presenter.on_verification_success(self.EXPECTED_CHALLENGE)

        self.view.on_success.assert_called_with({'challenge': self.EXPECTED_CHALLENGE})

    def test_on_failure(self):
        self.presenter.on_failure()

        self.view.on_error.assert_called()

    def test_entries_received(self):
        entries = [{}, {}, {}]

        self.presenter.entries_received(entries)

        assert self.usecase.entry_received.call_count == len(entries)

    def test_on_message_received(self):
        EXPECTED_PAGE_ID = 'PAGE_ID'
        EXPECTED_TIME = 1491670288081
        EXPECTED_EVENT = {}

        self.presenter.on_message_received(EXPECTED_PAGE_ID, EXPECTED_TIME, EXPECTED_EVENT)

        self.receive_message_usecase.received.assert_called_with(EXPECTED_PAGE_ID, EXPECTED_TIME, EXPECTED_EVENT)
