import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node3 = TextNode("T", TextType.BOLD)
        node4 = TextNode("T", TextType.TEXT)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("T", TextType.LINK)
        node6 = TextNode("T", TextType.BOLD)
        self.assertNotEqual(node5, node6)

if __name__ == "__main__":
    unittest.main()