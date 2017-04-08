class WebHookUseCaseCallback(object):
    def on_verification_success(self, challenge):
        raise NotImplementedError("Please Implement this method")

    def on_message_received(self, page_id, time_of_event, event):
        raise NotImplementedError("Please Implement this method")

    def on_unknown_event(self, page_id, time_of_event, event):
        raise NotImplementedError("Please Implement this method")

    def on_failure(self):
        raise NotImplementedError("Please Implement this method")
