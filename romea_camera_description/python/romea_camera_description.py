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
import romea_common_description
# from romea_common_description import DeviceConfiguration as Device
# from romea_common_description import generate_configuration_file
# from romea_common_description import get_specifications_file_path
# from romea_common_description import get_geometry_file_path
from ament_index_python.packages import get_package_share_directory


def image_width(resolution):
    return int(resolution.split("x")[0])


def image_height(resolution):
    return int(resolution.split("x")[1])


def get_specifications_file_path(camera_description):
    return romea_common_description.get_specifications_file_path(
        "romea_camera_description", camera_description
    )


def get_specifications(camera_description):
    with open(get_specifications_file_path(camera_description)) as f:
        return yaml.safe_load(f)


def get_geometry_file_path(camera_description):
    return romea_common_description.get_geometry_file_path(
        "romea_camera_description", camera_description
    )


def get_geometry(camera_description):
    with open(get_geometry_file_path(camera_description)) as f:
        return yaml.safe_load(f)


def get_specification_units_file_path():
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/specifications_units.yaml'


def get_specification_units():
    with open(get_specification_units_file_path()) as f:
        return yaml.safe_load(f)


def get_complete_component_configuration(
    component_name, specifications, camera_description
):
    component = romea_common_description.DeviceConfiguration(
        component_name, specifications, camera_description, get_specification_units()
    )

    return {
     "type": component.get("type"),
     "frame_rate": component.get("frame_rate"),
     "image_width": image_width(component.get("resolution")),
     "image_height": image_height(component.get("resolution")),
     "image_format": component.get("image_format"),
     "horizontal_fov": component.get("horizontal_fov")
    }


def get_complete_configuration(camera_name, camera_description, camera_location):

    model = camera_description["model"]
    version = camera_description["version"]
    manufacturer = camera_description["manufacturer"]

    camera_name = f'{manufacturer} {model} {version} camera called {camera_name}'
    specifications = get_specifications(camera_description)

    camera_configuration = {}
    camera_configuration["model"] = camera_description["model"]
    camera_configuration["version"] = camera_description["version"]
    camera_configuration["manufacturer"] = camera_description["manufacturer"]
    if "components" in specifications:
        camera_configuration["type"] = specifications["type"]
        for component_name in specifications["components"]:
            camera_configuration[component_name] = get_complete_component_configuration(
                f"{component_name} component of {camera_name}",
                specifications[component_name],
                camera_description.get(component_name, {}),
            )
    else:
        camera_configuration = get_complete_component_configuration(
            camera_name, specifications, camera_description
        )

    return {**camera_configuration, **camera_location}


def generate_configuration_file(configuration, extended):
    units = get_specification_units()
    return romea_common_description.generate_configuration_file(configuration, units, extended)


def generate_urdf_description(
    prefix, mode, camera_name, camera_description, camera_location, ros_namespace
):

    configuration = get_complete_configuration(
        camera_name, camera_description, camera_location
    )

    configuration_yaml_file = f'/tmp/{prefix}{camera_name}_configuration.yaml'
    with open(configuration_yaml_file, 'w') as f:
        f.write(generate_configuration_file(configuration, False))

    geometry_yaml_file = get_geometry_file_path(camera_description)

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
            "sensor_config_yaml_file": configuration_yaml_file,
            "geometry_config_yaml_file": geometry_yaml_file,
            "mesh_visual": str(True),
            "ros_namespace": ros_namespace,
        },
    )
    return urdf_xml.toprettyxml()
