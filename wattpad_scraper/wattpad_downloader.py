from typing import List
from bs4 import BeautifulSoup
from wattpad_scraper.models import Author, Book, Chapter, Status
from wattpad_scraper.utils import get, Log
from urllib.parse import quote
import os


class Wattpad:
    def __init__(self,username=None,password=None,verbose=False,cookie_file=None) -> None:
        """
        Initialize the Wattpad class.
        
        Args:
            username (string)(optional): username or email
            password (string)(optional): password
            verbose (bool)(optional): verbose mode default False
        """
        self.verbose = verbose
        self.log = Log(name="wattpad_log", verbose=verbose)

        self.main_url = "https://www.wattpad.com"
        if username is not None and password is not None:
            os.environ['WATTPAD_USERNAME'] = username
            os.environ['WATTPAD_PASSWORD'] = password
            self.log.print("Logging in as {}".format(username),color="green")
        elif cookie_file is not None:
            os.environ['WATTPAD_COOKIE_FILE'] = cookie_file
            self.log.print("Logging in with Cookie File {}".format(cookie_file),color="green")

    def get_book_by_url(self, url) -> Book:
        """
        Args:
            url (string): book url

        Returns:
            Book: returns a Book object

            Book object has the following attributes:
                url (string): book url
                name (string): book name
                author (Author): author object
                img_url (string): book image url
                tags (list): list of tags
                description (string): book description
                published (string): book published date
                reads (int): book reads
                votes (int): book votes
                status (Status): book status
                isMature (bool): book is mature
                chapters (list): list of chapter objects
        """

        response = get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get book stats
        stats = soup.find(class_='new-story-stats')
        lis = stats.find_all('li')

        reads = lis[0].find(
            class_="sr-only").get_text().replace('Reads', '').replace(',', '').strip()
        reads = int(reads)

        votes = lis[1].find(
            class_="sr-only").get_text().replace('Votes', '').replace(',', '').strip()
        votes = int(votes)

        parts = lis[2].find(
            class_="sr-only").get_text().replace('Parts', '').strip()
        parts = int(parts)

        # class : story-badges
        badges = soup.find(class_='story-badges')
        completed = badges.find(
            class_="tag-item").get_text().lower().startswith('com')
        status = None
        if completed:
            status = Status.COMPLETED
        else:
            status = Status.ONGOING

        # is mature class mature
        mature = badges.find(class_="mature") is not None

        # published sr-only > ex. Complete, First published Sep 25, 2018
        published = badges.find(
            class_='sr-only').get_text().split('First published ')[1]

        # description class description-text
        description = soup.find(class_='description-text').get_text()

        # Get Chapters - Class: "story-chapter-list" > li > List<a> > text,href
        toc = soup.find(class_='table-of-contents')
        lis = toc.find_all('li')
        chapters = []
        for n,li in enumerate(lis):
            a = li.find('a')
            url = a.get('href')
            if url.startswith('/'):
                url = self.main_url + url
            ch = Chapter(
                url=url, title=a.get_text().strip().replace('\n', ' '), chapter_number=n+1)
            chapters.append(ch)

        # Get Title class: "sr-only" > text (title)
        title = soup.find(class_='sr-only').get_text()

        # Get Author class: "author-info" > img,a > img:src,a:href,a:text
        author_info = soup.find(class_='author-info')
        img_url = author_info.find('img').get('src')
        if img_url.startswith('/'):
            img_url = self.main_url + img_url
        a = author_info.find('a')
        author_url = a.get('href')
        if author_url.startswith('/'):
            author_url = self.main_url + author_url
        author = Author(url=author_url, name=a.get_text(),
                        author_img_url=img_url)

        # Get Image class: "story-cover" > img > src
        book_img_url = soup.find(class_='story-cover').find('img').get('src')
        if book_img_url.startswith('/'):
            book_img_url = self.main_url + book_img_url

        # Get Tags class: tag-items > li > a > text
        tags = []
        tag_items = soup.find(class_='tag-items')
        if tag_items is not None:
            lis = tag_items.find_all('li')
            for li in lis:
                tags.append(li.find('a').get_text())

        # Get Book object
        book = Book(url=url, title=title, author=author, img_url=book_img_url, description=description,
                    published=published, isMature=mature, reads=reads, votes=votes, chapters=chapters, total_chapters=parts, tags=tags, status=status)
        return book

    def search_books(self, query: str,limit:int=15,mature:bool=True,free:bool=True,paid:bool=True,completed:bool=False,show_only_total:bool=False) -> List[Book]:
        """
        Args:
            query (string): search query

        Returns:
            List[Book]: returns a list of Book objects
        """
        self.log.debug("Searching for '{}'".format(query),"with options: mature={},free={},paid={},completed={},show_only_total={}".format(mature,free,paid,completed,show_only_total))
        mature_str = "&mature=true" if mature else ""
        free_str = "&free=1" if free else ""
        paid_str = "&paid=1" if paid else ""
        completed_str = "&filter=complete" if completed else ""

        parsed_query = quote(query)
        url = f"https://www.wattpad.com/v4/search/stories?query={parsed_query}{completed_str}{mature_str}{free_str}{paid_str}&fields=stories(id,title,voteCount,readCount,commentCount,description,completed,mature,cover,url,isPaywalled,length,language(id),user(name),numParts,lastPublishedPart(createDate),promoted,sponsor(name,avatar),tags,tracking(clickUrl,impressionUrl,thirdParty(impressionUrls,clickUrls)),contest(endDate,ctaLabel,ctaURL)),chapters(url),total,tags,nexturl&limit={limit}&offset=0"
        response = get(url)
        json_data = response.json()
        if not show_only_total:
            try:
                self.log.info(f"Found {json_data['total']} results")
                books = []
                for book in json_data['stories']:
                    b = Book.from_json(book)
                    books.append(b)
                return books
            except Exception as e:
                self.log.error(f"[{response.status_code}] {response.text}\nError: {e}")
                self.log.info(f"if you can't solve this error, please report it to the developer")
                self.log.info(f"Or submit a bug report at https://github.com/shhossain/wattpad-scraper/issues")
                return []
        else:
            try:
                return json_data['total']
            except Exception as e:
                self.log.error(f"[{response.status_code}] {response.text}\nError: {e}")
                self.log.info(f"if you can't solve this error, please report it to the developer")
                self.log.info(f"Or submit a bug report at https://github.com/shhossain/wattpad-scraper/issues")



        


# if __name__ == "__main__":
#     wattped = Wattpad()
#     wattped.search_book('harry potter')