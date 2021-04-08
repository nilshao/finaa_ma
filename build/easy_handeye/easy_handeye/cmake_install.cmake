# Install script for directory: /home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/sibohao/Desktop/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/easy_handeye.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/easy_handeye/cmake" TYPE FILE FILES
    "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/easy_handeyeConfig.cmake"
    "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/easy_handeyeConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/easy_handeye" TYPE FILE FILES "/home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/easy_handeye" TYPE PROGRAM FILES "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/calibrate.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/easy_handeye" TYPE PROGRAM FILES "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/robot.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/easy_handeye" TYPE PROGRAM FILES "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/handeye_calibration_commander.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/easy_handeye" TYPE PROGRAM FILES "/home/sibohao/Desktop/catkin_ws/build/easy_handeye/easy_handeye/catkin_generated/installspace/publish.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/easy_handeye/launch" TYPE FILE FILES
    "/home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye/launch/calibrate.launch"
    "/home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye/launch/publish.launch"
    "/home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye/launch/rqt_easy_handeye.perspective"
    "/home/sibohao/Desktop/catkin_ws/src/easy_handeye/easy_handeye/launch/rviz_easy_handeye.config"
    )
endif()

