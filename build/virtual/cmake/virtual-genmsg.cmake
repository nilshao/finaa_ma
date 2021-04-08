# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "virtual: 1 messages, 0 services")

set(MSG_I_FLAGS "-Ivirtual:/home/sibohao/Desktop/catkin_ws/src/virtual/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(virtual_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_custom_target(_virtual_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "virtual" "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(virtual
  "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/virtual
)

### Generating Services

### Generating Module File
_generate_module_cpp(virtual
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/virtual
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(virtual_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(virtual_generate_messages virtual_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_dependencies(virtual_generate_messages_cpp _virtual_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(virtual_gencpp)
add_dependencies(virtual_gencpp virtual_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS virtual_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(virtual
  "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/virtual
)

### Generating Services

### Generating Module File
_generate_module_eus(virtual
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/virtual
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(virtual_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(virtual_generate_messages virtual_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_dependencies(virtual_generate_messages_eus _virtual_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(virtual_geneus)
add_dependencies(virtual_geneus virtual_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS virtual_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(virtual
  "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/virtual
)

### Generating Services

### Generating Module File
_generate_module_lisp(virtual
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/virtual
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(virtual_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(virtual_generate_messages virtual_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_dependencies(virtual_generate_messages_lisp _virtual_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(virtual_genlisp)
add_dependencies(virtual_genlisp virtual_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS virtual_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(virtual
  "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/virtual
)

### Generating Services

### Generating Module File
_generate_module_nodejs(virtual
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/virtual
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(virtual_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(virtual_generate_messages virtual_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_dependencies(virtual_generate_messages_nodejs _virtual_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(virtual_gennodejs)
add_dependencies(virtual_gennodejs virtual_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS virtual_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(virtual
  "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/virtual
)

### Generating Services

### Generating Module File
_generate_module_py(virtual
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/virtual
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(virtual_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(virtual_generate_messages virtual_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sibohao/Desktop/catkin_ws/src/virtual/msg/CaliInfo.msg" NAME_WE)
add_dependencies(virtual_generate_messages_py _virtual_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(virtual_genpy)
add_dependencies(virtual_genpy virtual_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS virtual_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/virtual)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/virtual
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/virtual)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/virtual
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/virtual)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/virtual
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/virtual)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/virtual
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/virtual)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/virtual\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/virtual
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
