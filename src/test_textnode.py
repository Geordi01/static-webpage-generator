import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual("TextNode(This is a text node, TextType.BOLD, https://boot.dev)", repr(node))

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>This is a text node</code>")

    def test_links(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://boot.dev">This is a text node</a>')

    def test_images(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://boot.dev" alt="This is a text node"></img>')

if __name__ == "__main__":
    unittest.main()