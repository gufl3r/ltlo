def point_inside_area(point_position: tuple[int, int], area: tuple[tuple, tuple]) -> bool:
    px, py = point_position[0], point_position[1]
    (x, y), (w, h) = (area[0][0], area[0][1]), area[1]

    return (
        x <= px <= x + w and
        y <= py <= y + h
    )