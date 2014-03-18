import os
import config
from base import *

class Cubeb(Base):
    def __init__(self):
        self.name = "cubeb"
        self.version = ""
        self.compilers = [config.COMPILER_MAC_GCC]
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        self.dependencies = []
        self.info = "only compiled on mac - cross platform audio output"

    def download(self): 
        rb_git_clone(self, "https://github.com/kinetiknz/cubeb")
        if rb_is_mac():
            cmd = (
                "cd " +rb_get_download_dir(self) +"/",
                "autoreconf --install"
            )
            rb_execute_shell_commands(self, cmd, rb_get_autotools_environment_vars())
        return True

    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self);
        return False

    def is_build(self):
        if rb_is_mac():
            return rb_install_lib_file_exists("libcubeb.a")
        return False

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libcubeb.a"))
        rb_deploy_header(rb_install_get_include_file("sndfile.h"))
        rb_deploy_headers(dir = rb_install_get_dir() +"include/cubeb/", subdir = "cubeb")

        return True
        