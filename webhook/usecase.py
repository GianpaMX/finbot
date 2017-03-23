from webhook.callback import WebHookUseCaseCallback


class WebHookUseCase(object):
    def __init__(self, config):
        self.config = config

    def verify(self, token, challenge, callback: WebHookUseCaseCallback):
        if self.config['token'] == token:
            callback.on_success(challenge)
        else:
            callback.on_failure()
