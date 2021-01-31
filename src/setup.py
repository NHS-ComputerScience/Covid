# setup.py
from distutils.core import setup
import glob
import py2exe

setup(console=["Main.py"],
      data_files=[glob.glob("src\\*.py"),
                  glob.glob("stk\\*.txt")],
)


#setup(console=["Main.py"],
#      data_files=[("bitmaps",
#                   ["bm/large.gif", "bm/small.gif"]),
#                  ("fonts",
#                   glob.glob("fonts\\*.fnt"))],
#)