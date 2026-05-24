class HTMLNode:
    def __init__(self, tag:str|None = None, 
                 value:str|None = None, 
                 children:list["HTMLNode"]|None = None, 
                 props:dict[str,str]|None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_line = ""
        if self.props:
            for key, value in self.props.items():
                html_line += f" {key}='{value}'"
        return html_line
    
    def __repr__(self):
        return f"""{self.__class__.__name__}
        (tag = {self.tag}, 
        value = {self.value}, 
        children = {self.children}, 
        props = {self.props})"""

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return(
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
    
class LeafNode(HTMLNode):
    def __init__(self,
                 tag:str|None, 
                 value:str|None, 
                 props:dict[str,str]|None = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode has no value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"""{self.__class__.__name__}
        (tag = {self.tag}, 
        value = {self.value}, 
        props = {self.props})"""

class ParentNode(HTMLNode):
    def __init__(self, 
                 tag:str, 
                 children:list["HTMLNode"], 
                 props:dict[str, str]|None=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode children doesn't have a value")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"