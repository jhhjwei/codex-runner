import unittest

from scraper import PageParser, allowed_link, canonicalize


class PageParserTest(unittest.TestCase):
    def test_extracts_visible_text_title_and_links(self) -> None:
        parser = PageParser()
        parser.feed(
            """
            <html>
              <head><title> Demo Page </title><style>.x{}</style></head>
              <body>
                <h1>Hello</h1>
                <p>Useful text</p>
                <script>secret()</script>
                <a href="/next">Next</a>
              </body>
            </html>
            """
        )
        title, text, links = parser.result()
        self.assertEqual(title, "Demo Page")
        self.assertIn("Hello", text)
        self.assertIn("Useful text", text)
        self.assertNotIn("secret", text)
        self.assertEqual(links, ["/next"])

    def test_url_rules(self) -> None:
        self.assertEqual(canonicalize("HTTPS://Example.COM"), "https://example.com/")
        self.assertTrue(allowed_link("https://example.com/a", "example.com", True))
        self.assertFalse(allowed_link("https://other.com/a", "example.com", True))
        self.assertTrue(allowed_link("https://other.com/a", "example.com", False))
        self.assertFalse(allowed_link("mailto:test@example.com", "example.com", False))


if __name__ == "__main__":
    unittest.main()
