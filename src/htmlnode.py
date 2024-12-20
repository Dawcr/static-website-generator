class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None) -> None:
        self.tag: str = tag
        self.value: str = value
        self.children: list = children
        self.props: dict = props
        
    def to_html(self) -> None:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self) -> str:
        if self.value is None: # img tag has no value
            raise ValueError("Leaf node has no value")
        if not self.tag:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[LeafNode], props: dict[str, str] = None) -> None:
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent node has no tag")
        if not self.children:
            raise ValueError("Parent node has no children")
        return f"<{self.tag}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
