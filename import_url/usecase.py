from data.book_repository import BookRepository
from data.comodity_repository import ComodityRepository
from data.http_client import HttpClient
from entities.account import Account
from entities.book import Book
from entities.comodity import Comodity


class ImportUrlUseCase(object):
    def __init__(self, http_client: HttpClient, book_repository: BookRepository,
                 comodity_repository: ComodityRepository):
        self.comodity_repository = comodity_repository
        self.http_client = http_client
        self.book_repository = book_repository

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
            account = self.get_account(xml_account, book)
            print(account.name)

    def get_account(self, xml_account, book: Book):
        account_id = xml_account.find('act:id', self.ns).text
        account = book.accounts[account_id] if account_id in book.accounts else None
        if not account:
            account = Account()
            account.id = account_id
            book.accounts[account_id] = account

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

        xml_comodity = xml_book.find('gnc:commodity', self.ns)
        book.comodity = self.get_comodity(xml_comodity)

        return book, xml_book

    def get_comodity(self, xml_comodity):
        comodity_id = xml_comodity.find('cmdty:id', self.ns).text
        comodity = self.comodity_repository.find_by_id(comodity_id)
        if not comodity:
            comodity = Comodity()
            comodity.id = comodity_id
            comodity.space = xml_comodity.find('cmdty:space', self.ns).text

        return comodity
