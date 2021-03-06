import wx
import sys
import platform

APP = "main.py"
NAME = "Compressy2"
VERSION = "0.1.0"
AUTHOR = "Matthew Bozelka"
AUTHOR_EMAIL = "mattbozelka.dev@gmail.com"
URL = "https://github.com/mbozelka/compressy2"
LICENSE = "MIT"
YEAR = "2017"


def BuildPy2Exe():
    from distutils.core import setup
    try:
        import py2exe
    except ImportError:
        print("\n!! You dont have py2exe installed. !!\n")
        exit()
    
    archDat = platform.architecture()
    is32 = "32bit" in archDat
    bundle = 2 if is32 else 3
    OPTS = {"py2exe" : {"compressed" : 1,
            "optimize" : 1,
            "bundle_files" : bundle,
            "packages": ["PIL"],
            "excludes" : ["Tkinter",],
            "dll_excludes": ["MSVCP90.dll"]}}

    setup(name = NAME,
          version = VERSION,
          options = OPTS,
          windows = [{"script": APP,
                      "icon_resources": [(1, "Icon.ico")],
          }],
          description = NAME,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          license = LICENSE,
          url = URL,
          )


def BuildOSXApp():
    """Build the OSX Applet"""
    from setuptools import setup

    copyright = "Copyright %s %s" % (AUTHOR, YEAR)
    appid = "com.%s.%s" % (NAME, NAME)
    PLIST = dict(CFBundleName = NAME,
                 CFBundleIconFile = 'Icon.icns',
                 CFBundleShortVersionString = VERSION,
                 CFBundleGetInfoString = NAME + " " + VERSION,
                 CFBundleExecutable = NAME,
                 CFBundleIdentifier = appid,
                 CFBundleTypeMIMETypes = ['text/plain',],
                 CFBundleDevelopmentRegion = 'English',
                 NSHumanReadableCopyright = copyright
    )

    PY2APP_OPTS = dict(iconfile = "Icon.icns",
                       argv_emulation = True,
                       optimize = True,
                       packages = ['PIL'],
                       plist = PLIST)
    setup(app = [APP,],
          version = VERSION,
          options = dict( py2app = PY2APP_OPTS),
          description = NAME,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          license = LICENSE,
          url = URL,
          setup_requires = ['py2app'],
    )


if __name__ == '__main__':
    if wx.Platform == '__WXMSW__':
        # Windows
        BuildPy2Exe()
    elif wx.Platform == '__WXMAC__':
        # OSX
        BuildOSXApp()
    else:
        print("Unsupported platform: %s" % wx.Platform)