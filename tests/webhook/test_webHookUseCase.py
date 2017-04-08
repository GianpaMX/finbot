from unittest import TestCase
from unittest.mock import Mock

from webhook.callback import WebHookUseCaseCallback
from webhook.usecase import WebHookUseCase


class TestWebHookUseCase(TestCase):
    def setUp(self):
        config = {
            'token': '123'
        }
        self.usecase = WebHookUseCase(config)
        self.callback = Mock(WebHookUseCaseCallback)

    def test_verify_on_success(self):
        EXPECTED_CHALLENGE = 'expected_challenge'

        self.usecase.verify('123', EXPECTED_CHALLENGE, self.callback)

        self.callback.on_verification_success.assert_called_with(EXPECTED_CHALLENGE)

    def test_verify_on_failure(self):
        self.usecase.verify('456', 'expected_challenge', self.callback)

        self.callback.on_failure.assert_called()
