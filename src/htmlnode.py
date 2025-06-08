

class HTMLNode():
    def __init__(self, tag:str=None, value:str=None, children:list[object]=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for k, v in self.props.items():
            row = " " + k + "=" + '"' + v + '"'
            result += row

        return result

    def __repr__(self):
        return f"HTMLNode: tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"
    
    def __eq__(self, other):
        if (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        ):
            return True
        return False