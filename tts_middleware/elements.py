from collections import defaultdict

from pyquery.pyquery import PyQuery

_supported_element_attributes = {"voice": {"gender", "name"}}


def _get_preprocessing_attributes(node: PyQuery, element: str):
    attributes = defaultdict(lambda: None)
    if not node(element):
        return attributes
    for attribute in _supported_element_attributes[element]:
        attributes[attribute] = getattr(node(element).attr, attribute)
    return attributes
