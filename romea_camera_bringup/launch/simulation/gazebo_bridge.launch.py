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

import yaml

from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    OpaqueFunction,
)

from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def get_configuration(context):

    configuration_file_path = LaunchConfiguration("configuration_file_path").perform(context)

    with open(configuration_file_path, 'r') as f :
       return  yaml.safe_load(f)


def launch_setup(context, *args, **kwargs):

    configuration = get_configuration(context)
    frame_id = LaunchConfiguration("frame_id").perform(context)
    return []


def generate_launch_description():

    declared_arguments = []
    declared_arguments.append(DeclareLaunchArgument("frame_id"))
    declared_arguments.append(DeclareLaunchArgument("configuration_file_path"))

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )