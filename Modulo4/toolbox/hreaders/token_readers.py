
class Token_reader():

    def __init__(self, sep=",", nsplits=-1):
        self.sep = sep
        self.nsplits = nsplits

    def read_all(self, line):
        return line.strip().split(self.sep, self.nsplits)