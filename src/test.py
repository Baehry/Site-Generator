import unittest
from nodes import TextNode, HTMLNode, LeafNode, ParentNode
from enums import TextType, BlockType
from main import *
from functions import *


class Test(unittest.TestCase):
        def test_block_to_block_type(self):
            self.assertEqual(block_to_block_type("```Hello```"), BlockType.CODE)

        
    

if __name__ == "__main__":
    unittest.main()