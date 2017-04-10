from data.comodity_repository import ComodityRepository
from data.send_api_gateway import SendApiGateway
from entities.book import Book
from import_url.usecase import ImportUrlUseCase


class ReceiveMessageUseCase(ComodityRepository):
    def __init__(self, import_use_case: ImportUrlUseCase, send_api_gateway : SendApiGateway):
        self.import_url_usecase = import_use_case
        self.send_api_gateway = send_api_gateway

    def received(self, page_id, time_of_event, event):
        self.event = event
        if 'message' in event and 'attachments' in event['message']:
            for attachment in event['message']['attachments']:
                if 'url' in attachment:
                    self.import_url_usecase.import_url(attachment['url'], self)

    def on_success(self, book: Book):
        message = "I read your file and found %d accounts" % len(book.accounts)
        self.send_api_gateway.send_text_message(self.event['sender']['id'], message)

    def on_error(self):
        message = "Sorry, I coudn't read your file"
        self.send_api_gateway.send_text_message(self.event['sender']['id'], message)
