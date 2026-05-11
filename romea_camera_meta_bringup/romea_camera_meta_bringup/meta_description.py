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

import romea_camera_description
from romea_common_meta_bringup.meta_description import SensorMetaDescription
from romea_common_meta_bringup.ros_launch import LaunchFileGenerator


class CameraMetaDescription(SensorMetaDescription):
    def __init__(self, meta_description_file_path, robot_name=None):
        super().__init__("lidar", meta_description_file_path, robot_name)

    def get_frame_rate(self, component=None):
        return self._get_or("frame_rate", self.__full_param_ns(component))

    def get_resolution(self, component=None):
        return self._get_or("resolution", self.__full_param_ns(component))

    def __full_param_ns(seld, component):
        return "configuration" if component is None else f"configuration.{component}"


def load_meta_description(meta_description_file_path, robot_name=None):
    return CameraMetaDescription(meta_description_file_path, robot_name)


def get_specifications(meta_description):
    return romea_camera_description.get_camera_specifications(
        meta_description.get_configuration()
    )


def get_geometry(meta_description):
    return romea_camera_description.get_camera_geometry(
        meta_description.get_configuration()
    )


def get_complete_configuration(meta_description):
    return romea_camera_description.get_complete_configuration(
        meta_description.get_name(),
        meta_description.get_configuration(),
        meta_description.get_location()
    )


def generate_yaml_configuration_file_str(meta_description, extended):
    configuration = get_complete_configuration(meta_description)
    return romea_camera_description.generate_configuration_file(configuration, extended)


def generate_yaml_launch_file_str(meta_description):
    launch_file = meta_description.get_launch_file()
    launch_arguments = [{"name": "mode", "default": "live"}]
    namespaces = [
        meta_description.get_robot_name(),
        meta_description.get_namespace(),
        meta_description.get_name(),
    ]
    configuration = get_complete_configuration(meta_description)
    configuration["tf_prefix"] = meta_description.get_urdf_prefix()
    configuration["frame_id"] = meta_description.get_link()

    return LaunchFileGenerator("camera").generate(
        launch_file, launch_arguments, namespaces, configuration
    )


def generate_xml_urdf_description_str(mode, meta_description, standalone=False):

    return romea_camera_description.generate_urdf_description(
        meta_description.get_urdf_prefix(),
        mode,
        meta_description.get_name(),
        meta_description.get_configuration(),
        meta_description.get_location(),
        meta_description.get_full_namespace(),
        standalone,
    )
