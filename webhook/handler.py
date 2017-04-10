from tornado.ioloop import IOLoop

from jsonhandler import JsonHandler
from webhook.di import WebHookModule
from webhook.view import WebHookView


class WebHookHandler(JsonHandler, WebHookView):
    def initialize(self, config):
        web_hook_module = WebHookModule(config, self)
        self.presenter = web_hook_module.provideWebHookPresenter()

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
