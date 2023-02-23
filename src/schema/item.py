import strawberry
from sqlmodel import select
from strawberry.types import Info

from core.context import get_session
from graphql_types.item import GraphQLItem
from models import Item


def items_query(info: Info) -> list[GraphQLItem]:
    """Returns all Items"""

    session = get_session(info)
    query = select(Item)
    items = session.exec(query).all()

    return items


def add_item_mutation(info: Info, name: str) -> GraphQLItem:
    """Creates a new Item"""

    session = get_session(info)

    item = Item(name=name)
    session.add(item)
    session.commit()

    session.refresh(item)

    return item
