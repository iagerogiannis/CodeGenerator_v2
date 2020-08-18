import json


class MyJsonLib:

    @staticmethod
    def read_json(file):
        with open(file) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def write_data(data, file):
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def append_to_json(cls, data, file):
        file_data = cls.read_json(file)
        file_data.append(data)
        cls.write_data(file_data, file)

    @classmethod
    def locate_by_id(cls, file, id_label, id_num):
        data = cls.read_json(file)
        for entry in data:
            if entry[id_label] == id_num:
                return entry

    @classmethod
    def locate_index_by_id(cls, file, id_label, id_num):
        data = cls.read_json(file)
        i = 0
        for i in range(len(data)):
            if data[i][id_label] == id_num:
                return i
            i += 1

    @classmethod
    def drop_by_id(cls, file, id_label, id_num):
        data = cls.read_json(file)
        data[:] = [d for d in data if d.get(id_label) != int(id_num)]
        cls.write_data(data, file)

    @classmethod
    def next_index(cls, file, id_label):
        data = cls.read_json(file)
        next_id = - float("inf")
        for entry in data:
            next_id = max(next_id, entry[id_label])
        return next_id + 1

    @classmethod
    def overwrite_by_id(cls, file, id_label, id_num, new_data):
        index = cls.locate_index_by_id(file, id_label, id_num)
        file_data = cls.read_json(file)
        file_data[index] = new_data
        cls.write_data(file_data, file)
