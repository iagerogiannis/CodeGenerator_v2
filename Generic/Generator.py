from random import randint, shuffle
from Generic.MyJsonLib import MyJsonLib as jsonlib


class Generator:

    keys = jsonlib.read_json("{}/{}".format("Files", "primary_keys.json"))

    @classmethod
    def assortKeys(cls, setup):

        def getKey(id):
            i = 0
            for i in range(len(cls.keys)):
                if cls.keys[i]["id"] == id:
                    return cls.keys[i]
                i += 1

        def downcase(s):
            return s[:1].lower() + s[1:] if s else ''

        selected_characters = {"Letters": {"ShiftOut": {"number": 0,
                                                        "keys": []},
                                           "ShiftIn": {"number": 0,
                                                       "keys": []},
                                           },
                               "Numbers": {"ShiftOut": {"number": 0,
                                                        "keys": []},
                                           "ShiftIn": {"number": 0,
                                                       "keys": []},
                                           },
                               "Symbols": {"ShiftOut": {"number": 0,
                                                        "keys": []},
                                           "ShiftIn": {"number": 0,
                                                       "keys": []},
                                           }
                               }

        for key_id in setup["Key_ids"]:
            key = getKey(key_id)
            for shift in ["ShiftOut", "ShiftIn"]:
                selected_characters["{}s".format(key["type"])][shift]["keys"].append(key[downcase(shift)])

        for type in ["Letters", "Numbers", "Symbols"]:
            for shift in ["ShiftOut", "ShiftIn"]:
                selected_characters[type][shift]["number"] = setup[type][shift]

        return selected_characters

    @classmethod
    def selectCharacters(cls, setup):

        characters = cls.assortKeys(setup)

        code = []

        for type in ["Letters", "Numbers", "Symbols"]:
            for shift in ["ShiftOut", "ShiftIn"]:
                for i in range(characters[type][shift]["number"]):
                    amount = len(characters[type][shift]["keys"])
                    code.append(characters[type][shift]["keys"][randint(0, amount - 1)])

        return "".join(code)

    @classmethod
    def rearange(cls, code, times=5):
        temp = list(code)
        for i in range(5):
            shuffle(temp)
        return "".join(temp)

    @classmethod
    def produce_code(cls, setup):
        return cls.rearange(cls.selectCharacters(setup))
