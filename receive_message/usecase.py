from import_url.usecase import ImportUrlUseCase


class ReceiveMessageUseCase(object):
    def __init__(self, import_use_case: ImportUrlUseCase):
        self.import_url_usecase = import_use_case

    def received(self, page_id, time_of_event, event):
        if 'message' in event and 'attachments' in event['message']:
            for attachment in event['message']['attachments']:
                if 'url' in attachment:
                    self.import_url_usecase.import_url(attachment['url'])
