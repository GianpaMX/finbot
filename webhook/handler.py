from jsonhandler import JsonHandler
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookHandler(JsonHandler, WebHookView):
    def initialize(self, config):
        self.usecase = WebHookUseCase(config)
        self.presenter = WebHookPresenter(self, self.usecase)

    def get(self):
        if self.get_argument("hub.mode") == 'subscribe':
            self.presenter.subscribe(self.get_argument("hub.verify_token"), self.get_argument("hub.challenge"))

    def on_verified(self, response):
        self.write_json(response)

    def on_error(self):
        self.send_error(403)
