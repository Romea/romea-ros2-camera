# Copyright 2022 INRAE, French National Research Institute for Agriculture, Food and Environment
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ament_index_python.packages import get_package_share_directory

from romea_camera_description import (
    get_camera_complete_configuration,
    get_camera_geometry_file_path,
    get_camera_geometry,
    get_camera_specifications_file_path,
    get_camera_specifications,
)


def test_get_camera_specifications_file_path_ok():
    assert (
        get_camera_specifications_file_path("intel", "realsense", "d435")
        == get_package_share_directory("romea_camera_description")
        + "/config/intel_realsense_d435_specifications.yaml"
    )


def test_get_camera_specifications_ok():
    assert (
        get_camera_specifications("intel", "realsense", "d435")["rgb_camera"]["resolution"]["default"]
        == "1280x720"
    )


def test_get_camera_geometry_file_path_ok():
    assert (
        get_camera_geometry_file_path("intel", "realsense", "d435")
        == get_package_share_directory("romea_camera_description")
        + "/config/intel_realsense_d435_geometry.yaml"
    )


def test_get_camera_geometry_ok():
    assert get_camera_geometry("intel", "realsense", "d435")["mass"] == 0.075


def test_get_camera_complete_configuration_ok():
    user_description = {
        "manufacturer": "intel",
        "model": "realsense",
        "version": "d435",
        "infrared_camera": {
            "frame_rate": 30,
            "resolution": "640x480"
        },
        "rgb_camera": {
            "frame_rate": 30,
            "resolution": "320x240"
        },
        "depth_camera": {
            "frame_rate": 30,
            "resolution": "1280x720"
        }
    }

    configuration = get_camera_complete_configuration("stereo_camera", user_description)

    assert configuration["type"] == "rgbd_infrared_stereo_camera"
    assert configuration["infrared_camera"]["type"] == "stereo_camera"
    assert configuration["infrared_camera"]["frame_rate"] == 30
    assert configuration["infrared_camera"]["image_width"] == 640
    assert configuration["infrared_camera"]["image_height"] == 480
    assert configuration["infrared_camera"]["horizontal_fov"] == 69
    assert configuration["rgb_camera"]["type"] == "monocular_camera"
    assert configuration["rgb_camera"]["frame_rate"] == 30
    assert configuration["rgb_camera"]["image_width"] == 320
    assert configuration["rgb_camera"]["image_height"] == 240
    assert configuration["rgb_camera"]["horizontal_fov"] == 69
    assert configuration["depth_camera"]["type"] == "monocular_camera"
    assert configuration["depth_camera"]["frame_rate"] == 30
    assert configuration["depth_camera"]["image_width"] == 1280
    assert configuration["depth_camera"]["image_height"] == 720
    assert configuration["depth_camera"]["horizontal_fov"] == 69
