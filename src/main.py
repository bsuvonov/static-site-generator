from src.textnode import *
from src.htmlnode import *
from src.code import *



def main():


    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    for node in new_nodes:
        print(node)
    return 0

if __name__ == "__main__":
    main()