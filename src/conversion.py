from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from blocktype import BlockType
import re

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

def block_to_html_node(blocktype:BlockType, children, block):
    match blocktype:
        case BlockType.QUOTE:
            return ParentNode(tag="blockquote", children=children)
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=children)
        case BlockType.HEADING:
            amount = len(block.split(" ")[0])
            return ParentNode(tag=f"h{amount}", children=children)
        case BlockType.CODE:
            return ParentNode(tag="pre", children=children)
        case BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=children)
        case BlockType.ORDERED_LIST:
            return ParentNode(tag="ol", children=children)

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type:TextType):
    new_nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
            continue
        
        if delimiter not in old_node.text:
            new_nodes_list.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown syntax")

        for i, section in enumerate(parts):
            if (i+1) % 2 == 0:
                new_node = TextNode(section, text_type)
                new_nodes_list.append(new_node)
            else:
                new_node = TextNode(section, TextType.TEXT)
                new_nodes_list.append(new_node)
    return new_nodes_list

def extract_markdown_images(text) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\].*?\((.*?)\)", text)
    return matches
def extract_markdown_links(text) -> list[tuple]:
    matches = re.findall(r"\[(.*?)\].*?\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        s = old_node.text
        for i, tuple in enumerate(matches):
            delimiter = "!["+tuple[0]+"]"+"("+tuple[1]+")"
            parts = s.split(delimiter)
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
            s = "".join(parts[1:])
            if i+1 == len(matches) and len(s) != 0:
                new_nodes.append(TextNode(s, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes:list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        s = old_node.text
        for i, tuple in enumerate(matches):
            delimiter = "["+tuple[0]+"]"+"("+tuple[1]+")"
            parts = s.split(delimiter)
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
            s = "".join(parts[1:])
            if i+1 == len(matches) and len(s) != 0:
                new_nodes.append(TextNode(s, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    first_text_node = TextNode(text, TextType.TEXT)
    node_list = [first_text_node]

    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)

    return node_list

def markdown_to_blocks(markdown:str) -> list[str]:
    return_block_list = []
    block_list = markdown.split("\n\n")
    for block in block_list:
        block = block.strip()
        if len(block) == 0:
            continue
        return_block_list.append(block)
    return return_block_list

def block_to_block_type(block:str) -> BlockType:
    
    if re.match(r"^#{1,6} ", block) != None:
        return BlockType.HEADING
    elif re.match(r"^```.*?```$", block, re.DOTALL) != None:
        return BlockType.CODE
    elif re.fullmatch(r"^(>.*\n?)*", block, flags=re.MULTILINE) != None:
        return BlockType.QUOTE
    elif re.fullmatch(r"^(- .*\n?)*", block, flags=re.MULTILINE) != None:
        return BlockType.UNORDERED_LIST
    
    numbers_to_check = re.findall(r"^(\d+)\. .*\n?", block, flags=re.MULTILINE)
    number_of_rows_list = list(range(1, 1+len(block.split("\n"))))
    if list(map(lambda x: int(x), numbers_to_check)) == number_of_rows_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown:str) -> ParentNode:

    list_of_blocks = markdown_to_blocks(markdown)
    top_children = []

    for block in list_of_blocks:
        type_of_block = block_to_block_type(block)

        if type_of_block == BlockType.CODE:
            block = block.replace("```", "")
            children_html = [LeafNode(tag="code", value=block)]
            parent_of_block = block_to_html_node(type_of_block, children_html, block)
            top_children.append(parent_of_block)
        
        elif type_of_block == BlockType.HEADING:
            temp_block = block
            temp_block = "".join(re.findall(r"^#+ (.*)", temp_block))
            children_html = [LeafNode(tag=None, value=temp_block)]
            parent_of_block = block_to_html_node(type_of_block, children_html, block)
            top_children.append(parent_of_block)

        elif type_of_block == BlockType.UNORDERED_LIST:
            unordered_list_to_children = []
            for line in block.split("\n"):
                line = line.replace("- ", "", 1)

                list_of_text_nodes = text_to_textnodes(line)
                leafleafnode = []
                
                for textnode in list_of_text_nodes:
                    leafnode = text_node_to_html_node(textnode)
                    leafleafnode.append(leafnode)

                unordered_list_to_children.append(ParentNode("li", leafleafnode))
            parent_of_block = block_to_html_node(type_of_block, unordered_list_to_children, block)
            top_children.append(parent_of_block)
            
        elif type_of_block == BlockType.ORDERED_LIST:
            ordered_list_to_children = []
            for line in block.split("\n"):
                line = "".join(re.findall(r"^\d+\. (.*)", line))

                list_of_text_nodes = text_to_textnodes(line)
                leafleafnode = []
                
                for textnode in list_of_text_nodes:
                    leafnode = text_node_to_html_node(textnode)
                    leafleafnode.append(leafnode)

                ordered_list_to_children.append(ParentNode("li", leafleafnode))
            parent_of_block = block_to_html_node(type_of_block, ordered_list_to_children, block)
            top_children.append(parent_of_block)
        
        elif type_of_block == BlockType.QUOTE:
            ordered_list_to_children = []
            for line in block.split("\n"):
                line = "".join(re.findall(r"^>(.*)", line)).strip()
                ordered_list_to_children.append(LeafNode(tag=None, value=line))
            parent_of_block = block_to_html_node(type_of_block, ordered_list_to_children, block)
            top_children.append(parent_of_block)
        
        else:
            children = text_to_textnodes(block)
            
            children_html = []
            for textnode in children:
                children_html.append(text_node_to_html_node(textnode))

            parent_of_block = block_to_html_node(type_of_block, children_html, block)

            top_children.append(parent_of_block)
    

    top_parent = ParentNode(tag="div", children=top_children)
    return top_parent

if __name__ == "__main__":
    pass
