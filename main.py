from app.crawlers.hemoba.crawler import HemobaCrawler

def main():
    crawl = HemobaCrawler()
    crawl.execute()

if __name__ == "__main__":
    main()
