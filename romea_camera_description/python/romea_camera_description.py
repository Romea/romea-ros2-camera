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

import math
import xacro

from ament_index_python.packages import get_package_share_directory

from romea_common_description import (
    evaluate_parameter,
    evaluate_parameter_from_list,
    evaluate_parameter_from_range,
    get_device_geometry_file_path,
    get_device_geometry,
    get_device_specifications,
    save_device_specifications_file,
)


def image_width(resolution):
    return int(resolution.split("x")[0])


def image_height(resolution):
    return int(resolution.split("x")[1])


def evaluate_camera_parameter(
    camera_type, camera_model, specifications, user_configuration, parameter_name, key_value=None
):
    return evaluate_parameter(
        "camera", camera_type, camera_model, specifications, user_configuration, parameter_name, key_value
    )


def evaluate_camera_parameter_from_list(
    camera_type, camera_model, specifications, user_configuration, parameter_name, key_value=None
):
    return evaluate_parameter_from_list(
        "camera", camera_type, camera_model, specifications, user_configuration, parameter_name, key_value
    )


def evaluate_camera_parameter_from_range(
    camera_type, camera_model, specifications, user_configuration, parameter_name, key_value=None
):
    return evaluate_parameter_from_range(
        "camera", camera_type, camera_model, specifications, user_configuration, parameter_name, key_value
    )


def get_camera_geometry_file_path(camera_type, camera_model):
    return get_device_geometry_file_path("camera", camera_type, camera_model)

def get_camera_geometry(camera_type, camera_model):
    return get_device_geometry("camera", camera_type, camera_model)


def get_camera_specifications(camera_type, camera_model):
    return get_device_specifications("camera", camera_type, camera_model)


def get_camera_complete_configuration(camera_type, camera_model, user_configuration):
    if camera_type == "axis":
        return get_axis_complete_configuration(camera_model, user_configuration)

    raise LookupError("Cannot get camera configuration")


def get_axis_complete_configuration(camera_model, user_configuration):

    specifications = get_camera_specifications("axis", camera_model)
    
    configuration = {}
    resolution = evaluate_camera_parameter_from_list(
        "axis", camera_model, specifications, user_configuration, "resolution")

    configuration["image_width"] = image_width(resolution)
    configuration["image_height"] = image_height(resolution)

    configuration["horizontal_fov"] = evaluate_camera_parameter_from_range(
            "axis", camera_model, specifications, user_configuration, "horizontal_fov"
    ) * math.pi/180.

    configuration["frame_rate"] = evaluate_camera_parameter(
        "axis", camera_model, specifications, user_configuration, "frame_rate", resolution
    )
    # configuration["video_mode"] = evaluate_camera_parameter(
    #     "axis", camera_model, specifications, user_configuration, "video_mode", resolution
    # )
    configuration["video_format"] = evaluate_camera_parameter_from_list(
        "axis", camera_model, specifications, user_configuration, "video_format"
    )

    return configuration


def urdf(prefix, mode, name, type, model, user_configuration, user_geometry, ros_namespace):

    complete_configuration = get_camera_complete_configuration(type, model, user_configuration)
    complete_configuration_yaml_file = save_device_specifications_file(prefix, name, complete_configuration)
    geometry_yaml_file = get_camera_geometry_file_path(type, model)

    xacro_file = get_package_share_directory("romea_camera_description") + "/urdf/camera.xacro.urdf"

    urdf_xml = xacro.process_file(
        xacro_file,
        mappings={
            "prefix": prefix,
            "mode": mode,
            "name": name,
            "type": type,
            "model": model,
            "sensor_config_yaml_file": complete_configuration_yaml_file,
            "geometry_config_yaml_file": geometry_yaml_file,
            "parent_link": user_geometry["parent_link"],
            "xyz": " ".join(map(str, user_geometry["xyz"])),
            "rpy": " ".join(map(str, user_geometry["rpy"])),
            "mesh_visual": str(True),
            "ros_namespace": ros_namespace,
        },
    )
    return urdf_xml.toprettyxml()
