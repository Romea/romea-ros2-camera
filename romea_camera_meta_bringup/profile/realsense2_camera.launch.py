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
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def get_module_parameter(module_name, parameter, context):
    return LaunchConfiguration(f"{module_name}.{parameter}").perform(context)


def get_module_profile(module_name, context):
    image_width = get_module_parameter(module_name, "image_width", context)
    image_height = get_module_parameter(module_name, "image_height", context)
    frame_rate = get_module_parameter(module_name, "frame_rate", context)
    return f"{image_width},{image_height},{frame_rate}"


def get_module_image_format(module_name, context):
    return get_module_parameter(module_name, "image_format", context)


def launch_setup(context, *args, **kwargs):

    device = LaunchConfiguration("device").perform(context)
    enable_color = bool(LaunchConfiguration("enable_color").perform(context))
    enable_depth = bool(LaunchConfiguration("enable_depth").perform(context))
    enable_rgbd = bool(LaunchConfiguration("enable_rgbd").perform(context))
    enable_infra = bool(LaunchConfiguration("enable_infra").perform(context))
    enable_infra_left = bool(LaunchConfiguration("enable_infra_left").perform(context))
    enable_infra_right = bool(LaunchConfiguration("enable_infra_right").perform(context))

    mode = LaunchConfiguration("mode").perform(context)
    rgb_camera_profile = get_module_profile("rgb_camera", context)
    rgb_camera_image_format = get_module_image_format("rgb_camera", context)
    depth_camera_profile = get_module_profile("depth_camera", context)
    depth_camera_image_format = get_module_image_format("depth_camera", context)
    infrared_camera_profile = get_module_profile("infrared_camera", context)
    infrared_camera_image_format = get_module_image_format("infrared_camera", context)

    launch = LaunchDescription()

    if mode == "live":

        parameters = {
            # camera unique name
            "camera_name": "camera",
            # 'namespace for camera
            "camera_namespace": "",
            # choose device by serial number'
            "serial_no": "",
            # choose device by usb port id'
            "usb_port_id": "",
            # choose device by type'
            "device_type": device,
            # yaml config file,
            "config_file": "",
            # allows advanced configuration
            "json_file_path": "",
            # enable reconfiguration at start
            "initial_reset": False,
            # enable GPU acceleration with GLSL
            "accelerate_gpu_with_glsl": False,
            # A realsense bagfile to run from as a device'
            "rosbag_filename": "",
            # debug log level [DEBUG|INFO|WARN|ERROR|FATAL]'
            "log_level": "info",
            # pipe node output [screen|log]'
            "output": "screen",
            # description': 'enable color stream
            "enable_color": enable_color or enable_rgbd,
            # color stream profile
            "rgb_camera.color_profile": rgb_camera_profile,
            # color stream format
            "rgb_camera.color_format": rgb_camera_image_format,
            # enable/disable auto exposure for color image
            "rgb_camera.enable_auto_exposure": True,
            # enable depth stream
            "enable_depth": enable_depth or enable_rgbd,
            # enable infra0 stream
            "enable_infra": enable_infra,
            # enable infra1 stream
            "enable_infra1": enable_infra_left,
            # enable infra2 stream'
            "enable_infra2": enable_infra_right,
            # depth stream profile
            "depth_module.depth_profile": depth_camera_profile,
            # depth stream format
            "depth_module.depth_format": depth_camera_image_format,
            # infra streams (0/1/2) profile
            "depth_module.infra_profile": infrared_camera_profile,
            # infra0 stream format
            "depth_module.infra_format": infrared_camera_image_format,
            # infra1 stream format
            "depth_module.infra1_format": infrared_camera_image_format,
            # infra2 stream format
            "depth_module.infra2_format": infrared_camera_image_format,
            # enable/disable auto exposure for depth image
            "depth_module.enable_auto_exposure": True,
            # depth module manual exposure value,
            "depth_module.exposure": 8500,
            # Depth module manual gain value'
            "depth_module.gain": 16,
            # Depth module hdr enablement flag. Used for hdr_merge filter
            "depth_module.hdr_enabled": False,
            # Depth module first exposure value. Used for hdr_merge filter
            # 'depth_module.exposure.1' : '7500',
            # Depth module first gain value. Used for hdr_merge filter
            # 'depth_module.gain.1': '16',
            # Depth module second exposure value. Used for hdr_merge filter
            # 'depth_module.exposure.2': '1',
            # Depth module second gain value. Used for hdr_merge filter',
            # 'depth_module.gain.2': '16',
            # enable sync mode
            "enable_sync": enable_rgbd,
            # enable rgbd topic
            "enable_rgbd": enable_rgbd,
            # enable gyro stream
            "enable_gyro": False,
            # enable accel stream
            "enable_accel": False,
            "gyro_fps": 0,
            "accel_fps": 0,
            # [0-None, 1-copy, 2-linear_interpolation]
            "unite_imu_method": 0,
            # clip distance, no clip if a negative value is given
            "clip_distance": -2.0,
            # angular velocity variance
            "angular_velocity_cov": 0.01,
            # angular acceleration variance
            "linear_accel_cov": 0.01,
            # Rate of publishing diagnostics. 0=Disable
            "diagnostics_period": 0.0,
            # enable/disable publishing static & dynamic TF
            "publish_tf": False,
            # rate in Hz for publishing dynamic TF
            "tf_publish_rate": 0.0,
            # enable/disable publishing point cloud
            "pointcloud.enable": False,
            # texture stream for pointcloud
            "pointcloud.stream_filter": 2,
            # texture stream index for pointcloud'
            "pointcloud.stream_index_filter": 0,
            # enable/disable ordered point cloud
            "pointcloud.ordered_pc": False,
            # enable/disable add texture cloud
            "pointcloud.allow_no_texture_points": False,
            # enable align depth filter
            "align_depth.enable": enable_rgbd,
            # enable colorizer filter
            "colorizer.enable": False,
            # enable_decimation_filter'
            "decimation_filter.enable": False,
            # enable_spatial_filter'
            "spatial_filter.enable": False,
            # enable_temporal_filter'
            "temporal_filter.enable": False,
            # enable_disparity_filter,
            "disparity_filter.enable": False,
            # enable_hole_filling_filter,
            "hole_filling_filter.enable": False,
            # hdr_merge filter enablement flag'},
            "hdr_merge.enable": False,
            # timeout(seconds) for waiting for device to connect
            "wait_for_device_timeout": -1.0,
            # timeout(seconds) between consequtive reconnection attempts
            "reconnect_timeout": 6.0,
        }

        remappings = [
            (
                "driver/aligned_depth_to_color/camera_info",
                "aligned_depth_to_color/camera_info",
            ),
            ("driver/aligned_depth_to_color/image_raw", "aligned_depth_to_color/image_raw"),
            (
                "driver/aligned_depth_to_color/image_raw/compressed",
                "aligned_depth_to_color/image_raw/compressed",
            ),
            (
                "driver/aligned_depth_to_color/image_raw/compressedDepth",
                "aligned_depth_to_color/image_raw/compressedDepth",
            ),
            (
                "driver/aligned_depth_to_color/image_raw/theora",
                "aligned_depth_to_color/image_raw/theora",
            ),
            ("driver/aligned_depth_to_color/metadata", "depth/metadata"),
            ("driver/color/camera_info", "rgb/camera_info"),
            ("driver/color/image_raw", "rgb/image_raw"),
            ("driver/color/image_raw/compressed", "rgb/image_raw/compressed"),
            ("driver/color/image_raw/compressedDepth", "rgb/image_raw/compressedDepth"),
            ("driver/color/image_raw/theora", "rgb/image_raw/theora"),
            ("driver/color/metadata", "depth/metadata"),
            ("driver/depth/camera_info", "depth/camera_info"),
            ("driver/depth/image_rect_raw", "depth/image_raw"),
            ("driver/depth/image_rect_raw/compressed", "depth/image_raw/compressed"),
            ("driver/depth/image_rect_raw/compressedDepth", "depth/image_raw/compressedDepth"),
            ("driver/depth/image_rect_raw/theora", "depth/image_raw/theora"),
            ("driver/depth/metadata", "depth/metadata"),
            ("driver/infra1/camera_info", "infrared_right/camera_info"),
            ("driver/infra1/image_rect_raw", "infrared_right/image_raw"),
            ("driver/infra1/image_rect_raw/compressed", "infrared_right/image_raw/compressed"),
            (
                "driver/infra1/image_rect_raw/compressedDepth",
                "infrared_right/image_raw/compressedDepth",
            ),
            ("driver/infra1/image_rect_raw/theora", "infrared_right/image_raw/theora"),
            ("driver/infra1/metadata", "infrared_right/metadata"),
            ("driver/infra2/camera_info", "infrared_left/camera_info"),
            ("driver/infra2/image_rect_raw", "infrared_left/image_raw"),
            ("driver/infra2/image_rect_raw/compressed", "infrared_left/image_raw/compressed"),
            (
                "driver/infra2/image_rect_raw/compressedDepth",
                "infrared_left/image_raw/compressedDepth",
            ),
            ("driver/infra2/image_rect_raw/theora", "infrared_left/image_raw/theora"),
            ("driver/infra2/metadata", "infrared_left/metadata"),
            ("driver/depth/color/points", "points"),
            ("driver/extrinsics/depth_to_color", "extrinsics/depth_to_color"),
            ("driver/extrinsics/depth_to_depth", "extrinsics/depth_to_depth"),
            ("driver/imu", "imu"),
        ],

        launch.add_action(
            Node(
                package="realsense2_camera",
                executable="realsense2_camera_node",
                output="screen",
                name="driver",
                parameters=[parameters],
                # remappings=remappings,
            )
        )

    return [launch]


def generate_launch_description():

    return LaunchDescription(
        [
            DeclareLaunchArgument("device"),
            DeclareLaunchArgument("enable_color", default_value="true"),
            DeclareLaunchArgument("enable_depth", default_value="true"),
            DeclareLaunchArgument("enable_rgbd", default_value="false"),
            DeclareLaunchArgument("enable_infra", default_value="false"),
            DeclareLaunchArgument("enable_infra_left", default_value="false"),
            DeclareLaunchArgument("enable_infra_right", default_value="false"),
            OpaqueFunction(function=launch_setup)
        ]
    )
