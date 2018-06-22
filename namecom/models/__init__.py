# -*- coding: utf-8 -*-

from .data_models import *
from .response_result_models import *

__data_models__ = [model.__name__ for model in DataModel.__subclasses__()]
