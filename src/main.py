from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={text_node.text: text_node.url})
    raise Exception("texttype doesn't match any")

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type:TextType):
    new_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0 or len(parts) == 1:
            raise Exception("invalid markdown syntax")

        for i, section in enumerate(parts):
            if (i+1) % 2 == 0:
                new_node = TextNode(section, text_type)
                new_nodes_list.append(new_node)
            else:
                new_node = TextNode(section, TextType.TEXT)
                new_nodes_list.append(new_node)
    return new_nodes_list



