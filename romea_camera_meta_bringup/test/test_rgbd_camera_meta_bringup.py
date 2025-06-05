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


import os
import pytest

from romea_camera_meta_bringup import CameraMetaDescription


@pytest.fixture(scope="module")
def meta_description():
    meta_description_file_path = os.path.join(os.getcwd(), "test_rgbd_camera_meta_bringup.yaml")
    return CameraMetaDescription(meta_description_file_path)


def test_get_name(meta_description):
    assert meta_description.get_name() == "camera"


def test_get_namespace(meta_description):
    assert meta_description.get_namespace() == "ns"


def test_get_launch_file(meta_description):
    assert meta_description.get_launch_file() is not None


def test_get_manufacturer(meta_description):
    assert meta_description.get_manufacturer() == "realsense"


def test_get_model(meta_description):
    assert meta_description.get_model() == "d435"


def test_get_rgb_frame_rate(meta_description):
    assert meta_description.get_frame_rate("rgb_camera") == 15


def test_get_rgb_resolution_(meta_description):
    print(meta_description.get_resolution("rgb_camera"))
    assert meta_description.get_resolution("rgb_camera") == "640x480"


def test_get_depth_frame_rate(meta_description):
    assert meta_description.get_frame_rate("depth_camera") == 30


def test_get_depth_resolution_(meta_description):
    assert meta_description.get_resolution("depth_camera") == "640x480"


def test_get_infrared_frame_rate(meta_description):
    assert meta_description.get_frame_rate("infrared_camera") == 60


def test_get_infrared_resolution_(meta_description):
    assert meta_description.get_resolution("infrared_camera") == "640x480"


def test_get_parent_link(meta_description):
    assert meta_description.get_parent_link() == "base_link"


# def test_get_xyz(meta_description):
#     assert meta_description.get_xyz() == [1.0, 2.0, 3.0]


# def test_get_rpy_deg(meta_description):
#     assert meta_description.get_rpy() == [4.0, 5.0, 6.0]
