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


from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    OpaqueFunction,
    GroupAction
)

from launch_ros.actions import PushRosNamespace
from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

from romea_common_bringup import device_link_name, robot_urdf_prefix
from romea_common_description import save_device_specifications_file
from romea_camera_bringup import CameraMetaDescription, get_sensor_configuration
from romea_camera_description import get_camera_complete_configuration

def get_mode(context):
    mode = LaunchConfiguration("mode").perform(context)
    if mode == "simulation":
       return "simulation_gazebo_classic"
    else :
       return mode 

def get_robot_namespace(context):
    return LaunchConfiguration("robot_namespace").perform(context)

def get_meta_description(context):

    meta_description_file_path = LaunchConfiguration(
        "meta_description_file_path"
    ).perform(context)

    return CameraMetaDescription(meta_description_file_path)

def launch_setup(context, *args, **kwargs):

    mode = get_mode(context)
    robot_namespace = get_robot_namespace(context)
    meta_description = get_meta_description(context)

    camera_name = meta_description.get_name()
    camera_namespace = str(meta_description.get_namespace() or "")

    user_configuration = get_sensor_configuration(meta_description)

    complete_configuration = get_camera_complete_configuration(
        meta_description.get_type(), meta_description.get_model(), user_configuration)

    complete_configuration_yaml_file = save_device_specifications_file(
        robot_urdf_prefix(robot_namespace), camera_name, complete_configuration
    )

    actions=[
        PushRosNamespace(robot_namespace),
        PushRosNamespace(camera_namespace),
        PushRosNamespace(camera_name)
    ]

    if mode == "live" and meta_description.get_driver_pkg() is not None:
        actions.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        PathJoinSubstitution(
                            [
                                FindPackageShare("romea_camera_bringup"),
                                "launch",
                                "drivers/" + meta_description.get_driver_pkg() + ".launch.py",
                            ]
                        )
                    ]
                ),
                launch_arguments={
                    "video_device": meta_description.get_driver_video_device(),
                    "frame_id": device_link_name(robot_namespace, camera_name),
                    "configuration_file_path": complete_configuration_yaml_file,
                }.items(),
            )
        )

    if mode == "simulation_gazebo" :
        actions.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        PathJoinSubstitution(
                            [
                                FindPackageShare("romea_camera_bringup"),
                                "launch",
                                "drivers/gazebo_bridge.launch.py",
                            ]
                        )
                    ]
                ),
                launch_arguments={
                    "frame_id": device_link_name(robot_namespace, camera_name),
                    "configuration_file_path": complete_configuration_yaml_file,
                }.items(),
            )
        )

    # add launch viewer

    return [GroupAction(actions)]


def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(DeclareLaunchArgument("meta_description_file_path"))

    declared_arguments.append(
        DeclareLaunchArgument("robot_namespace", default_value="")
    )

    declared_arguments.append(
        DeclareLaunchArgument("mode", default_value="live")
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
