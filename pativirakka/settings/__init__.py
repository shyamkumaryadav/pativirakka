import os


if os.getenv("shyamkumaryadav"):
    from .production import *
else:
    from .development import *
