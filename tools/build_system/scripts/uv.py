import os
import config
from base import *

class UV(Base):

    def __init__(self):
        self.name = "uv"
        #self.version = "d7a1ba85f204183244721d838a70286cb5cfddeb" 
        #self.version = "acb9f8951eaeacaed1f0dfeaed67cb8bda7cd5b1"
        self.version = "git"
        self.compilers = [config.COMPILER_WIN_MSVC2010, config.COMPILER_WIN_MSVC2012, config.COMPILER_MAC_GCC, config.COMPILER_MAC_CLANG, config.COMPILER_UNIX_GCC]        
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_git_clone(self, "https://github.com/joyent/libuv.git")
        #, self.version)

    def build(self):
        if rb_is_mac():

            arch = "ia32" if rb_is_32bit() else "x64"

            output_dir = rb_get_triplet() +"_" +rb_msvc_get_build_type_string()

            dd = rb_get_download_dir(self)

            # static lib
            cmd = (
                "set -x",
                "cd " +dd,
                "mkdir out",
                "if [ ! -d build/gyp ] ; then  git clone https://git.chromium.org/external/gyp.git build/gyp ; fi",
                "./gyp_uv.py -Dtarget_arch=" +arch +" -Dhost_arch=" +arch,
                "make -C out BUILDTYPE=" +rb_msvc_get_build_type_string() +rb_get_make_compiler_flags(),
                "mv out " +output_dir
                )

            rb_execute_shell_commands(self, cmd)

            return True

            # shared lib
            output_dir = output_dir +"_Shared"
            cmd = (
                "cd " +dd,
                "if [ ! -d build/gyp ] ; then  git clone https://git.chromium.org/external/gyp.git build/gyp ; fi",
                "./gyp_uv.py -Dtarget_arch=" +arch +" -Dlibrary=shared_library -Dcomponent=shared_library ",
                "make -C out BUILDTYPE=" +rb_msvc_get_build_type_string() +rb_get_make_compiler_flags(),
                "mv out " +output_dir
                )

            rb_execute_shell_commands(self, cmd)

        elif rb_is_msvc():
            rb_copy_to_download_dir(self, "CMakeLists.txt")
            rb_cmake_configure(self)
            rb_cmake_build(self)

        elif rb_is_unix():
            cmd = (
                "cd " +rb_get_download_dir(self),
                "./autogen.sh",
                )
            rb_execute_shell_commands(self, cmd)
            rb_build_with_autotools(self)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libuv.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libuv.dll") # test this!
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    # on mac the build file destination can be either in "Release/out", "out" or just "Release"
    # this finds the correct one :) 
    def get_build_file(self, filename):
        dd = rb_get_download_dir(self)
        output_dir = rb_get_download_dir(self) +rb_get_triplet() +"_" +rb_msvc_get_build_type_string()
        output_dir_a = output_dir +"/" +rb_msvc_get_build_type_string() +"/"
        output_dir_b = output_dir +"/out/" +rb_msvc_get_build_type_string() +"/";
        output_dir_c = output_dir +"_Shared/" +rb_msvc_get_build_type_string() +"/"
        output_dir_d = output_dir +"_Shared/out/" +rb_msvc_get_build_type_string() +"/"
        file_a = output_dir_a +filename
        file_b = output_dir_b +filename
        file_c = output_dir_c +filename
        file_d = output_dir_d +filename
        if os.path.exists(file_a):
            return file_a
        elif os.path.exists(file_b):
            return file_b
        elif os.path.exists(file_c):
            return file_c
        elif os.path.exists(file_d):
            return file_d
        else:
            rb_yellow_ln("Cannot find file: " +filename +" in either: " +file_a +" or " +file_b)
            return False
            
    def deploy_lib_if_exists(self, filename):
        fn = self.get_build_file(filename)
        if fn:
            rb_deploy_lib(fn)
    
    def deploy(self):
        if rb_is_msvc():
            rb_deploy_lib(rb_install_get_lib_file("libuv.lib"))
            rb_deploy_dll(rb_install_get_bin_file("libuv.dll"))
            rb_deploy_header(rb_install_get_include_file("uv.h"))
            rb_deploy_header(rb_install_get_include_file("uv-errno.h"))
            rb_deploy_header(rb_install_get_include_file("uv-win.h"))
            rb_deploy_header(rb_install_get_include_file("stdint-msvc2008.h"))
        elif rb_is_mac():
            self.deploy_lib_if_exists("libuv.a")
            rb_deploy_header(rb_download_get_file(self, "include/pthread-fixes.h"))
            rb_deploy_header(rb_download_get_file(self, "include/stdint-msvc2008.h"))
            rb_deploy_header(rb_download_get_file(self, "include/tree.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-bsd.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-darwin.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-version.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-errno.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-linux.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-sunos.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-unix.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-win.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv.h"))
        elif rb_is_linux():
            rb_deploy_header(rb_install_get_include_file("uv-errno.h"))
            rb_deploy_header(rb_install_get_include_file("uv-linux.h"))
            rb_deploy_header(rb_install_get_include_file("uv-unix.h"))
            rb_deploy_header(rb_install_get_include_file("uv.h"))
            rb_deploy_lib(rb_install_get_lib_file("libuv.a"))

        else:
            rb_red_ln("Deploy uv not implemented")
            


        
