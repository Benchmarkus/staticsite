import unittest

from textnode import TextNode, TextType
from blocktype import BlockType
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type

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
        
    def test_extract_markdown_images(self):
        func = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        result = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(func, result)

    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        func = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(func, result)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        text = "### Heading"
        result1 = BlockType.HEADING
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)
    
    def test_block_to_block_type_paragraph(self):
        text = "jotain tekstiä blaa"
        result1 = BlockType.PARAGRAPH
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)
    
    def test_block_to_block_type_code(self):
        text = '```jotain koodia\nlisää koodia```'
        result1 = BlockType.CODE
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)

    def test_block_to_block_type_quote(self):
        text = '> jotain koodia\n>lisää koodia'
        result1 = BlockType.QUOTE
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)

    def test_block_to_block_type_unordered_list(self):
        text = '- jotain koodia\n- lisää koodia'
        result1 = BlockType.UNORDERED_LIST
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)

    def test_block_to_block_type_ordered_list(self):
        text = '1. jotain koodia\n2. lisää koodia\n3. asd\n4. asd\n5. asd\n6. asd\n7. asd\n8. asd\n9.  asd\n10. asd'
        result1 = BlockType.ORDERED_LIST
        func1 = block_to_block_type(text)
        self.assertEqual(func1, result1)
