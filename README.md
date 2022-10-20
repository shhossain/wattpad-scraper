# Wattpad Scraper(wattpad stories downloader)
Get wattpad stories, download wattpad stories, convert wattpad stories to ebook (epub/pdf[In Development])

## Major Features
- Search books 
- Get book by wattpad url
- Convert books to epub
- Login to wattpad

### Important Links
- [GitHub](https://github.com/shhossain/wattpad-scraper)
- [PYPI](https://pypi.org/project/wattpad-scraper/)

## Installation

```bash
pip install wattpad-scraper
```

## Usage

### Get Book By Url
```python
from wattpad_scraper import Wattpad

wattped = Wattpad()
# wattpad = Wattpad(verbose=True)  if you want to see output in console
book_url = "https://www.wattpad.com/story/162756571-bending-the-rules-the-rules-1"
book = wattped.get_book_by_url(book_url)
print(book.title) # "Bending the Rules: The Rules 1"
print(book.author.name, book.author.url) 
print(book.description)
print(book.chapters)
print(book.chapters[0].title,book.chapters[0].content)

# Content is a List of strings and image urls.

```

### Search Books
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
books = wattpad.search_books('harry potter by joekih01',completed=True,mature=True,free=True,paid=True,limit=10) 
print(books[0].chapters[0].content) # on search book chapters have to load first so it may take a while
print(len(books)) # 10
```

### Create Users Book List
```python
#First login to perform actions on your book list
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.create_reading_list("Super Fly")
```

### Get Users Book List
Gets the Books in a reading list
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

# By default without passsing any arguement it returns all your reading lists 
readingList.get_reading_list()

#Get your reading list by it's title
readingList.get_reading_list(title="Super Fly")

# Get all users reading list
readingList.get_reading_list(username="Ghost_Lord")

#Get the reading list of a user by their title
readingList.get_reading_list(title="GEMS", username="Ghost_Lord")
```


### Delete Reading List
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.delete_reading_list("Super Fly")
```


### Add a book to a reading list
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.add_to_reading_list(urlOfBook="https://www.wattpad.com/story/116064909-around-the-world-in-80-days-completed", titleOfReadingList="Hype")
```

### Get Authors Book List
```python
from wattpad_scraper.utils import ReadingList

readingList = ReadingList()

readingList.author_book_list("amberkbryant")

```


### Convert Book to Epub
```python
from wattpad_scraper import Wattpad as wt

w = wt()
books = w.search_books('harry potter by joekih01')
book = books[0]
book.convert_to_epub() # will save book to epub file in current directory

# book.convert_to_epub(loc='/path/to/save/book/to/epub') # to save book to specific location
# book.convert_to_epub(verbose=False) # to disable terminal outputs while converting

```

### Auth System (Beta) (More Features are coming soon)
```python
from wattpad_scraper import Wattpad as wt

w = wt("wattpad_username","wattpad_password")
book= w.search_books("Rules") 
contents = book.chapters[2].content
# better search books that are not shown in search results for non logged users.
# More features are coming soon.
```

#### Cookie authentication
1. Download an extension called "Cookie - Editor" in your browser.
2. Open the extension and click Export.
3. Save copied text in to a file and rename with the `` .json`` extension.
4. Copy file location
```python
from wattpad_scraper import Wattpad as wt

w = wt(cookie_file='/home/Desktop/wattpad-cookies.json')
w.search_books("Rules")
```

