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


import xacro
import yaml
import math
from romea_common_description import DeviceConfiguration as Device
from ament_index_python.packages import get_package_share_directory


def image_width(resolution):
    return int(resolution.split("x")[0])


def image_height(resolution):
    return int(resolution.split("x")[1])


def get_camera_specifications_file_path(type, model):
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/{type}_{model}_specifications.yaml'


def get_camera_specifications(type, model):
    with open(get_camera_specifications_file_path(type, model)) as f:
        return yaml.safe_load(f)


def get_camera_geometry_file_path(type, model):
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/{type}_{model}_geometry.yaml'


def get_lidar_geometry(type, model):
    with open(get_camera_geometry_file_path(type, model)) as f:
        return yaml.safe_load(f)


def get_camera_specification_units_file_path():
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/specifications_units.yaml'


def get_camera_specification_units():
    with open(get_camera_specification_units_file_path()) as f:
        return yaml.safe_load(f)


def get_camera_complete_configuration(camera_name, user_configuration):

    type = user_configuration["type"]
    model = user_configuration["model"]
    camera_name = f'{type} {model} camera called {camera_name}'
    specifications = get_camera_specifications(type, model)
    specifications_units = get_camera_specification_units()

    camera = Device(camera_name, specifications, user_configuration, specifications_units)

    configuration = {}
    configuration["frame_rate"] = camera.get("frame_rate")
    configuration["image_width"] = image_width(camera.get("resolution"))
    configuration["image_height"] = image_height(camera.get("resolution"))
    configuration["horizontal_fov"] = camera.get("horizontal_fov")
    configuration["video_format"] = camera.get("video_format")

    return configuration


def urdf(prefix, mode, camera_name, camera_description, camera_location, ros_namespace):

    configuration = get_camera_complete_configuration(camera_name, camera_description)

    configuration_yaml_file = f'/tmp/{prefix}{camera_name}urdf_configuration.yaml'

    with open(configuration_yaml_file, 'w') as f:
        yaml.dump({**configuration, **camera_location}, f)

    geometry_yaml_file = get_camera_geometry_file_path(
        camera_description["type"], camera_description["model"]
    )

    xacro_file = (
        get_package_share_directory("romea_camera_description") + "/urdf/camera.xacro.urdf"
    )

    if mode == "simulation":
        mode += "_gazebo_classic"

    urdf_xml = xacro.process_file(
        xacro_file,
        mappings={
            "prefix": prefix,
            "mode": mode,
            "name": camera_name,
            # "type": camera_description["type"],
            # "model": camera_description["model"],
            "sensor_config_yaml_file": configuration_yaml_file,
            "geometry_config_yaml_file": geometry_yaml_file,
            # "parent_link": camera_geometry["parent_link"],
            # "xyz": " ".join(map(str, camera_geometry["xyz"])),
            # "rpy": " ".join(map(str, camera_geometry["rpy"])),
            "mesh_visual": str(True),
            "ros_namespace": ros_namespace,
        },
    )
    return urdf_xml.toprettyxml()
