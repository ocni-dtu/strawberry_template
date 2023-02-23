import pytest
from mixer.backend.sqlalchemy import Mixer

from core.connection import get_local_session
from models import Item


@pytest.fixture()
def items(db):
    local_session = get_local_session()

    with local_session() as session:
        mixer = Mixer(session=session, commit=True)
        entries = mixer.cycle(3).blend(
            Item,
        )
    yield entries
