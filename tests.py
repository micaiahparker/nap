import pytest

import falcon
from pony.orm import Database, db_session
from nap import NapMixin, NapAPI

@pytest.fixture
def test_model():
    _db = Database()

    class TestModel(_db.Entity, NapMixin):
        pass

    _db.bind('sqlite', ':memory:')
    _db.generate_mapping(create_tables=True)
    return TestModel

def test_mixin_init(test_model):
    with db_session:
        assert test_model()

def test_mixin_put(test_model):
    assert test_model.http_put() == {'id': 1}
    with pytest.raises(falcon.errors.HTTPConflict):
        test_model.http_put(id=1)

def test_mixin_get(test_model):
    with pytest.raises(falcon.errors.HTTPNotFound):
        test_model.http_get(id=1)
    test_model.http_put()
    assert test_model.http_get(id=1) == {'id': 1}
