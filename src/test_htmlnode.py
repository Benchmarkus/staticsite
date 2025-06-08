import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_isinstance(self):
        node1 = HTMLNode("<a>", "testinks", None, None)
        self.assertIsInstance(node1, HTMLNode)

    def test_eq(self):
        node0 = HTMLNode("ssss", "l", None, {"href":"https://www.google.com","target":"_blank"})
        self.assertEqual(node0.props_to_html(), r' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()