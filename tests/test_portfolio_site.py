from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))


class PortfolioSiteTests(unittest.TestCase):
    def test_case_study_is_valid_html_and_links_home(self):
        page = ROOT / "case-studies" / "ecommerce-behavior-analysis.html"
        parser = LinkCollector()
        parser.feed(page.read_text(encoding="utf-8"))

        self.assertIn("../index.html", parser.links)
        self.assertIn("../styles.css", page.read_text(encoding="utf-8"))
        self.assertIn("課堂團隊案例", page.read_text(encoding="utf-8"))
        self.assertIn("原始資料與程式碼未公開", page.read_text(encoding="utf-8"))

    def test_home_page_links_to_case_study(self):
        page = ROOT / "index.html"
        contents = page.read_text(encoding="utf-8")

        self.assertIn("case-studies/ecommerce-behavior-analysis.html", contents)
        self.assertIn("電商行為資料與文案分析", contents)


if __name__ == "__main__":
    unittest.main()
