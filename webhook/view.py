class WebHookView(object):
    def on_verified(self, response):
        raise NotImplementedError("Please Implement this method")

    def on_error(self):
        raise NotImplementedError("Please Implement this method")
