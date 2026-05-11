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

# from launch_ros.actions import SetRemap

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LoadComposableNodes, Node
from launch_ros.descriptions import ComposableNode


class LaunchVariables:
    def __init__(self, context):
        self.__context = context

    def get(self, variable_name):
        return LaunchConfiguration(variable_name).perform(self.__context)


def launch_setup(context, *args, **kwargs):

    var = LaunchVariables(context)

    mode = var.get("mode")
    container = var.get("container")
    ros_namespace = var.get("ros_namespace")
    camera_type = var.get("type")
    # print(context.launch_configurations)

    if camera_type == "monocular_camera":
        common_arguments = {
            "package": "ros_gz_bridge",
            "name": "gz_bridge",
            "parameters": [
                {
                    "bridge_names": ["image_bridge", "info_bridge"],
                    "bridges.image_bridge.ros_topic_name": f"{ros_namespace}/image_raw",
                    "bridges.image_bridge.gz_topic_name": f"{ros_namespace}/image_raw",
                    "bridges.image_bridge.ros_type_name": "sensor_msgs/msg/Image",
                    "bridges.image_bridge.gz_type_name": "gz.msgs.Image",
                    "bridges.image_bridge.direction": "GZ_TO_ROS",
                    "bridges.image_bridge.lazy": True,
                    "bridges.image_bridge.qos_profile": "SENSOR_DATA",
                    "bridges.info_bridge.ros_topic_name": f"{ros_namespace}/camera_info",
                    "bridges.info_bridge.gz_topic_name": f"{ros_namespace}/camera_info",
                    "bridges.info_bridge.ros_type_name": "sensor_msgs/msg/CameraInfo",
                    "bridges.info_bridge.gz_type_name": "gz.msgs.CameraInfo",
                    "bridges.info_bridge.direction": "GZ_TO_ROS",
                    "bridges.info_bridge.lazy": True,
                    "bridges.info_bridge.qos_profile": "SENSOR_DATA",
                }
            ]
        }

    elif camera_type == "stereo_camera":

        common_arguments = {
            "package": "ros_gz_bridge",
            "name": "gz_bridge",
            "parameters": [
                {
                    "bridge_names": [
                        "left_image_bridge",
                        "left_info_bridge",
                        "right_image_bridge",
                        "right_info_bridge",
                    ],
                    "bridges.left_image_bridge.ros_topic_name": f"{ros_namespace}/left/image_raw",
                    "bridges.left_image_bridge.gz_topic_name": f"{ros_namespace}/left/image_raw",
                    "bridges.left_image_bridge.ros_type_name": "sensor_msgs/msg/Image",
                    "bridges.left_image_bridge.gz_type_name": "gz.msgs.Image",
                    "bridges.left_image_bridge.direction": "GZ_TO_ROS",
                    "bridges.left_image_bridge.lazy": True,
                    "bridges.left_image_bridge.qos_profile": "SENSOR_DATA",
                    "bridges.left_info_bridge.ros_topic_name": f"{ros_namespace}/left/camera_info",
                    "bridges.left_info_bridge.gz_topic_name": f"{ros_namespace}/left/camera_info",
                    "bridges.left_info_bridge.ros_type_name": "sensor_msgs/msg/CameraInfo",
                    "bridges.left_info_bridge.gz_type_name": "gz.msgs.CameraInfo",
                    "bridges.left_info_bridge.direction": "GZ_TO_ROS",
                    "bridges.left_info_bridge.lazy": True,
                    "bridges.left_info_bridge.qos_profile": "SENSOR_DATA",
                    "bridges.right_image_bridge.ros_topic_name": f"{ros_namespace}/right/image_raw",
                    "bridges.right_image_bridge.gz_topic_name": f"{ros_namespace}/right/image_raw",
                    "bridges.right_image_bridge.ros_type_name": "sensor_msgs/msg/Image",
                    "bridges.right_image_bridge.gz_type_name": "gz.msgs.Image",
                    "bridges.right_image_bridge.direction": "GZ_TO_ROS",
                    "bridges.right_image_bridge.lazy": True,
                    "bridges.right_image_bridge.qos_profile": "SENSOR_DATA",
                    "bridges.right_info_bridge.ros_topic_name": f"{ros_namespace}/right/camera_info",
                    "bridges.right_info_bridge.gz_topic_name": f"{ros_namespace}/right/camera_info",
                    "bridges.right_info_bridge.ros_type_name": "sensor_msgs/msg/CameraInfo",
                    "bridges.right_info_bridge.gz_type_name": "gz.msgs.CameraInfo",
                    "bridges.right_info_bridge.direction": "GZ_TO_ROS",
                    "bridges.right_info_bridge.lazy": True,
                    "bridges.right_info_bridge.qos_profile": "SENSOR_DATA",
                },
            ],
        }

    launch = LaunchDescription()
    if mode == "simulation_gazebo":

        if container == "":
            executable = "parameter_bridge"
            launch.add_action(Node(**common_arguments, executable=executable))
        else:
            plugin = "ros_gz_bridge::RosGzBridge"
            extra_arguments = [{"use_intra_process_comms": True}]
            launch.add_action(
                LoadComposableNodes(
                    target_container=container,
                    composable_node_descriptions=[
                        ComposableNode(
                            **common_arguments, plugin=plugin, extra_arguments=extra_arguments
                        )
                    ],
                )
            )

    return [launch]


def generate_launch_description():

    return LaunchDescription(
        [
            DeclareLaunchArgument("container", default_value=""),
            OpaqueFunction(function=launch_setup),
        ]
    )
