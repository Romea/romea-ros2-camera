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
    type = "axis"
    model = "p1346"

    configuration={
        "resolution": "1280x720",
        "frame_rate": 30,
        "horizontal_fov": None,
        "video_format": None,
    }

    geometry ={
        "parent_link" : "base_link",
        "xyz" : [1.0, 2.0, 3.0],
        "rpy" : [4.0, 5.0, 6.0],
    }

    ros_namespace = "ns"

    print(urdf(prefix, mode, name, type, model, configuration, geometry, ros_namespace))
    return ET.fromstring(urdf(prefix, mode, name, type, model, configuration, geometry, ros_namespace))


def test_camera_name(urdf_xml):
    assert urdf_xml.find("link").get("name") == "robot_camera_link"


def test_camera_position(urdf_xml):
    assert urdf_xml.find("joint/origin").get("xyz") == "1.0 2.0 3.0 "


def test_camera_orientation(urdf_xml):
    assert urdf_xml.find("joint/origin").get("rpy") == "4.0 5.0 6.0"


def test_camera_parent_link(urdf_xml):
    assert urdf_xml.find("joint/parent").get("link") == "robot_base_link"


def test_sensor_update_rate(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/update_rate").text == "30"


def test_plugin_namespace(urdf_xml):
    assert urdf_xml.find("gazebo/sensor/plugin/ros/namespace").text == "ns"
