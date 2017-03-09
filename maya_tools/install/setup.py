from distutils.core import setup
import py2exe,sys,os

includes = [
	"encodings",
	"encodings.utf_8"
]

options = {
}


setup(
	options = {"py2exe":options},
	console = [{"script":"pingomenuInstall.py"}],
	zipfile = None,
)