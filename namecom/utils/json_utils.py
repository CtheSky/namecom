"""
namecom: utils/json_utils.py

Provides custom json encoder for data models.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""

import json
import functools
from ..data_models import DataModel


class DataModelEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, DataModel):
            return o.to_dict()
        return json.JSONEncoder.default(o)


json_dumps = functools.partial(json.dumps, cls=DataModelEncoder)
