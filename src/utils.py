def to_dictionary(list: list, field: str):
    new_dict = {}
    for item in list:
        name = item.get(field)
        new_dict[name] = item
    return new_dict
