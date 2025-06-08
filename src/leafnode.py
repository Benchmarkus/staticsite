from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        
        # if self.tag in ["p","b","i","s","q","code","blockquote","li","h1","h2","h3","h4","h5","h6"]:
        if self.props == None:
            return "<" + self.tag + ">" + self.value + "</" + self.tag + ">"
        # if self.tag == "a":
        else:
            return "<"+ self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
        # raise Exception("jotain kusee")