class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        # return " ".join(map(lambda prop: f"{prop}: \"{self.props[prop]}\"", self.props)) # cool but harder to read
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}: "{self.props[prop]}"'
        return props_html[1:]
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    