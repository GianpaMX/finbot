from data.book_repository import BookRepository
from data.comodity_repository import ComodityRepository
from data.facebook_send_api_gateway import FacebookSendApiGateway
from data.http_client import HttpClient
from import_url.usecase import ImportUrlUseCase
from receive_message.usecase import ReceiveMessageUseCase
from webhook.presenter import WebHookPresenter
from webhook.usecase import WebHookUseCase
from webhook.view import WebHookView


class WebHookModule:
    def __init__(self, config, webHookView: WebHookView):
        self.config = config
        self.webHookView = webHookView

    def provideHttpClient(self):
        return HttpClient()

    def provideBookRepository(self):
        return BookRepository()

    def provideComodityRepository(self):
        return ComodityRepository()

    def provideImportUrlUseCase(self):
        return ImportUrlUseCase(self.provideHttpClient(), self.provideBookRepository(),
                                self.provideComodityRepository())

    def provideSendApiGateway(self):
        return FacebookSendApiGateway(self.provideHttpClient(), self.config)

    def provideReceiveMessageUseCase(self):
        return ReceiveMessageUseCase(self.provideImportUrlUseCase(), self.provideSendApiGateway())

    def provideWebHookUseCase(self):
        return WebHookUseCase(self.config)

    def provideWebHookPresenter(self):
        return WebHookPresenter(self.webHookView, self.provideWebHookUseCase(), self.provideReceiveMessageUseCase())
