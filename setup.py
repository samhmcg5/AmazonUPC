from cx_Freeze import setup, Executable
import sys

build_exe_options = dict(excludes=["tkinter", "PyQt4.sqlite3","QtOpenGL4", "QtSql"],
                        includes=["idna.idnadata"], 
                        optimize=2, 
                        include_files=[])


base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="UpcProductLoader",
      version="",
      description="",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
