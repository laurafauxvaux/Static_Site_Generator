from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    new_node = TextNode("here is some text", TextType.LINK, "https://www.boot.dev")
    print(new_node)
    new_html_node = HTMLNode("p", "abracadabra", None, {"href": "https://www.google.com","target": "_blank",})
    print(new_html_node)

main()