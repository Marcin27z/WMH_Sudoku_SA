from enum import Enum

## Klasa enumeracyjna reprezentująca możliwe tryby uruchomienia
#
#
class Mode(Enum):
    RANDOM = 0,
    NOT_RANDOM = 1

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    ## Funkcja pomocnicza używana przy wczytywaniu argumentów z lini poleceń
    #
    #
    @staticmethod
    def argparse(s):
        try:
            return Mode[s.upper()]
        except KeyError:
            return s

