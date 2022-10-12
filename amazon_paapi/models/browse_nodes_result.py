from typing import List

from ..sdk import models as sdk_models


class BrowseNodeChild(sdk_models.BrowseNodeChild):
    context_free_name: str
    display_name: str
    id: str


class BrowseNodeAncestor(BrowseNodeChild, sdk_models.BrowseNodeAncestor):
    ancestor: BrowseNodeChild


class BrowseNode(sdk_models.BrowseNode):
    display_name: str
    id: str
    is_root: bool
    context_free_name: str
    children: List[BrowseNodeChild]
    ancestor: BrowseNodeAncestor
