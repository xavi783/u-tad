
class Simple_mapper():

    def __init__(self, keys=[0], values=[1], sep=","):
        self.keys = keys if type(keys) is list else [keys]
        self.values = values if type(values) is list else [values]
        self.sep = sep

    def get_key(self, words):
        return self.get_member(words, self.keys)

    def get_value(self, words):
        return self.get_member(words, self.values)

    def get_member(self, words, indexes):
        try:
            return self.sep.join([str(words[i]) for i in indexes])
        except TypeError:
            return "ERROR"

    def __repr__(self):
        return "words => <words{},words{}>".format(self.keys, self.values)
