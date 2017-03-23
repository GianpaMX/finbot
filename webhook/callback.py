class WebHookUseCaseCallback(object):
    def on_success(self, challenge):
        raise NotImplementedError("Please Implement this method")

    def on_failure(self):
        raise NotImplementedError("Please Implement this method")
