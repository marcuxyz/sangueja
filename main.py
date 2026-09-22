import argparse

from app.crawlers.hemoes.crawler import HemoesCrawler
from app.crawlers.hemoba.crawler import HemobaCrawler


CRAWLERS = {
    "hemoba": HemobaCrawler,
    "hemoes": HemoesCrawler
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bloodcenter",
        choices=CRAWLERS.keys(),
        help="Executa deteminado crawler de acordo com o valor passado"
    )
    args = parser.parse_args()

    if args.bloodcenter:
        crawler = CRAWLERS[args.bloodcenter]()
        crawler.execute()
        return

    for crawler in CRAWLERS.values():
        crawl = crawler()
        crawl.execute()


if __name__ == "__main__":
    main()
