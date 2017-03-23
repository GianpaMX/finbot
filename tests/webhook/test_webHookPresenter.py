from pprint import pprint
from unittest import TestCase
from unittest.mock import Mock

from webhook.callback import WebHookUseCaseCallback
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class TestWebHookPresenter(TestCase):
    EXPECTED_CHALLENGE = '123'

    def setUp(self):
        self.view = Mock(WebHookView)
        self.usecase = Mock(WebHookUseCase)
        self.presenter = WebHookPresenter(self.view, self.usecase)

    def test_subscribe(self):
        EXPECTED_TOKEN = '456'

        self.presenter.subscribe(self.EXPECTED_CHALLENGE, EXPECTED_TOKEN)

        self.assertEqual(self.usecase.verify.call_args[0][0], self.EXPECTED_CHALLENGE)
        self.assertEqual(self.usecase.verify.call_args[0][1], EXPECTED_TOKEN)
        self.assertIsInstance(self.usecase.verify.call_args[0][2], WebHookUseCaseCallback)

    def test_on_success(self):
        self.presenter.on_success(self.EXPECTED_CHALLENGE)

        self.view.on_verified.assert_called_with({'challenge': self.EXPECTED_CHALLENGE})

    def test_on_failure(self):
        self.presenter.on_failure()

        self.view.on_error.assert_called()
