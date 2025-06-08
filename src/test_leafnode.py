import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node0 = LeafNode("p", "This is a paragraph of text.")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node0.to_html(), r"<p>This is a paragraph of text.</p>")
        self.assertEqual(node1.to_html(), r'<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()