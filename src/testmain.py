import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter

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
    
    def test_raises_exception_from_wrong_texttype(self):
        node = TextNode("This is text", "wrong text type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ",TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is ",TextType.TEXT),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" text", TextType.TEXT)])
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is ",TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" text", TextType.TEXT)])