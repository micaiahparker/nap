from pony.orm import db_session, OrmError
import falcon

class NapMixin:
    @classmethod
    @db_session
    def _http_get(cls, **kwargs):
        item = cls.get(**kwargs)
        if item:
            return item.to_dict()
        raise falcon.errors.HTTPNotFound

    @classmethod
    @db_session
    def _http_put(cls, **kwargs):
        try:
            item = cls(**kwargs)
            return item.to_dict()
        except OrmError:
            raise falcon.errors.HTTPConflict(
                title='Duplicate Resource',
                description='Resource already exists.'
            )

    @classmethod
    def http_get(cls, **kwargs):
        return cls._http_get(**kwargs)

    @classmethod
    def http_put(cls, **kwargs):
        return cls._http_put(**kwargs)
