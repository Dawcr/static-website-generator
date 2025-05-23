from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
     
class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str = url

    def __eq__(self, node: 'TextNode') -> bool:
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    