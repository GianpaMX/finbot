import json

from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application, url

from webhook.handler import WebHookHandler

define("config", default="config.json", help="Main config file")


def make_app(json_config):
    with open(json_config) as data_file:
        config = json.load(data_file)

    return Application([
        url(r"/webhook", WebHookHandler, dict(config=config), "webhook")
    ])


if __name__ == "__main__":
    parse_command_line()

    app = make_app(options.config)
    app.listen(8080)
    IOLoop.current().start()
