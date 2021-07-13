from typing import List
from ..sdk import models


class BrowseNodeChild(models.BrowseNodeChild):
    context_free_name: str
    display_name: str
    id: str


class BrowseNodeAncestor(BrowseNodeChild, models.BrowseNodeAncestor):
    ancestor: BrowseNodeChild


class BrowseNode(models.BrowseNode):
    display_name: str
    id: str
    is_root: bool
    context_free_name: str
    children: List[BrowseNodeChild]
    ancestor: BrowseNodeAncestor
