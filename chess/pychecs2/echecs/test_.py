import unittest
from project.pychecs2.echecs import piece

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)



class Piece(unittest.TestCase):
    def test_color(self):
       pass

    def test_can_move(self):
        result = piece.Piece.can_move_towards( self,"a8", "b6")
        self.assertEqual(result, "a8", "b6")









