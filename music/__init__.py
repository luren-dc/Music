from .__about__ import __author__, __author_email__, __version__
from .core import *
from .utils.http import init_session

# 初始化
init_js_context()
init_session()
