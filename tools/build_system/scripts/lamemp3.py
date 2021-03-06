import os
import config
from base import *

class LameMP3(Base):

    def __init__(self):
        self.name = "lamemp3"
        self.version = "3.99.5"
        self.compilers = [config.COMPILER_MAC_GCC, config.COMPILER_WIN_MSVC2010, config.COMPILER_WIN_MSVC2012, config.COMPILER_UNIX_GCC]        
        self.arch = [config.ARCH_M32, config.ARCH_M64]
        self.dependencies = []
        self.info = "@todo check out if we can use the SSE2 version"

    def download(self): 
        rb_download_and_extract(self, 
                                "http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz",
                                "lame-" +self.version +".tar.gz", 
                                "lame-" +self.version)
    def build(self):
        if rb_is_unix():
            rb_build_with_autotools(self)
        elif rb_is_msvc():

            dd = rb_get_download_dir(self)
            rb_msvc_copy_custom_project(self, dd +"/" +rb_get_compiler_shortname())

            cmd = (
                "call " +rb_msvc_get_setvars(),
                "cd " +dd +"/" +rb_get_compiler_shortname(),
                "del /q .\\..\\output\\" +rb_msvc_get_build_type_string() +"\\*",
                "msbuild.exe vc9_lame.sln " +rb_msvc_get_msbuild_type_flag()  +" /t:libmp3lame "
            )

            rb_execute_shell_commands(self, cmd)
    
    def deploy(self):
        if rb_is_msvc():
            id = rb_get_download_dir(self) +"/include/"
            sd = rb_get_download_dir(self) +"/output/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(sd +"libmp3lame.dll")
            rb_deploy_lib(sd +"libmp3lame.lib")
            rb_deploy_header(id +"lame.h", "lame")
        elif rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libmp3lame.a"))
            rb_deploy_lib(rb_install_get_lib_file("libmp3lame.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libmp3lame.0.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"lame")
        elif rb_is_linux():
            rb_deploy_lib(rb_install_get_lib_file("libmp3lame.a"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"lame")


            


        
