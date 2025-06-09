from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        
        if self.tag == None:
            return f"{self.value}"

        if self.props == None:
            return "<" + self.tag + ">" + self.value + "</" + self.tag + ">"
        else:
            return "<"+ self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"