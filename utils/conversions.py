def convert_position(position:tuple[int, int], from_screen_size:tuple[int, int], to_screen_size:tuple[int, int]) -> tuple[int, int]:
    x_ratio = to_screen_size[0] / from_screen_size[0]
    y_ratio = to_screen_size[1] / from_screen_size[1]
    return (int(position[0] * x_ratio), int(position[1] * y_ratio))

def convert_size(size:tuple[int, int], from_screen_size:tuple[int, int], to_screen_size:tuple[int, int]) -> tuple[int, int]:
    return convert_position(size, from_screen_size, to_screen_size)