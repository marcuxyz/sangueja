from app.crawlers.hemoba.crawler import Crawler

def main():
    crawl = Crawler()
    crawl.perform()
    crawl.send_alert()


if __name__ == "__main__":
    main()
