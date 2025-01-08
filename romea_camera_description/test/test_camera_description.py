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


import pytest
import xml.etree.ElementTree as ET
from romea_camera_description import urdf


@pytest.fixture(scope="module")
def urdf_xml():
    prefix = "robot_"
    mode = "simulation"
    name = "camera"

    description = {
        "type": "axis",
        "model": "p1346",
        "resolution": "1280x720",
        "frame_rate": 30,
        "horizontal_fov": None,
        "video_format": None,
    }

    location = {
        "parent_link": "base_link",
        "xyz": [1.0, 2.0, 3.0],
        "rpy": [4.0, 5.0, 6.0],
    }

    ros_namespace = "ns"

    print(urdf(prefix, mode, name, description, location, ros_namespace))
    with open('/tmp/camera_urdf', 'w') as file:
        file.write(urdf(prefix, mode, name, description, location, ros_namespace))

    return ET.fromstring(urdf(prefix, mode, name, description, location, ros_namespace))


def test_camera_name(urdf_xml):
    assert urdf_xml.find("link").get("name") == "robot_camera_link"


def test_camera_position(urdf_xml):
    assert urdf_xml.find("joint/origin").get("xyz") == "1.0 2.0 3.0"


def test_camera_orientation(urdf_xml):
    assert (
        urdf_xml.find("joint/origin").get("rpy")
        == "0.06981317007977318 0.08726646259971647 0.10471975511965977"
    )


def test_camera_parent_link(urdf_xml):
    assert urdf_xml.find("joint/parent").get("link") == "robot_base_link"


def test_sensor_update_rate(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/update_rate").text == "30"


def test_gazebo_horizontal_fov(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/camera/horizontal_fov").text == "1.2566370614359172"


def test_gazebo_image_width(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/camera/image/width").text == "1280"


def test_gazebo_image_height(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/camera/image/height").text == "720"


def test_plugin_namespace(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/plugin/ros/namespace").text == "ns"
