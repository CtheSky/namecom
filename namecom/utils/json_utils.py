import json
import functools
from ..models import DataModel


class DataModelEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, DataModel):
            return o.to_dict()
        return json.JSONEncoder.default(o)


json_dumps = functools.partial(json.dumps, cls=DataModelEncoder)
