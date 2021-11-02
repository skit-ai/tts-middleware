from collections import defaultdict

import pytest
from pyquery import PyQuery as pq

from tts_middleware.elements import _get_preprocessing_attributes

nodes = list(
    map(
        lambda x: pq(x),
        [
            '<voice gender="female" name="angry"> Hello world </voice>',
            "hello world",
            '<voice name="apologetic"> Hello world </voice>',
        ],
    )
)
attributes = [
    {"gender": "female", "name": "angry"},
    {},
    {"name": "apologetic", "gender": None},
]


@pytest.mark.parametrize(
    "node, element, attribute",
    [(node, "voice", attribute) for node, attribute in zip(nodes, attributes)],
)
def test_get_voice_attributes(node, element, attribute):
    assert _get_preprocessing_attributes(node, element) == defaultdict(
        lambda: None, attribute
    )
