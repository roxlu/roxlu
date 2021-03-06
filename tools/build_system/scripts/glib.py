import os
from base import *

class Glib(Base):
    
    def __init__(self):
        self.name = "glib"
        self.version = "2.36.4"
        self.compilers = [config.COMPILER_MAC_GCC, config.COMPILER_MAC_CLANG]  # , config.COMPILER_WIN_MSVC2010, config.COMPILER_WIN_MSVC2012]
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        if rb_is_unix():
            self.dependencies = ["pkgconfig", "automake", "libtool", "autoconf", "gettext"]
        else:
            self.dependencies = []
        self.info = "on mac we need to figure out why the build complaints it cannot find automake"

    def download(self):
        rb_download_and_extract(self, 
                                "http://ftp.gnome.org/pub/gnome/sources/glib/2.36/glib-" +self.version +".tar.xz",
                                "glib-" +self.version +".tar.xz", 
                                "glib-" +self.version)


    def build(self):
        if rb_is_mac():
            id = rb_install_get_dir()
            env = {"LIBFFI_LIBS":"\"-L" +id+"/lib -lffi\"",
                   "LIBFFI_CFLAGS":"\"-I" +id+"/include -I" +id+"/lib/libffi-3.0.13/include/\""}
            rb_build_with_autotools(self, environmentVars=env)
        else:
            rb_red_ln("@todo pkgconfig")

    def is_build(self):
        return rb_install_lib_exists("libglib.a")

    def deploy(self):
        if rb_is_mac():
            rb_red_ln("@todo pkgconfig ")
        else:
            rb_red_ln("@todo pkgconfig ")



                
            



