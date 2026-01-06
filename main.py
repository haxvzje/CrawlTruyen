def scan_chapter(url: str) -> list:
    setting = Setting()
    print(setting.SITE)

def uri_split(url: str) -> dict:
    childUrl = url.split('/')
    return {'originUrl': childUrl[2], 'URIName': childUrl[3]}
    

def main():
    str_truyenUrl = input('URL > ')
    print(uri_split(str_truyenUrl))

class Setting():
    SITE = "https://truyensextv2.com/"

main()
