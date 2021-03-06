import os
import config
from base import *

class Cairo(Base):
    
    def __init__(self):
        self.name = "cairo"
        self.version = "ac5f3e2b8ef1937b3e6e3a3f03773cf471e46cc3"
        self.compilers = [config.COMPILER_MAC_GCC, config.COMPILER_MAC_CLANG]
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        if rb_is_unix():
            self.dependencies = ["automake", "autoconf", "libtool", "pixman", "freetype"]
        else:
            self.dependencies = []

    def download(self):
        rb_git_clone(self, "git://anongit.freedesktop.org/git/cairo", self.version)

    def build(self):
        cmd = [
            "cd " +rb_get_download_dir(self),
            "./autogen.sh"
            ]

        env = rb_get_autotools_environment_vars()
        env["POPPLER_CFLAGS"] = "-I" +rb_install_get_include_dir()
        env["POPPLER_LIBS"] = "-lpoppler"  
        #env = { "POPPLER_CFLAGS":"-I" +rb_install_get_include_dir(), "POPPLER_LIBS" :"-lpoppler" } 
        rb_execute_shell_commands(self, cmd, env)
        
        
        rb_build_with_autotools(self, environmentVars = env)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libcairo.a")
        else:
            rb_red_ln("@todo cairo")

    def deploy(self):
        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libcairo.a"))
            rb_deploy_lib(rb_install_get_lib_file("libcairo.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libcairo.2.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"cairo", subdir = "cairo")
        else:
            rb_yellow_ln("@todo cairo")



                
            



