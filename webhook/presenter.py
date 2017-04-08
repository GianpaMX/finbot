from receive_message.usecase import ReceiveMessageUseCase
from webhook.callback import WebHookUseCaseCallback
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookPresenter(WebHookUseCaseCallback):
    def __init__(self, view: WebHookView, webhook_usecase: WebHookUseCase,
                 receive_message_usecase: ReceiveMessageUseCase):
        self.view = view
        self.webhook_usecase = webhook_usecase
        self.receive_message_usecase = receive_message_usecase

    def subscribe(self, token, challenge):
        self.webhook_usecase.verify(token, challenge, self)

    def on_verification_success(self, challenge):
        self.view.on_success({'challenge': challenge})

    def on_failure(self):
        self.view.on_error()

    def entries_received(self, entries):
        for entry in entries:
            self.webhook_usecase.entry_received(entry, self)

    def on_message_received(self, page_id, time_of_event, event):
        self.receive_message_usecase.received(page_id, time_of_event, event)

    def on_unknown_event(self, page_id, time_of_event, event):
        pass
