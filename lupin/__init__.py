# -*- coding: utf-8 -*-
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from .fields import *  # NOQA
from .schema import Schema  # NOQA
from .mapping import Mapping  # NOQA
from .mapper import Mapper  # NOQA