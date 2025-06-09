import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestMain(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_eq_bold(self):
        node = TextNode("This is a node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a node")
    
    def test_eq_image(self):
        node = TextNode("This is text", TextType.IMAGE, "www.kuva.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props[node.text], "www.kuva.com")
   
    def test_eq_link(self):
        node = TextNode("This is text", TextType.LINK, "www.kuva.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["href"], "www.kuva.com")
        self.assertEqual(html_node.tag, "a")