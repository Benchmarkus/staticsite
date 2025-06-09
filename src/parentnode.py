from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag value")
        if self.children == []:
            raise ValueError("no children listed")
        
        html_string = ""
        for child in self.children:
            html_string += child.to_html()

        return "<" + self.tag + ">" + html_string + "</" + self.tag + ">"
