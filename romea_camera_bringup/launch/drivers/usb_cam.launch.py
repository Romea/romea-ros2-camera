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
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def get_configuration(context):

    configuration_file_path = LaunchConfiguration("configuration_file_path").perform(context)

    with open(configuration_file_path, 'r') as f :
       return  yaml.safe_load(f)


def launch_setup(context, *args, **kwargs):

    configuration = get_configuration(context)
    video_device = LaunchConfiguration("video_device").perform(context)
    frame_id = LaunchConfiguration("frame_id").perform(context)

    driver = LaunchDescription()

    print(video_device)

    parameters = {
        "video_device": video_device,
        "frame_id": frame_id,
        "frame_rate": configuration["frame_rate"],
        "image_height": configuration["image_height"],
        "image_width": configuration["image_width"],
    }

    driver_node = Node(
        package="usb_cam",
        executable="usb_cam_node_exe",
        output="screen",
        name="driver",
        parameters=[parameters],
    )

    driver.add_action(driver_node)

    return [driver]


#   this->declare_parameter("camera_name", "default_cam");
#   this->declare_parameter("pixel_format", "yuyv");
#   this->declare_parameter("av_device_format", "YUV422P");
#   this->declare_parameter("brightness", 50);  // 0-255, -1 "leave alone"
#   this->declare_parameter("contrast", -1);    // 0-255, -1 "leave alone"
#   this->declare_parameter("saturation", -1);  // 0-255, -1 "leave alone"
#   this->declare_parameter("sharpness", -1);   // 0-255, -1 "leave alone"
#   this->declare_parameter("gain", -1);        // 0-100?, -1 "leave alone"
#   this->declare_parameter("auto_white_balance", true);
#   this->declare_parameter("white_balance", 4000);
#   this->declare_parameter("autoexposure", true);
#   this->declare_parameter("exposure", 100);
#   this->declare_parameter("autofocus", false);
#   this->declare_parameter("focus", -1);  // 0-255, -1 "leave alone"


def generate_launch_description():

    declared_arguments = []
    declared_arguments.append(DeclareLaunchArgument("video_device"))
    declared_arguments.append(DeclareLaunchArgument("frame_id"))
    declared_arguments.append(DeclareLaunchArgument("configuration_file_path"))

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
