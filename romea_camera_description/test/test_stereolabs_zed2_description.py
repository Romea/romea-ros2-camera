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

import pytest

from romea_camera_description import (
    get_complete_configuration,
    get_geometry,
    get_geometry_file_path,
    get_specifications,
    get_specifications_file_path,
)


@pytest.fixture(scope="module")
def user_description():

    return {
        "manufacturer": "stereolabs",
        "model": "zed",
        "version": "2",
        "frame_rate": 30
    }


def test_get_specifications_file_path_ok(user_description):
    assert (
        get_specifications_file_path(user_description)
        == get_package_share_directory("romea_camera_description")
        + "/config/stereolabs_zed_2_specifications.yaml"
    )


def test_get_specifications_ok(user_description):
    assert get_specifications(user_description)["resolution"]["default"] == "1280x720"


def test_get_geometry_file_path_ok(user_description):
    assert (
        get_geometry_file_path(user_description)
        == get_package_share_directory("romea_camera_description")
        + "/config/stereolabs_zed_2_geometry.yaml"
    )


def test_get_geometry_ok(user_description):
    assert get_geometry(user_description)["mass"] == 0.124


def test_get_complete_configuration_ok(user_description):

    configuration = get_complete_configuration("stereo_camera", user_description, {})

    assert configuration["type"] == "stereo_camera"
    assert configuration["frame_rate"] == 30
    assert configuration["image_width"] == 1280
    assert configuration["image_height"] == 720
    assert configuration["horizontal_fov"] == 104.0
