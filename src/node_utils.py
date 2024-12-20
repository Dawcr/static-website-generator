import re

from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_utils import BlockType, markdown_to_blocks, block_to_block_type


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


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks_tuple = list(map(lambda block: (block_to_block_type(block), block), markdown_to_blocks(markdown)))
    
    children: list[list[HTMLNode]] = []
    for item in blocks_tuple:
        children.append(block_to_html_node(*item))
    
    return ParentNode("div", children) 

def block_to_html_node(block_type, block):
    if block_type in [BlockType.HEADING1, BlockType.HEADING2, BlockType.HEADING3, BlockType.HEADING4, BlockType.HEADING5, BlockType.HEADING6]:
        return header_to_htmlnode(block_type, block)
    if block_type in [BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST]:
        return list_to_htmlnode(block_type, block)
    if block_type == BlockType.CODE:
        return code_to_htmlnode(block)
    if block_type == BlockType.QUOTE:
        return quotes_to_htmlnode(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_htmlnode(block)
    raise ValueError("Invalid block type")
    
def text_to_children(text: str) -> list[LeafNode]:
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

    
def header_to_htmlnode(type: BlockType, block: str) -> ParentNode:
    # header block should start with 1 to 6 # followed by space and then header text
    if not block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        raise ValueError("Incorrect header format")
    
    # remove the preceding 1-6 # followed by space by splitting at space and returning the second half
    text = block.split(maxsplit=1)[1]
    # Blocktype.HEADING<n> is set to value "heading <n>", taking advantage of it and splitting at space to return <n>, could also use type.value[8], but trying to avoid magic numbers
    header_number = f"h{type.value.split()[1]}"
    
    return ParentNode(header_number, text_to_children(text))


def code_to_htmlnode(block: str) -> ParentNode:
    # code block should start and end with 3 backticks
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Incorrect code block format")
    
    # remove the starting and ending ```
    text = block[4:-3]
    return ParentNode("pre", [ParentNode("code", text_to_children(text))])
    
    
def list_to_htmlnode(type: BlockType, block: str) -> ParentNode:
    items = block.split('\n')
    children: list[LeafNode] = []
    start = block[:2]
    
    for index, item in enumerate(items, start=1):
        if type == BlockType.ORDERED_LIST:
            start = f"{index}. "
        
        # ordered lists start with number followed by a period and space(3 chars), unordered lists start with * or - followed by space(2 chars)
        if not item.startswith(start):
            raise ValueError(f"List item not starting with {start}")
        
        text = item.lstrip(start)
        children.append(ParentNode("li", text_to_children(text)))
        
    return ParentNode("ol" if type == BlockType.ORDERED_LIST else "ul", children)
    
    
def quotes_to_htmlnode(block: str) -> ParentNode:
    items = block.split('\n')
    lines: list[str] = []
    for item in items:
        # every line in a quote block starts with a >
        if not item.startswith('>'):
            raise ValueError("Incorrect quote block format")
        lines.append(item[1:].strip())
    text = " ".join(lines)
    
    return ParentNode("blockquote", text_to_children(text))


def paragraph_to_htmlnode(block: str) -> ParentNode:
    lines = block.split('\n')
    text = " ".join(lines)
    return ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(text))))

