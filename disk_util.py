
__base_url__ = "../output-data/"


def write_array_of_arrays(array: list, file_name: str, title: str = ''):
    csv = title + '\n'
    for index in range(0, len(array[0])):
        csv += str(index)
        for list in array:
            csv += ',' + str(list[index])
        csv += '\n'

    write_file(csv, file_name)


def write_dict_of_array(dict: dict, file_name:str, title: str = ''):
    csv = title + '\n'
    for key, value in dict.items():
        csv += key
        for item in value:
            csv += ",{}".format(item)
        csv += '\n'

    write_file(csv, file_name)


def write_array(array: list, file_name: str, title: str = ''):
    csv = title + '\n'
    for item in array:
        csv += "{}\n".format(item)
    write_file(csv, file_name)


def write_dict(dict, file_name, title = 'Amplitude, Sample count'):
    csv = title + '\n'
    for k in sorted(dict):
        csv += "{},{}\n".format(k, dict[k])
    write_file(csv, file_name)


def write_file(file_data, name):
    file = open(__base_url__ + name, 'w')
    file.write(file_data)
    file.close()
