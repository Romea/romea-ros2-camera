cmake_minimum_required(VERSION 3.5)
project(romea_camera_bringup)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_python_install_module(python/romea_camera_bringup.py)

install(PROGRAMS
  scripts/urdf_description.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  configure_file(test/test_camera_bringup.yaml test_camera_bringup.yaml)
  ament_add_pytest_test(test_camera_bringup test/test_camera_bringup.py)
  ament_add_pytest_test(test_urdf_description test/test_urdf_description.py)
endif()

ament_package()
