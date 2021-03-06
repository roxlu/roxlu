import os
import config
from base import *

class Freenect(Base):
    
    def __init__(self):
        self.name = "freenect"
        self.version = "c55f3c94c422afc9f4c3c34327da9526b44f32a2"
        self.compilers = [config.COMPILER_MAC_GCC, config.COMPILER_MAC_CLANG]
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        self.dependencies = ["libusb"]
        self.info = "NOT FINISHED YET"

    def download(self):
        rb_git_clone(self, "git://github.com/OpenKinect/libfreenect.git")

    def build(self):
        opts = [ 
            "-DBUILD_OPENNI2_DRIVER=ON",
            "-DLIBUSB_1_INCLUDE_DIRS=" +rb_install_get_include_dir()
        ]
        rb_cmake_configure(self, opts)
        rb_cmake_build(self)
        return True

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libfreenect.a")
        else:
            rb_red_ln("@todo freenect check if file exists on windows")
        return True

        return True

    def deploy(self):
        if rb_is_unix():
            if not rb_is_mac():
                if rb_is_64bit():
                    rb_deploy_lib(rb_install_get_dir() +"lib64/libfreenect.a")
                else:
                    rb_red_ln("@todo freenect mac 32bit")
            else:
                rb_deploy_lib(rb_install_get_lib_file("libfreenect.a"))
            rb_deploy_headers(dir = rb_install_get_dir() +"include/libfreenect/", subdir = "libfreenect")
            rb_deploy_header(rb_install_get_include_file("libfreenect.hpp"))
        return True



                
            



