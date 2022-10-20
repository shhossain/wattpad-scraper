import pytest
from wattpad_scraper import Wattpad
from wattpad_scraper.utils.reading_list import ReadingList

EXAMPLE_URL = "https://www.wattpad.com/story/48217861-ruins-harry-potter-1"
EXAMPLE_AUTHOR = "haIfblood"

class TestWattpadDownloader:
    
  def test_book_exists(self):
    wattpad = Wattpad()
    book = wattpad.get_book_by_url(EXAMPLE_URL)
    assert book is not None

  def test_harry_in_tags(self):
    wattpad = Wattpad()
    book = wattpad.get_book_by_url(EXAMPLE_URL)
    assert "harry" in book.tags

  def test_find_correct_author(self):
    wattpad = Wattpad()
    book = wattpad.get_book_by_url(EXAMPLE_URL)
    assert book.author.name == "haIfblood"

  def test_get_author_book_list(self):
    book_list= ReadingList().author_book_list(EXAMPLE_AUTHOR)
    assert type(book_list) == dict

  def test_get_reading_list(self):
    reading_list = ReadingList().get_reading_list(username=EXAMPLE_AUTHOR)
    assert type(reading_list) == list




if __name__ == "__main__":
  pytest.main()
  