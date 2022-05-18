from cx_Freeze import setup, Executable

setup(name = "PAC-CAT" ,
      version = "1.0.0" ,
      description = "DESCRIPTION" ,
      executables = [Executable("paccat.py", base = "Win32GUI")]
)