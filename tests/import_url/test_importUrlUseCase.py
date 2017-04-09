from unittest import TestCase
from unittest.mock import Mock, MagicMock

from data.account_repository import AccountRepository
from data.book_repository import BookRepository
from data.comodity_repository import ComodityRepository
from data.http_client import HttpClient
from import_url.usecase import ImportUrlUseCase


class TestImportUrlUseCase(TestCase):
    def setUp(self):
        self.http_client = Mock(HttpClient)
        self.book_repository = Mock(BookRepository)
        self.account_repository = Mock(AccountRepository)
        self.comodity_repository = Mock(ComodityRepository)

        self.usecase = ImportUrlUseCase(self.http_client, self.book_repository, self.account_repository,
                                        self.comodity_repository)

    def test_import_url(self):
        EXPECTED_URL = 'ANY_URL'
        EXPECTED_BOOK = Mock()
        EXPECTED_ACCOUNT = Mock()
        xml_account = Mock()
        xml_book = Mock()
        xml_book.findall = MagicMock(return_value=[xml_account])
        self.http_client.get_from_url = MagicMock(return_value=Mock())
        self.usecase.get_book = MagicMock(return_value=(EXPECTED_BOOK, xml_book))
        self.usecase.get_account = MagicMock(return_value=EXPECTED_ACCOUNT)

        self.usecase.import_url(EXPECTED_URL)

        self.http_client.get_from_url.assert_called_with(EXPECTED_URL)
        self.book_repository.update_or_create.assert_called_with(EXPECTED_BOOK)
        self.account_repository.update_or_create.assert_called_with(EXPECTED_ACCOUNT)

    def test_get_account(self):
        EXPECTED_ID = 'EXPECTED_ID'
        EXPECTED_NAME = 'EXPECTED_NAME'
        EXPECTED_TYPE = 'EXPECTED_TYPE'
        EXPECTED_PLACEHOLDER = True

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

            return mock

        self.account_repository.find_by_id = MagicMock(return_value=None)
        xml_account = Mock()
        xml_account.find = find
        xml_slot = Mock()
        xml_slot.find = find
        xml_account.findall = MagicMock(return_value=[xml_slot])

        account = self.usecase.get_account(xml_account)

        assert account.id == EXPECTED_ID
        assert account.name == EXPECTED_NAME
        assert account.type == EXPECTED_TYPE
        assert account.is_placeholder == EXPECTED_PLACEHOLDER

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
