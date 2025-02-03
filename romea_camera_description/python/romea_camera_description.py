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
from romea_common_description import DeviceConfiguration as Device
from ament_index_python.packages import get_package_share_directory


def image_width(resolution):
    return int(resolution.split("x")[0])


def image_height(resolution):
    return int(resolution.split("x")[1])


def get_camera_specifications_file_path(manufacturer, model):
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/{manufacturer}_{model}_specifications.yaml'


def get_camera_specifications(manufacturer, model):
    with open(get_camera_specifications_file_path(manufacturer, model)) as f:
        return yaml.safe_load(f)


def get_camera_geometry_file_path(manufacturer, model):
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/{manufacturer}_{model}_geometry.yaml'


def get_camera_geometry(manufacturer, model):
    with open(get_camera_geometry_file_path(manufacturer, model)) as f:
        return yaml.safe_load(f)


def get_camera_specification_units_file_path():
    pkg_path = get_package_share_directory('romea_camera_description')
    return f'{pkg_path}/config/specifications_units.yaml'


def get_camera_specification_units():
    with open(get_camera_specification_units_file_path()) as f:
        return yaml.safe_load(f)


def get_camera_complete_component_configuration(
    component_name, specifications, user_configuration
):
    component = Device(
        component_name, specifications, user_configuration, get_camera_specification_units()
    )

    configuration = {}
    configuration["type"] = component.get("type")
    configuration["frame_rate"] = component.get("frame_rate")
    configuration["image_width"] = image_width(component.get("resolution"))
    configuration["image_height"] = image_height(component.get("resolution"))
    configuration["horizontal_fov"] = component.get("horizontal_fov")

    return configuration


def get_camera_complete_configuration(camera_name, user_configuration):

    model = user_configuration["model"]
    manufacturer = user_configuration["manufacturer"]
    camera_name = f'{manufacturer} {model} camera called {camera_name}'
    specifications = get_camera_specifications(manufacturer, model)

    configuration = {}
    if "components" in specifications:
        configuration["type"] = specifications["type"]
        for component_name in specifications["components"]:
            configuration[component_name] = get_camera_complete_component_configuration(
                f"{component_name} component of {camera_name}",
                specifications[component_name],
                user_configuration.get(component_name, {}),
            )
    else:
        configuration = get_camera_complete_component_configuration(
            camera_name, specifications, user_configuration
        )

    return configuration


def urdf(prefix, mode, camera_name, camera_description, camera_location, ros_namespace):

    configuration = get_camera_complete_configuration(camera_name, camera_description)

    configuration_yaml_file = f'/tmp/{prefix}{camera_name}_urdf_configuration.yaml'

    with open(configuration_yaml_file, 'w') as f:
        yaml.dump({**configuration, **camera_location}, f)

    geometry_yaml_file = get_camera_geometry_file_path(
        camera_description["manufacturer"], camera_description["model"]
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
            "sensor_config_yaml_file": configuration_yaml_file,
            "geometry_config_yaml_file": geometry_yaml_file,
            "mesh_visual": str(True),
            "ros_namespace": ros_namespace,
        },
    )
    return urdf_xml.toprettyxml()
