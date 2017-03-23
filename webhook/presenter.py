from webhook.callback import WebHookUseCaseCallback
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookPresenter(WebHookUseCaseCallback):
    def __init__(self, view: WebHookView, usecase: WebHookUseCase):
        self.view = view
        self.usecase = usecase

    def subscribe(self, token, challenge):
        self.usecase.verify(token, challenge, self)

    def on_verification_success(self, challenge):
        self.view.on_success({'challenge': challenge})

    def on_failure(self):
        self.view.on_error()

    def entriesReceived(self, entries):
        for entry in entries:
            self.usecase.entryReceived(entry)

    def on_message_received(self, page_id, time_of_event, event):
        pass

    def on_unknown_event(self, page_id, time_of_event, event):
        pass


