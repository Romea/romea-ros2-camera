cmake_minimum_required(VERSION 3.5)
project(romea_camera_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config urdf launch
  DESTINATION share/${PROJECT_NAME}
)

ament_python_install_module(python/romea_camera_description.py)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_flake8_CONFIG_FILE "${CMAKE_SOURCE_DIR}/.flake8")
  list(APPEND AMENT_LINT_AUTO_EXCLUDE ament_cmake_copyright)
  
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_monocular_camera_urdf_gazebo_classic test/test_monocular_camera_urdf_gazebo_classic.py)
  ament_add_pytest_test(test_stereo_camera_urdf_gazebo_classic test/test_stereo_camera_urdf_gazebo_classic.py)
  ament_add_pytest_test(test_rgbd_stereo_camera_urdf_gazebo_classic test/test_rgbd_stereo_camera_urdf_gazebo_classic.py)
  ament_add_pytest_test(test_rgbd_infrared_stereo_camera_urdf_gazebo_classic test/test_rgbd_infrared_stereo_camera_urdf_gazebo_classic.py)
  ament_add_pytest_test(test_stereolabs_zed1_description test/test_stereolabs_zed1_description.py)
  ament_add_pytest_test(test_stereolabs_zed2_description test/test_stereolabs_zed2_description.py)
  ament_add_pytest_test(test_realsense_d435_description test/test_realsense_d435_description.py)

endif()

ament_package()


