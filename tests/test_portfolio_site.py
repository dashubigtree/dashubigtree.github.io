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

    def test_home_page_has_personal_introduction(self):
        contents = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("我是徐澍萭（Benson）", contents)
        self.assertIn("LLM、RAG 與 AI Agent", contents)
        self.assertIn("金融業知識庫問答與防詐資料分析", contents)

    def test_home_page_has_four_project_backed_capabilities(self):
        contents = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertEqual(contents.count('class="capability-card"'), 4)
        self.assertIn("LLM &amp; RAG 系統", contents)
        self.assertIn("資料分析 &amp; 機器學習", contents)
        self.assertIn("自然語言處理 &amp; 文字探勘", contents)
        self.assertIn("電腦視覺 &amp; 運動科技", contents)

    def test_header_has_only_github_and_linkedin_links(self):
        contents = (ROOT / "index.html").read_text(encoding="utf-8")
        header = contents[contents.index("<header") : contents.index("</header>")]

        self.assertIn("https://github.com/dashubigtree", header)
        self.assertIn("https://www.linkedin.com/in/%E6%BE%8D%E8%90%AD-%E5%BE%90-bensonhsu", header)
        self.assertNotIn('href="#projects"', header)
        self.assertNotIn('href="#about"', header)
        self.assertNotIn("case-studies/ecommerce-behavior-analysis.html", header)

    def test_badminton_project_is_marked_in_progress(self):
        contents = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<h3>Badminton CV</h3>', contents)
        self.assertIn('class="project-status"', contents)
        self.assertIn('專案狀態：進行中', contents)

    def test_projects_appear_in_the_intended_order(self):
        contents = (ROOT / "index.html").read_text(encoding="utf-8")
        expected_titles = [
            "Badminton CV",
            "電商行為資料與文案分析",
            "Agentic AI &amp; RAG",
            "BERTopic 文字主題建模",
            "AICUP 2025 Table Tennis",
        ]

        positions = [contents.index(title) for title in expected_titles]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
