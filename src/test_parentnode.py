import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node0 = ParentNode("p",
        [LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),],)

        self.assertEqual(node0.to_html(), r'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

        node1 = ParentNode("p",[LeafNode("b", "Bold text")])

        self.assertEqual(node1.to_html(), r'<p><b>Bold text</b></p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

if __name__ == "__main__":
    unittest.main()