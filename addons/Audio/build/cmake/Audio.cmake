
roxlu_addon_begin("audio")
  # --------------------------------------------------------------------------------------
  roxlu_addon_add_source_file(audio/Audio.cpp)
  roxlu_addon_add_source_file(audio/AudioFile.cpp)
  roxlu_addon_add_source_file(audio/AudioOutput.cpp)
  roxlu_addon_add_source_file(audio/AudioStream.cpp)
  roxlu_addon_add_source_file(audio/PCMWriter.cpp)
  roxlu_addon_add_source_file(audio/MP3Writer.cpp)
  
  if(WIN32)
    roxlu_add_extern_library(portaudio_x86.lib)
    roxlu_add_extern_library(libsndfile-1.lib)
    roxlu_add_extern_library(libmp3lame.lib)
    roxlu_add_dll(portaudio_x86.dll)
    roxlu_add_dll(libsndfile-1.dll)
    roxlu_add_dll(libmp3lame.dll)
  endif()

  if(UNIX)
    roxlu_add_extern_library(libportaudio.a)
    roxlu_add_extern_library(libsndfile.a)
    roxlu_add_extern_library(libiconv.a)  
    roxlu_add_extern_library(libmp3lame.a)
    roxlu_add_extern_library(libuv.a)
  endif()

  if(UNIX AND NOT APPLE)
    roxlu_add_lib(asound) 
  endif()

  if(APPLE)
    find_library(fr_audio CoreAudio)
    find_library(fr_audio_unit AudioUnit)
    find_library(fr_audio_toolbox AudioToolbox)
    find_library(fr_core_services CoreServices)

    roxlu_add_library(${fr_audio})
    roxlu_add_library(${fr_audio_unit})
    roxlu_add_library(${fr_audio_toolbox})
    roxlu_add_library(${fr_core_services})

  endif(APPLE)
  # --------------------------------------------------------------------------------------
roxlu_addon_end()

