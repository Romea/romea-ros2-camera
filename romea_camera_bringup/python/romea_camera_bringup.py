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
from romea_camera_description import get_camera_specifications, get_camera_geometry, urdf
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

    def get_driver_pkg(self):
        return self.meta_description.get("pkg", "driver")

    def get_type(self):
        return self.meta_description.get("type", "configuration")

    def get_model(self):
        return self.meta_description.get("model", "configuration")

    def get_frame_rate(self):
        return self.meta_description.get_or("frame_rate", "configuration", None)

    def get_resolution(self):
        return self.meta_description.get_or("resolution", "configuration", None)

    def get_horizontal_fov(self):
        return self.meta_description.get_or("horizontal_fov", "configuration", None)

    def get_video_format(self):
        return self.meta_description.get_or("video_format", "configuration", None)

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
    return get_camera_specifications(meta_description.get_type(), meta_description.get_model())


def get_sensor_geometry(meta_description):
    return get_camera_geometry(meta_description.get_type(), meta_description.get_model())


def urdf_description(robot_namespace, mode, meta_description_file_path):

    meta_description = CameraMetaDescription(meta_description_file_path)

    ros_namespace = device_namespace(robot_namespace, meta_description.get_namespace(), meta_description.get_name())

    configuration = {}
    configuration["frame_rate"] = meta_description.get_frame_rate()
    configuration["resolution"] = meta_description.get_resolution()
    configuration["horizontal_fov"] = meta_description.get_horizontal_fov()
    configuration["video_format"] = meta_description.get_video_format()

    geometry = {}
    geometry["parent_link"] = meta_description.get_parent_link()
    geometry["xyz"] = meta_description.get_xyz()
    geometry["rpy"] = meta_description.get_rpy_rad()

    return urdf(
        robot_urdf_prefix(robot_namespace),
        mode,
        meta_description.get_name(),
        meta_description.get_type(),
        meta_description.get_model(),
        configuration,
        geometry,
        ros_namespace,
    )
