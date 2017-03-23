from webhook.callback import WebHookUseCaseCallback


class WebHookUseCase(object):
    def __init__(self, config):
        self.config = config

    def verify(self, token, challenge, callback: WebHookUseCaseCallback):
        if self.config['token'] == token:
            callback.on_verification_success(challenge)
        else:
            callback.on_failure()

    def entryReceived(self, entry, callback):
        page_id = entry['id']
        time_of_event = entry['time']

        for event in entry['messaging']:
            if 'message' in event:
                callback.on_message_received(page_id, time_of_event, event)
            else:
                callback.on_unknown_event(page_id, time_of_event, event)
