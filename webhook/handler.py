from tornado.ioloop import IOLoop

from data.book_repository import BookRepository
from data.comodity_repository import ComodityRepository
from data.http_client import HttpClient
from import_url.usecase import ImportUrlUseCase
from jsonhandler import JsonHandler
from receive_message.usecase import ReceiveMessageUseCase
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookHandler(JsonHandler, WebHookView):
    def initialize(self, config):
        self.http_client = HttpClient()
        self.book_repository = BookRepository()
        self.comdity_repository = ComodityRepository()
        self.import_url_usecase = ImportUrlUseCase(self.http_client, self.book_repository, self.comdity_repository)
        self.receive_message_usecase = ReceiveMessageUseCase(self.import_url_usecase)
        self.webhook_usecase = WebHookUseCase(config)
        self.presenter = WebHookPresenter(self, self.webhook_usecase, self.receive_message_usecase)

    def get(self):
        if self.get_argument("hub.mode") == 'subscribe':
            self.presenter.subscribe(self.get_argument("hub.verify_token"), self.get_argument("hub.challenge"))

    def post(self):
        IOLoop.instance().spawn_callback(lambda: self.presenter.entries_received(self.json_data['entry']))
        self.write_json({"success": True})

    def on_success(self, response):
        self.write_json(response)

    def on_error(self):
        self.send_error(403)
