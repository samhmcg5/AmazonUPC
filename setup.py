from cx_Freeze import setup, Executable

# build_exe_options = {"excludes": ["tkinter", "PyQt4.sqlite3",
#                                   "QtOpenGL4", "QtSql"]}

build_exe_options = dict(excludes=["tkinter"], includes=[
                    "idna.idnadata"], optimize=1, include_files=['home.html'])


setup(name="main",
      version="0.1",
      description="",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base="Win32GUI")])
