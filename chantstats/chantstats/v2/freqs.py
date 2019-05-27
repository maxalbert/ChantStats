import pandas as pd
import textwrap
from collections import Counter
from .leap import LeapL5
from .mode_degree import ModeDegree
from .pitch_class import PC


class BaseFreqsMeta(type):

    # Note: the only purpose of this metaclass is to ensure that the `BaseFreqs`
    # class has a class attribute called `zero_freqs` which can be used as the
    # "zero frequencies value" when calculating sums of frequencies using sum().

    @property
    def zero_freqs(cls):
        # initialise the class with an empty list to obtain a "zero frequencies" object
        return cls([])


class BaseFreqs(metaclass=BaseFreqsMeta):
    """
    Base class representing absolute/relative frequencies of some entity
    (for example, of pitch classes). This base class provides all the
    machinery; derived classes only need to set ALLOWED_VALUES.
    """

    ALLOWED_VALUES = []  # derived classes need to set this to a list of allowed values

    def __init__(self, list_or_freqs):
        if isinstance(list_or_freqs, pd.Series):
            freqs = list_or_freqs
            assert list(freqs.index == self.ALLOWED_VALUES)
            self.abs_freqs = freqs
        elif isinstance(list_or_freqs, list):
            if not set(list_or_freqs).issubset(self.ALLOWED_VALUES):
                raise ValueError(
                    f"Unexpected values: {set(list_or_freqs)}. Must be a subset of allowed values: {self.ALLOWED_VALUES}"
                )
            self.abs_freqs = pd.Series(Counter(list_or_freqs), index=self.ALLOWED_VALUES).fillna(0, downcast="infer")
        else:  # pragma: no cover
            raise ValueError(f"Cannot instantiate {self.__class__.__name__} from object: {list_or_freqs}")

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.abs_freqs + other.abs_freqs)

    def __repr__(self):
        freqs_indented = textwrap.indent(str(self.abs_freqs), prefix="   ")
        return f"<{self.__class__.__name__}:\n\n{freqs_indented}\n>"

    @property
    def rel_freqs(self):
        return (self.abs_freqs / self.abs_freqs.sum()) * 100


class PCFreqs(BaseFreqs):
    ALLOWED_VALUES = PC.allowed_values

    @classmethod
    def from_notes(cls, notes):
        return cls([PC.from_note(n) for n in notes])


class ModeDegreeFreqs(BaseFreqs):
    ALLOWED_VALUES = ModeDegree.allowed_values

    @classmethod
    def from_notes_and_final(cls, notes, final):
        return cls([ModeDegree.from_note_pair(note=n, base_note=final) for n in notes])


class LeapL5Freqs(BaseFreqs):
    ALLOWED_VALUES = LeapL5.allowed_values

    @classmethod
    def from_note_pairs(cls, note_pairs):
        leaps_found = []
        for note_pair in note_pairs:
            try:
                leaps_found.append(LeapL5.from_note_pair(note_pair))
            except ValueError:
                pass

        return cls(leaps_found)
