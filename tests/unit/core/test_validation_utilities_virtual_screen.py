from src.core.utilities.validation_utilities import get_virtual_screen_bounds


def test_get_virtual_screen_bounds_returns_valid_tuple():
    min_x, min_y, max_x, max_y = get_virtual_screen_bounds()
    assert isinstance(min_x, int)
    assert isinstance(min_y, int)
    assert isinstance(max_x, int)
    assert isinstance(max_y, int)
    assert max_x >= min_x
    assert max_y >= min_y


