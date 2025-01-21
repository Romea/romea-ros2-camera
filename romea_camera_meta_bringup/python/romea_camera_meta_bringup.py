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


from romea_common_bringup import MetaDescription, robot_urdf_prefix, device_namespace
import romea_camera_description
from numpy import radians


class CameraMetaDescription:
    def __init__(self, meta_description_file_path, description_type="camera"):
        self.meta_description = MetaDescription(description_type, meta_description_file_path)

    def get_name(self):
        return self.meta_description.get("name")

    def get_namespace(self):
        return self.meta_description.get_or("namespace", None)

    def has_driver_configuration(self):
        return self.meta_description.exists("driver")

    def get_driver_package(self):
        return self.meta_description.get("package", "driver")

    def get_driver_executable(self):
        return self.meta_description.get("executable", "driver")

    def get_driver_parameters(self):
        return self.meta_description.get("parameters", "driver")

    def get_type(self):
        return self.meta_description.get("type", "configuration")

    def get_model(self):
        return self.meta_description.get("model", "configuration")

    def get_configuration(self, ns=None):
        return self.meta_description.get("configuration")

    # perhaps add get_configuration_parameter in MetaDescription class
    def get_configuration_parameter_or(self, parameter_name, ns=None, default_value=None):
        if ns is None:
            return self.meta_description.get_or(parameter_name, "configuration", None)
        else:
            return self.meta_description.get_or(parameter_name, "configuration." + ns, None)

    def get_frame_rate(self, ns=None):
        return self.get_configuration_parameter_or("frame_rate", ns, None)

    def get_resolution(self, ns=None):
        return self.get_configuration_parameter_or("resolution", ns, None)

    def get_horizontal_fov(self, ns=None):
        return self.get_configuration_parameter_or("horizontal_fov", ns, None)

    def get_video_format(self, ns=None):
        return self.get_configuration_parameter_or("video_format", ns, None)

    def get_geometry(self, ns=None):
        return self.meta_description.get("geometry")

    def get_parent_link(self):
        return self.meta_description.get("parent_link", "geometry")

    def get_xyz(self):
        return self.meta_description.get("xyz", "geometry")

    def get_rpy_deg(self):
        return self.meta_description.get("rpy", "geometry")

    def get_rpy_rad(self):
        return radians(self.get_rpy_deg()).tolist()

    def get_records(self):
        return self.meta_description.get_or("records", None, {})

    def get_bridge(self):
        return self.meta_description.get_or("bridge", None, {})


def load_meta_description(meta_description_file_path):
    return CameraMetaDescription(meta_description_file_path)


def get_sensor_specifications(meta_description):
    return romea_camera_description.get_camera_specifications(
        meta_description.get_type(), meta_description.get_model()
    )


def get_sensor_geometry(meta_description):
    return romea_camera_description.get_camera_geometry(
        meta_description.get_type(), meta_description.get_model()
    )


def get_complete_configuration(meta_description):
    return romea_camera_description.get_complete_configuration(
        meta_description.get_name(), meta_description.get_configuration()
    )


def driver_executable_parameters(executable, driver_configuration, camera_configuration, frame_id):
    parameters = driver_configuration
    parameters["frame_id"] = frame_id

    if executable == "usb_cam_node":
        parameters["framerate"] = camera_configuration("frame_rate")
        parameters["image_height"] = camera_configuration("image_height")
        parameters["image_width"] = camera_configuration("image_width")
    else:
        # TODO (add other drivers)
        pass

    return parameters


def urdf_description(robot_namespace, mode, meta_description_file_path):

    meta_description = CameraMetaDescription(meta_description_file_path)

    ros_namespace = device_namespace(
        robot_namespace,
        meta_description.get_namespace(), 
        meta_description.get_name()
    )

    return romea_camera_description.urdf(
        robot_urdf_prefix(robot_namespace),
        mode,
        meta_description.get_name(),
        meta_description.get_configuration(),
        meta_description.get_geometry(),
        ros_namespace,
    )
