import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestTriangleType(unittest.TestCase):

    # Позитивные тесты
    def test_equilateral_triangle(self):
        self.assertEqual(get_triangle_type(3, 3, 3), "equilateral")

    def test_isosceles_triangle(self):
        self.assertEqual(get_triangle_type(4, 4, 5), "isosceles")

    def test_nonequilateral_triangle(self):
        self.assertEqual(get_triangle_type(5, 4, 6), "nonequilateral")

    def test_equilateral_with_floats(self):
        self.assertEqual(get_triangle_type(0.5, 0.5, 0.5), "equilateral")

    def test_isosceles_with_floats(self):
        self.assertEqual(get_triangle_type(2, 2, 3.5), "isosceles")

    # Негативные тесты
    def test_zero_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 3, 3)

    def test_negative_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 2)

    def test_invalid_triangle_sum_equal(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)

    def test_invalid_triangle_sum_less(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 4)

    def test_string_input(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type("3", 3, 3)

    def test_none_input(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(None, 3, 3)

    def test_infinite_value(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(float('inf'), 3, 3)

if __name__ == "__main__":
    unittest.main()