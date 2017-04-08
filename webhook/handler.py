from pprint import pprint

from tornado.ioloop import IOLoop

from import_url.usecase import ImportUrlUseCase
from jsonhandler import JsonHandler
from receive_message.usecase import ReceiveMessageUseCase
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookHandler(JsonHandler, WebHookView):
    def initialize(self, config):
        self.import_url_usecase = ImportUrlUseCase()
        self.receive_message_usecase = ReceiveMessageUseCase(self.import_url_usecase)
        self.webhook_usecase = WebHookUseCase(config)
        self.presenter = WebHookPresenter(self, self.webhook_usecase, self.receive_message_usecase)

    def get(self):
        if self.get_argument("hub.mode") == 'subscribe':
            self.presenter.subscribe(self.get_argument("hub.verify_token"), self.get_argument("hub.challenge"))

    def post(self):
        IOLoop.instance().spawn_callback(lambda: self.presenter.entries_received(self.json_data['entry']))
        pprint(self.json_data)
        self.write_json({"success": True})

        # if self.json_data['object'] == 'page':
        #     self.presenter.entriesReceived(self.json_data['entry'])

    def on_success(self, response):
        self.write_json(response)

    def on_error(self):
        self.send_error(403)
