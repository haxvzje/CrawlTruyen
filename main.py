import requests, argparse, os, sys, shutil
from bs4 import BeautifulSoup
from ebooklib import epub

class Main:
    def __init__(self, sUrl: str):
        if __name__ == '__main__':
            self.chapter = 0
            self.book = 0
            self.bookData = None
            self.bookInfo = None
            self.sUrlInput = sUrl
            self.ebook = epub.EpubBook()
            self.chapterTuple = []
            self.chapterList = ['nav']
            self.main()
            
    def set_book_metadata(self, number: int):
        self.ebook.set_identifier(f"{(self.bookData['uri_name']).replace('-', '')}{number}")
        self.ebook.set_title(self.bookInfo['Tên truyện'])
        self.ebook.add_author(self.bookInfo['Tác giả'])
        self.ebook.set_language("vi")
        
        if not os.path.exists('temp'):
            os.mkdir('temp')
        if not os.path.exists('output'):
            os.mkdir('output')
        if not os.path.exists('temp/' + f"{self.bookData['uri_name']}-quyen-{number}"):
            os.mkdir('temp/' + f"{self.bookData['uri_name']}-quyen-{number}")
        if not os.path.exists('output/' + f"{self.bookData['uri_name']}"):
            os.mkdir('output/' + f"{self.bookData['uri_name']}")
            
        # intro chapter
        c1 = epub.EpubHtml(title='Introduction', file_name=f"temp/{self.bookData['uri_name']}-quyen-{number}/intro.xhtml", lang='vi')
        c1.content=f"<html><head></head><body><center><h1>{self.bookInfo['Tên truyện']}</h1><p>Author: {self.bookInfo['Tác giả']}</p><p>Release Date: {self.bookInfo['Ngày cập nhật']}</p></center></body></html>"
        self.ebook.add_item(c1)
        
        self.chapterTuple.append(c1)
        self.chapterList.append(c1)

    def get_url(self, url: str, retries=3) -> str:
        session = requests.Session()
        session.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
                "Accept-Encoding": "*",
                "Connection": "keep-alive"
            }
        try:
            response = session.get(url)
            if response.status_code == 200:
                # print(response.text)
                return response.text
            else:
                return "ERROR"
        except ValueError as err:
            print(err)
            if retries < 1:
                raise ValueError('No more retries!')
            return session.get(url, retries - 1)
        
        # try:
        #     session = requests.Session()
        #     session.headers = {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        #         "Accept-Encoding": "*",
        #         "Connection": "keep-alive"
        #     }
        #     # print(url)
        #     response = session.get(url, timeout=1000)
        #     if response.status_code == 200:
        #         # print(response.text)
        #         return response.text
        #     else:
        #         return "ERROR"
        # except Exception as e:
        #     return f"Traceback exeptions: {e}"
    
    def uri_split(self, url: str):
        # DONE
        uriList = url.split('/')
        self.bookData = {'site': uriList[2], 'uri_name': uriList[3]}
    
    def get_chapter(self, bookNum: int, bookData: dict):
        if bookNum == 1:
            tempUrlContent = self.get_url(f"https://{bookData['site']}/{bookData['uri_name']}/")
        else:
            tempUrlContent = self.get_url(f"https://{bookData['site']}/{bookData['uri_name']}-quyen-{bookNum}/")
        
        soup = BeautifulSoup(tempUrlContent, 'html.parser')
        divs = soup.find_all('div', class_='bai-viet-box')
        
        for div in divs:
            strong = div.find('strong', string="Danh sách các phần:")
            if strong:
                hr_count = len(div.find_all('hr'))
                self.chapter = hr_count
                break
        else:
            print("Không tìm thấy thông tin chapter.")
    
    def get_book(self, url: str):
        tempUrlContent = self.get_url(url)
        soup = BeautifulSoup(tempUrlContent, 'html.parser')
        divs = soup.find_all('div', class_='bai-viet-box')
        
        for div in divs:
            strong = div.find('strong', string="Danh sách truyện cùng bộ:")
            if strong:
                hr_count = len(div.find_all('hr'))
                self.book = hr_count
                break
        else:
            print("Không tìm thấy thông tin book.")
    
    def get_book_infomation(self, bookNum: int, bookData: dict):
        if bookNum == 1:
            soup = BeautifulSoup(self.get_url(f"https://{bookData['site']}/{bookData['uri_name']}/"), 'html.parser')
        else:
            soup = BeautifulSoup(self.get_url(f"https://{bookData['site']}/{bookData['uri_name']}-quyen-{bookNum}/"), 'html.parser')
        table = soup.find('table')
        data_dict = {}
        rows = table.find_all('tr')[1:] 
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                data_dict[key] = value
        self.bookInfo = data_dict
    
    def get_nd_truyen(self, bookNum: int, chapter: int, bookData: dict) -> str:
        print(f"    Dang crawl chapter {chapter}")
        
        suffix = "" if bookNum == 1 else f"-quyen-{bookNum}"
        url = f"https://{bookData['site']}/{bookData['uri_name']}{suffix}/{chapter}"
        
        soup = BeautifulSoup(self.get_url(url), 'html.parser')
        div_nd = soup.find('div', class_='ndtruyen')
        
        if not div_nd:
            return ""

        for em_tag in div_nd.find_all('em'):
            em_tag.decompose()

        signature_html = 'EBookCrawl by <strong>github@haxvzje</strong><br>Chúc bạn đọc sách vui vẻ!<br>'
        found_ad_tag = False
        
        for strong_tag in div_nd.find_all('strong'):
            if "Bạn đang đọc Quyển" in strong_tag.get_text():
                new_content = BeautifulSoup(signature_html, 'html.parser')
                strong_tag.replace_with(new_content)
                found_ad_tag = True
                break
            
        if not found_ad_tag and chapter == 1:
            new_signature = BeautifulSoup(signature_html, 'html.parser')
            div_nd.insert(0, new_signature)

        return div_nd.encode_contents().decode('utf-8').strip()
    
    def main(self):
        self.uri_split(self.sUrlInput)
        self.get_book(self.sUrlInput)
        self.get_book_infomation(1, self.bookData)
        print(
            f"Tên truyện: {self.bookInfo['Tên truyện']}\nNgày cập nhật: {self.bookInfo['Ngày cập nhật']}\nTác giả: {self.bookInfo['Tác giả']}\nSố lượng book: {self.book}\n"
        )
        
        with open('epub.css', 'r') as f:
            style = f.read() 
        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
        self.ebook.add_item(default_css)
        
        ###
        for i in range(1, self.book+1):
        # for i in range(1, 2+1):
            self.get_chapter(i, self.bookData)
            self.get_book_infomation(i, self.bookData)
            print(f"[*] Bat dau crawl '{self.bookInfo['Tên truyện']}'")
            self.set_book_metadata(i)
            for j in range(1, self.chapter+1):
            # for j in range(1, 5+1):
                content = self.get_nd_truyen(i, j, self.bookData)
                chapter = epub.EpubHtml(title=f'Chapter {j}', file_name=f"{self.bookData['uri_name']}-quyen-{i}/chapter-{j}.xhtml")
                chapter.content=content
                chapter.add_item(default_css)
                self.ebook.add_item(chapter)
                self.chapterTuple.append(chapter)
                self.chapterList.append(chapter)
            print()
            
            #create table of contents
            #- add section
            #- add auto created links to chapters

            self.ebook.toc = (tuple(self.chapterTuple))

            # add navigation files
            self.ebook.add_item(epub.EpubNcx(file_name=f"temp/{self.bookData['uri_name']}-quyen-{i}/toc.ncx"))
            self.ebook.add_item(epub.EpubNav(file_name=f"temp/{self.bookData['uri_name']}-quyen-{i}/nav.xhtml"))

            # create spine
            self.ebook.spine = self.chapterList

            # create epub file
            epub.write_epub(f"output/{self.bookData['uri_name']}/{self.bookInfo['Tên truyện']}.epub", self.ebook, {})
            
            self.ebook = epub.EpubBook()
            self.bookInfo = None
            self.chapterTuple = []
            self.chapterList = ['nav']
        if os.path.exists('temp'):
            shutil.rmtree('temp')

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        # sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(argument_default="-h", description="Simple crawler tool to crawl truyenfull, truyentv, truyensextv")
parser.add_argument("-l", "--link", help="link truyen can crawl", required=True)
args = parser.parse_args()

if ("http://" not in args.link):
    if ("https://" not in args.link):
        print("URL KHONG HOP LE")
        sys.exit(0)

try:
    Main(args.link)
except Exception as e:
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    print(f"[!] Error: {e}")
    sys.exit(0)
except KeyboardInterrupt:
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    print("\n[!] Cancelled!")
    sys.exit(0)