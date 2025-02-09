import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div", 
            "Hello world!", 
            None, 
            {"class": "primary"},
        )
        self.assertEqual(
            node.props_to_html(), 
            ' class="primary"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_values_none(self):
        node = LeafNode("img", None, {"src": "https://boot.dev"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tags_none(self):
        node = LeafNode(None, "Hello world", {"src": "https://boot.dev"})
        self.assertEqual(
            node.to_html(),
            "Hello world",
        )

    def test_to_html(self):
        node = LeafNode("p", "Hello world", {"class": "primary"})
        self.assertEqual(
            node.to_html(),
            '<p class="primary">Hello world</p>',
        )

class TestParentNode(unittest.TestCase):
    def test_tag_none(self):
        node = ParentNode(None, [LeafNode("p", "Hello world")], {"class": "primary"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_children_none(self):
        node = ParentNode("div", None, {"class": "primary"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html(self):
        node = ParentNode("div", [LeafNode("p", "Hello world")], {"class": "primary"})
        self.assertEqual(
            node.to_html(),
            '<div class="primary"><p>Hello world</p></div>',
        )
            

if __name__ == "__main__":
    unittest.main()