import logging
import sys
import unittest

from ztag.stream import Stream, Outgoing
from ztag.transform import Transform, CompoundOutput

logging.basicConfig(stream=sys.stderr)

logger = logging.getLogger(__file__)
logger.trace = logger.debug
logger.setLevel(5)


# Just wrap a string in a dict
def wrap(val):
    return {
        "content": val
    }


# An 'outgoing' implementation that just drops anything it take()s into contents.
class Accumulator(Outgoing):
    def __init__(self):
        self.contents = []

    def take(self, obj):
        self.contents.append(obj)

    def __iter__(self):
        return self.contents.__iter__()

    def __len__(self):
        return len(self.contents)


# If "split" is in obj, return 3 copies of it prefixed with l/c/r.
# If "drop" is on obj, return nothing.
# Otherwise, just return obj.
def conditional_split(obj):
    if "split" in obj.lower():
        return CompoundOutput("l-" + obj, "c-" + obj, "r-" + obj)
    if "drop" in obj.lower():
        return
    return obj


# Return a CompoundOutput with two copies of obj, prefixed with left/right.
def unconditional_split(obj):
    return CompoundOutput(wrap("l-" + obj["content"]), wrap("r-" + obj["content"]))


# If "ignore" is in obj, return None. Otherwise just return obj.
def ignorer(obj):
    if "ignore" in obj["content"].lower():
        return None
    return obj


# A Transform implementation that invokes a single simple function.
class SimpleTransform(Transform):
    def __init__(self, func):
        self.func = func

    def _transform_object(self, obj):
        return self.func(obj)


class StreamTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_stream(self):
        """
        Check that compound results from transform() are properly handled, and that take() is
        eventually called with the correct values.
        """
        incoming = ["a", "dropme", "b", "split", "d", "e", "ignoreme", "f"]
        transforms = [
            conditional_split,
            lambda x: x.upper(),
            wrap,
            unconditional_split,
            ignorer,
        ]
        outgoing = Accumulator()
        s = Stream(incoming, outgoing, transforms=[SimpleTransform(x) for x in transforms])
        handled, skipped = s.run()
        self.assertEqual(2, skipped)
        self.assertEqual(len(outgoing), handled)
        expected = [
            # a -> a -> A -> wrap(A) -> l-A, r-A -> l-A, r-A
            "l-A", "r-A",
            # dropme -> None -> IgnoreObject
            # b -> b -> B -> wrap(B) -> l-B, r-B -> l-B, r-B
            "l-B", "r-B",
            # split -> l-split, c-split, r-split -> L-SPLIT, C-SPLIT, R-SPLIT -> wrap(...) -> ...
            #   ... -> l-L-SPLIT, r-L-SPLIT, l-C-SPLIT, r-C-SPLIT, l-R-SPLIT, r-R-SPLIT
            "l-L-SPLIT", "r-L-SPLIT", "l-C-SPLIT", "r-C-SPLIT", "l-R-SPLIT", "r-R-SPLIT",
            "l-D", "r-D",
            "l-E", "r-E",
            # ignoreme -> ignoreme -> IGNOREME -> wrap(IGNOREME)
            #          -> l-IGNOREME, r-IGNOREME -> None -> IgnoreObject
            "l-F", "r-F",
        ]
        actual = [v["content"] for v in outgoing]
        self.assertListEqual(expected, actual)
