def check_and_extract_coordinate(coordinate, coordinate_type):
    borders = {'lat': 90, 'lon': 180}
    try:
        coordinate = float(coordinate)
        if -borders[coordinate_type] <= coordinate <= borders[coordinate_type]:
            return coordinate
    except (ValueError, TypeError):
        pass


def clean_city_name(city_name):
    return city_name.strip().lower()
