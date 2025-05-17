import pytest
from triangle_class import Triangle, IncorrectTriangleSides

# Позитивные тесты 
def test_equilateral_triangle():
    t = Triangle(5, 5, 5)
    assert t.triangle_type() == "equilateral"
    assert t.perimeter() == 15

def test_isosceles_triangle():
    t = Triangle(5, 5, 3)
    assert t.triangle_type() == "isosceles"
    assert t.perimeter() == 13

def test_nonequilateral_triangle():
    t = Triangle(3, 4, 5)
    assert t.triangle_type() == "nonequilateral"
    assert t.perimeter() == 12

# Негативные тесты
def test_negative_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 4, 5)

def test_zero_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 4, 5)

def test_non_numeric_sides():
    with pytest.raises(IncorrectTriangleSides):
        Triangle("a", 4, 5)

def test_violates_triangle_inequality():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 10)

def test_all_zero_sides():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 0, 0)