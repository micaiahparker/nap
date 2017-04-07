import pytest

import falcon
from pony.orm import Database, db_session
from nap import NapMixin, NapAPI

@pytest.fixture(scope='function')
def model():
    _db = Database()

    class TestModel(_db.Entity, NapMixin):
        pass

    _db.bind('sqlite', ':memory:')
    _db.generate_mapping(create_tables=True)
    return TestModel

def test_mixin_init(model):
    with db_session:
        assert model()

def test_mixin_put(model):
    assert model.http_put() == {'id': 1}
    with pytest.raises(falcon.errors.HTTPConflict):
        model.http_put(id=1)

def test_mixin_get(model):
    with pytest.raises(falcon.errors.HTTPNotFound):
        model.http_get(id=1)
    model.http_put()
    assert model.http_get(id=1) == {'id': 1}
