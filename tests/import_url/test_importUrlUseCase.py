from unittest import TestCase
from unittest.mock import Mock, MagicMock

from data.book_repository import BookRepository
from data.comodity_repository import ComodityRepository
from data.http_client import HttpClient
from entities.account import Account
from entities.book import Book
from import_url.callback import ImportUrlCallback
from import_url.usecase import ImportUrlUseCase


class TestImportUrlUseCase(TestCase):
    def setUp(self):
        self.http_client = Mock(HttpClient)
        self.book_repository = Mock(BookRepository)
        self.comodity_repository = Mock(ComodityRepository)

        self.usecase = ImportUrlUseCase(self.http_client, self.book_repository,
                                        self.comodity_repository)

    def test_import_url_success(self):
        EXPECTED_URL = 'ANY_URL'
        EXPECTED_BOOK = Book()
        EXPECTED_ACCOUNT = Mock()
        xml_account = Mock()
        xml_book = Mock()
        xml_book.findall = MagicMock(return_value=[xml_account])
        self.http_client.get_from_url = MagicMock(return_value=Mock())
        self.usecase.get_book = MagicMock(return_value=(EXPECTED_BOOK, xml_book))
        self.usecase.get_account = MagicMock(return_value=EXPECTED_ACCOUNT)
        callback = Mock(ImportUrlCallback)

        self.usecase.import_url(EXPECTED_URL, callback)

        self.http_client.get_from_url.assert_called_with(EXPECTED_URL)
        self.book_repository.update_or_create.assert_called_with(EXPECTED_BOOK)
        callback.on_success.assert_called_with(EXPECTED_BOOK)

    def test_import_url_failure(self):
        EXPECTED_URL = 'ANY_URL'
        callback = Mock(ImportUrlCallback)
        self.http_client.get_from_url = MagicMock(side_effect=RuntimeError())

        self.usecase.import_url(EXPECTED_URL, callback)

        callback.on_error.assert_called()

    def test_get_account(self):
        EXPECTED_ID = 'EXPECTED_ID'
        EXPECTED_NAME = 'EXPECTED_NAME'
        EXPECTED_TYPE = 'EXPECTED_TYPE'
        EXPECTED_PLACEHOLDER = True
        EXPECTED_PARENT_ID = 'EXPECTED_PARENT_ID'

        def find(match, ns):
            mock = Mock()

            if match == 'act:id':
                mock.text = EXPECTED_ID
            if match == 'act:name':
                mock.text = EXPECTED_NAME
            if match == 'act:type':
                mock.text = EXPECTED_TYPE
            if match == 'slot:key':
                mock.text = 'placeholder'
            if match == 'slot:value':
                mock.text = 'true' if EXPECTED_PLACEHOLDER else 'false'
            if match == 'act:parent':
                mock.text = EXPECTED_PARENT_ID

            return mock

        xml_account = Mock()
        xml_account.find = find
        xml_slot = Mock()
        xml_slot.find = find
        xml_account.findall = MagicMock(return_value=[xml_slot])
        account = Account()
        account.id = EXPECTED_PARENT_ID
        book = Mock()
        book.accounts = {EXPECTED_PARENT_ID: account}

        account = self.usecase.get_account(xml_account, book)

        assert account.id == EXPECTED_ID
        assert account.name == EXPECTED_NAME
        assert account.type == EXPECTED_TYPE
        assert account.is_placeholder == EXPECTED_PLACEHOLDER
        assert account.parent.id == EXPECTED_PARENT_ID

    def test_get_book(self):
        EXPECTED_ID = 'ANY_ID'
        mock = Mock()
        mock.text = EXPECTED_ID
        EXPECTED_XML_BOOK = Mock()
        EXPECTED_XML_BOOK.find = MagicMock(return_value=mock)
        gnucash_file = Mock()
        gnucash_file.find = MagicMock(return_value=EXPECTED_XML_BOOK)
        self.book_repository.find_by_id = MagicMock(return_value=None)
        self.usecase.get_comodity = MagicMock(return_value=Mock())

        book, book_xml = self.usecase.get_book(gnucash_file)

        assert book.id == EXPECTED_ID
        assert book_xml == EXPECTED_XML_BOOK
        self.usecase.get_comodity.assert_called_with(mock)

    def test_get_comodity(self):
        EXPECTED_ID = 'ANY_ID'
        EXPECTED_SPACE = 'ANY_SPACE'

        def find(id, ns):
            mock = Mock()

            if id == 'cmdty:id':
                mock.text = EXPECTED_ID
            if id == 'cmdty:space':
                mock.text = EXPECTED_SPACE

            return mock

        xml_comodity = Mock()
        xml_comodity.find = find
        self.comodity_repository.find_by_id = MagicMock(return_value=None)

        comodity = self.usecase.get_comodity(xml_comodity)

        assert comodity.id == EXPECTED_ID
        assert comodity.space == EXPECTED_SPACE
