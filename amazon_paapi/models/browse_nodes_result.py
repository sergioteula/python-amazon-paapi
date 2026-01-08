"""Browse node result models for Amazon Product Advertising API."""

from __future__ import annotations

from amazon_paapi.sdk import models as sdk_models


class BrowseNodeChild(sdk_models.BrowseNodeChild):
    """Represent a child browse node."""

    context_free_name: str
    display_name: str
    id: str


class BrowseNodeAncestor(BrowseNodeChild, sdk_models.BrowseNodeAncestor):
    """Represent an ancestor browse node."""

    ancestor: BrowseNodeChild


class BrowseNode(sdk_models.BrowseNode):
    """Represent a browse node with its hierarchy information."""

    display_name: str
    id: str
    is_root: bool
    context_free_name: str
    children: list[BrowseNodeChild]
    ancestor: BrowseNodeAncestor
