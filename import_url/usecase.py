from data.account_repository import AccountRepository
from data.book_repository import BookRepository
from data.http_client import HttpClient
from entities.account import Account
from entities.book import Book


class ImportUrlUseCase(object):
    def __init__(self, http_client: HttpClient, book_repository: BookRepository, account_repository: AccountRepository):
        self.http_client = http_client
        self.book_repository = book_repository
        self.account_repository = account_repository

        self.ns = {
            'gnc': 'http://www.gnucash.org/XML/gnc',
            'act': 'http://www.gnucash.org/XML/act',
            'slot': 'http://www.gnucash.org/XML/slot',
            'book': 'http://www.gnucash.org/XML/book'
        }

    def import_url(self, url):
        gnucash_file = self.http_client.get_from_url(url)

        book, xml_book = self.get_book(gnucash_file)
        self.book_repository.update_or_create(book)

        for xml_account in xml_book.findall('gnc:account', self.ns):
            account = self.get_account(xml_account)
            self.account_repository.update_or_create(account)
            print(account.name)

    def get_account(self, xml_account):
        account_id = xml_account.find('act:id', self.ns).text
        account = self.account_repository.find_by_id(account_id)
        if not account:
            account = Account()
            account.id = account_id

        account.name = xml_account.find('act:name', self.ns).text
        account.type = xml_account.find('act:type', self.ns).text
        for xml_slot in xml_account.findall('slot', self.ns):
            if xml_slot.find('slot:key', self.ns).text == 'placeholder':
                account.is_placeholder = xml_slot.find('slot:value', self.ns).text == 'true'

        return account

    def get_book(self, gnucash_file):
        xml_book = gnucash_file.find('gnc:book', self.ns)
        book_id = xml_book.find('book:id', self.ns).text

        book = self.book_repository.find_by_id(book_id)

        if not book:
            book = Book()
            book.id = book_id

        return book, xml_book
