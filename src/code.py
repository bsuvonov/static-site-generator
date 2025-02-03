import re
from src.textnode import *
from src.htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            
            if delimiter not in old_node.text:
                new_nodes.append(old_node)
                continue

            parts = old_node.text.split(delimiter)


            # handle two delimiters with empty inline text
            # delimiters should show as it is: aabc****def should result in TEXT type node
            new_parts = []
            cnt = 0
            for i in range(len(parts)):
                if cnt > 0:
                    cnt-=1
                    continue
                if len(parts[i])!=0 or i%2==0:
                    new_parts.append(parts[i])
                else:
                    i += 1
                    if i < len(parts):
                        new_parts[-1] += delimiter*2 + parts[i]
                        cnt+=1
                    else:
                        new_parts[-1] += delimiter
            
            # If there are odd number of delimiters, then keep the last one as it is
            if(len(new_parts)%2==0):
                new_parts[-2] += delimiter + new_parts[-1]
                new_parts.pop()


            type_used = None
            match delimiter:
                case "**":
                    type_used = TextType.BOLD
                case "*":
                    type_used = TextType.ITALIC
                case "`":
                    type_used = TextType.CODE
                case _:
                    raise Exception("Invalid delimiter type")

            for i, part in enumerate(new_parts):
                if len(part)==0:
                    continue
                if i%2==0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, type_used))

        else:
            new_nodes.append(old_node)
    return new_nodes

def extract_markdown_images(text):

    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    return image_pattern.findall(text)

def extract_markdown_links(text):

    link_pattern = re.compile(r'(?<!\!)\[(.*?)\]\((.*?)\)')
    return link_pattern.findall(text)


def split_nodes_image(old_nodes):

    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
        
        text = old_node.text
        text_parts = []

        for image in images:
            splitted_text = text.split(f"![{image[0]}]({image[1]})")
            if len(splitted_text[0])!=0:
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = splitted_text[1]

        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
        
        text = old_node.text
        text_parts = []

        for link in links:
            splitted_text = text.split(f"[{link[0]}]({link[1]})")
            if len(splitted_text[0])!=0:
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = splitted_text[1]
    
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes
        
