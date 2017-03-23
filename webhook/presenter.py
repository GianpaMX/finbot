from webhook.callback import WebHookUseCaseCallback
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookPresenter(WebHookUseCaseCallback):
    def __init__(self, view: WebHookView, usecase: WebHookUseCase):
        self.view = view
        self.usecase = usecase

    def subscribe(self, token, challenge):
        self.usecase.verify(token, challenge, self)

    def on_success(self, challenge):
        self.view.on_verified({'challenge': challenge})

    def on_failure(self):
        self.view.on_error()
