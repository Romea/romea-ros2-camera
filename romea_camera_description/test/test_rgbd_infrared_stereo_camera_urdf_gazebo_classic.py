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


import xml.etree.ElementTree as ET

import pytest
from romea_camera_description import generate_urdf_description as urdf


@pytest.fixture(scope="module")
def urdf_xml():
    prefix = "robot_"
    mode = "simulation"
    name = "rgbd_infrared_stereo_camera"

    description = {
        "manufacturer": "intel",
        "model": "realsense",
        "version": "d435"
    }
    description["rgb_camera"] = {
        "resolution": "1920x1080",
        "frame_rate": 30,
    }
    description["infrared_camera"] = {
        "resolution": "848x480",
        "frame_rate": 30,
    }
    description["depth_camera"] = {
        "resolution": "1280x720",
        "frame_rate": 30,
    }

    location = {
        "parent_link": "base_link",
        "xyz": [1.0, 2.0, 3.0],
        "rpy": [4.0, 5.0, 6.0],
    }

    ros_namespace = "ns"

    print(urdf(prefix, mode, name, description, location, ros_namespace))
    with open('/tmp/rgbd_infrared_stereo_camera_urdf', 'w') as file:
        file.write(urdf(prefix, mode, name, description, location, ros_namespace))

    return ET.fromstring(urdf(prefix, mode, name, description, location, ros_namespace))


def test_rgbd_camera_name(urdf_xml):
    assert urdf_xml.find("link").get("name") == "robot_rgbd_infrared_stereo_camera_link"


# def test_rgbd_position(urdf_xml):
#     assert urdf_xml.find("joint/origin").get("xyz") == "1.0 2.0 3.0"


# def test_rgbd_camera_orientation(urdf_xml):
#     assert (
#         urdf_xml.find("joint/origin").get("rpy")
#         == "0.06981317007977318 0.08726646259971647 0.10471975511965977"
#     )


# def test_rgbd_camera_parent_link(urdf_xml):
#     assert urdf_xml.find("joint/parent").get("link") == "robot_base_link"


# def test_rgbd_sensor_update_rate(urdf_xml):
#     assert urdf_xml.find("gazebo/sensor/update_rate").text == "30"


# def test_plugin_namespace(urdf_xml):
#     assert urdf_xml.find("gazebo/sensor/plugin/ros/namespace").text == "ns"
