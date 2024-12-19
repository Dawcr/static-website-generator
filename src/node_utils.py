import re

from textnode import TextType, TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Trying to convert text node with invalid text type: {text_node.text_type}")
        
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        # only splitting TextType.TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        
        # if the lenght is not odd then a closing delimiter is missing
        if len(split_text) % 2 != 1 and len(split_text) > 1:
            raise Exception("closing delimiter missing")
        
        for index, item in enumerate(split_text):
            if not item:
                continue
            # closed_delim open_delim closed_delim...
            new_nodes.append(TextNode(item, TextType.TEXT if index % 2 == 0 else text_type))
            
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    #return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    # using regex provided by boot.dev to match ![alt_text](url)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    #return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    # using regex provided by boot.dev to match [anchor_text](url)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    
    return split_nodes_imagelink(old_nodes, TextType.IMAGE)
    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    return split_nodes_imagelink(old_nodes, TextType.LINK)


def split_nodes_imagelink(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    if text_type != TextType.IMAGE and text_type != TextType.LINK:
        raise ValueError("split_nodes_imagelink only works with images and links")
    
    # decide the right extractor to use
    extractor = extract_markdown_images if text_type == TextType.IMAGE else extract_markdown_links
    
    node_links = list(map(lambda node: extractor(node.text), old_nodes))
    
    if not node_links:
        return old_nodes
    
    new_nodes: list[TextNode] = []
    
    #![alt_text](url) for images [anchor_text](url) for links
    def delimiter(text: str, url: str) -> str:
        return ('!' if text_type == TextType.IMAGE else "") + f"[{text}]({url})"
    
    for links_list, node in zip(node_links, old_nodes):
        if not links_list:
            new_nodes.append(node)
            continue
            
        split_text = [node.text]
        
        for text, url in links_list:
            split_text = split_text[-1].split(delimiter(text, url), 1)
            
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], node.text_type))
            new_nodes.append(TextNode(text, text_type, url))
            
        # append the last piece of text if it is not empty  
        if split_text[-1]:
            new_nodes.append(TextNode(split_text[-1], node.text_type))
    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    node_delimiters = {
        TextType.BOLD : "**",
        TextType.ITALIC : "*",
        TextType.CODE : "`",
    }
    nodes = [TextNode(text, TextType.TEXT)]
    
    for type, delimiter in node_delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, type)
        
    return split_nodes_image(split_nodes_link(nodes))