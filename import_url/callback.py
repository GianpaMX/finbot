from entities.book import Book


class ImportUrlCallback(object):
    def on_success(self, book: Book):
        raise NotImplementedError("Please Implement this method")

    def on_error(self):
        raise NotImplementedError("Please Implement this method")
