from symbol import Symbol


class Code:
    def __init__(self, symbols=[]):
        self.symbols = symbols

    def __eq__(self, other):

        if isinstance(other, Code):
            if len(other.symbols) != len(self.symbols):
                #print("Un-equal lengths")
                return False

            for index, symbol in enumerate(self.symbols):
                if symbol == other.symbols[index]:
                    a = 1
                else:
                    #print("Two symbols are not the same")
                    return False

            return True

        else:
            return False

    def to_string(self):
        for symbol in self.symbols:
            print(symbol)

    def reset(self):
        self.symbols = []

    def unsecure_equals(self, other):
        if isinstance(other, Code):
            if len(other.symbols) != len(self.symbols):
                #print("Un-equal lengths")
                return False
            else:
                self.symbols.sort()
                other.symbols.sort()
                print("***SORTED INPUT***")
                print(self)
                print("***SORTED CODE***")
                print(other)

                for index, symbol in enumerate(self.symbols):
                    if not (other.symbols[index].duration - symbol.tollerance <= symbol.duration <= other.symbols[index].duration + symbol.tollerance):
                        return False
                        
                return True

        else:
            return False

    def __str__(self):

        if len(self.symbols) == 0:
            print("EMPTY CODE")

        stg = ""
        for symbol in self.symbols:
            stg += symbol.__str__()

        return stg
