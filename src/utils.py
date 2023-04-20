def convert_list_to_dictionary_by_field(list: list, field: str):
    new_dict = {}
    for item in list:
        name = item.get(field)
        new_dict[name] = item #todo: dict.update
    return new_dict
