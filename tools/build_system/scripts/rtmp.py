"""
on mac you probably want to change the rpath to use rtmpdump:
install_name_tool -change /usr/local/lib/librtmp.0.dylib @executable_path/librtmp/librtmp.dylib rtmpdump
"""
import os
import config
from base import *

class Rtmp(Base):

    def __init__(self):
        self.name = "rtmp"
        self.version = ""
        self.compilers = [config.COMPILER_MAC_GCC, config.COMPILER_UNIX_GCC] #, config.COMPILER_WIN_MSVC2010, config.COMPILER_WIN_MSVC2012]        
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        self.dependencies = ["zlib", "openssl"]

    def download(self): 
        rb_git_clone(self, "git://git.ffmpeg.org/rtmpdump")

    def build(self):
        dd = rb_get_download_dir(self)

        if rb_is_unix():
            env = rb_get_autotools_environment_vars()
            ef = (
                "set -x",
                "cd " +dd,
                rb_get_export_cmd("XCFLAGS", rb_get_cflags()),
                rb_get_export_cmd("XLDFLAGS", rb_get_ldflags()),
                "make clean",
                "make SYS=darwin"
                )
            rb_execute_shell_commands(self, ef, env)

        elif rb_is_win():
            rb_copy_to_download_dir(self, "CMakeLists.txt")
            rb_cmake_configure(self)
            rb_cmake_build(self)

        return True

    def is_build(self):
        if rb_is_unix():
            return rb_deploy_lib_file_exists("librtmp.a")
        elif rb_is_win:
            return rb_deploy_lib_file_exists("librtmp.lib")
        return False
    
    def deploy(self):

        if rb_is_unix():
            rb_deploy_lib(rb_download_get_file(self, "librtmp/librtmp.a"))
            rb_deploy_headers(dir = rb_get_download_dir(self) +"librtmp/*.h", subdir = "librtmp")
        elif rb_is_win():
            rb_deploy_headers(dir = rb_install_get_include_dir() +"librtmp/*.h", subdir = "librtmp")
            rb_deploy_lib(rb_install_get_lib_file("librtmp.lib"))
        return True
                
        
