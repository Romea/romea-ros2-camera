# romea_camera_meta_bringup

## 1) Overview

`romea_camera_meta_bringup` provides tools to describe, generate and launch camera sensors using the ROMEA meta-description workflow.

It is built on top of `romea_common_meta_bringup` and specializes the generic sensor workflow for cameras.

From a camera meta-description, the package can generate:

* a camera configuration file
* a camera URDF fragment
* a YAML launch file that starts camera drivers or simulation bridges

The camera specifications and URDF templates are provided by `romea_camera_description`.

---

## 2) Camera meta-description

### 2.1 Concept

A camera meta-description centralizes the information required to integrate a camera into a robot system:

* camera name and namespace
* camera manufacturer, model, version and stream overrides
* camera location on the robot
* launch description for live drivers and simulation bridges
* optional record configuration

The meta-description does not contain the full camera specification or geometry. These details are selected from `romea_camera_description` according to the `configuration` section.

### 2.2 Format

```yaml
name: camera
namespace: sensors

configuration:
  manufacturer: axis
  model: p1346
  version: ""
  frame_rate: 30
  resolution: 1280x720

location:
  parent_link: base_link
  xyz: [1.0, 0.0, 1.2]
  rpy: [0.0, 0.0, 0.0]

launch:
  - include:
      file: "$(find-pkg-share romea_camera_meta_bringup)/profile/usb_cam.launch.py"
      arg:
        - name: device
          value: /dev/video0
      if: $(eval "'$(var mode)' == 'live'")
  - include:
      file: "$(find-pkg-share romea_camera_meta_bringup)/profile/gz_bridge.launch.py"
      arg:
        - name: container
          value: /gz_container
      if: $(eval "'$(var mode)' == 'simulation_gazebo'")

records:
  image_raw: true
  camera_info: false
```

For multi-component cameras, stream overrides can be provided per component:

```yaml
configuration:
  manufacturer: intel
  model: realsense
  version: d435
  rgb_camera:
    frame_rate: 15
    resolution: 640x480
  depth_camera:
    frame_rate: 30
    resolution: 640x480
  infrared_camera:
    frame_rate: 60
    resolution: 640x480
```

`xyz` is expressed in meters and `rpy` in degrees.

---

## 3) Generated artifacts

### 3.1 Generate configuration file

```bash
ros2 run romea_camera_meta_bringup generate_configuration_file.py \
  meta_description_file_path:path/to/camera_meta_description.yaml \
  extended:false
```

This command generates a complete camera configuration by combining:

* the meta-description configuration section
* the camera specification file from `romea_camera_description`
* the camera location

Example output for a monocular camera:

```yaml
model: p1346
version: ''
manufacturer: axis
type: monocular_camera
frame_rate: 30
image_width: 1280
image_height: 720
image_format: yuyv
horizontal_fov: 72.0
parent_link: base_link
xyz: [1.0, 0.0, 1.2]
rpy: [0.0, 0.0, 0.0]
```

### 3.2 Generate URDF description

```bash
ros2 run romea_camera_meta_bringup generate_urdf_description.py \
  robot_namespace:robot \
  meta_description_file_path:path/to/camera_meta_description.yaml \
  mode:simulation_gazebo
```

The generated URDF fragment defines how the camera is attached to the robot. Depending on the camera family, it contains the camera base link, optical frames, component links and, in simulation mode, Gazebo camera sensors.

Example output, simplified:

```xml
<link name="robot_camera_link">
  ...
</link>

<joint name="robot_camera_joint" type="fixed">
  <parent link="robot_base_link"/>
  <child link="robot_camera_link"/>
  <origin xyz="1.0 0.0 1.2" rpy="0.0 0.0 0.0"/>
</joint>

<link name="robot_camera_optical_frame"/>

<gazebo reference="robot_camera_link">
  <sensor name="robot_camera" type="camera">
    ...
  </sensor>
</gazebo>
```

This URDF fragment can be combined with the mobile base reference URDF and the other device URDF fragments by `romea_robot_meta_bringup`.

### 3.3 Generate launch file

```bash
ros2 run romea_camera_meta_bringup generate_launch_file.py \
  robot_namespace:robot \
  meta_description_file_path:path/to/camera_meta_description.yaml
```

The generated YAML launch file:

* pushes the robot, camera namespace and camera name namespaces
* exposes configuration values as `let` variables
* includes the launch entries declared in the meta-description

---

## 4) Launch files

The package provides two main launch files:

| Launch file | Role |
|:------------|:-----|
| `camera.launch.py` | dynamically generates and includes the camera launch file from a camera meta-description |
| `simulation_test.launch.py` | starts a simulator, spawns the camera entity and starts the camera simulation bridge |

Reusable launch files are stored in `profile/`:

| File | Role |
|:--------|:-----|
| `usb_cam.launch.py` | start a USB camera driver |
| `realsense2_camera.launch.py` | start an Intel RealSense camera driver |
| `gz_bridge.launch.py` | bridge simulated Gazebo camera topics to ROS2 |

The selected files are included from the `launch` section of the camera meta-description. This keeps live driver choices and simulation bridge choices outside the robot-level description.

---

## 5) Usage

### Dynamic bringup

```bash
ros2 launch romea_camera_meta_bringup camera.launch.py \
  mode:=live \
  robot_namespace:=robot \
  meta_description_file_path:=path/to/camera_meta_description.yaml
```

`camera.launch.py` loads the camera meta-description, generates a YAML launch file in `/tmp` and includes it with the selected `mode`.

### Simulation test

```bash
ros2 launch romea_camera_meta_bringup simulation_test.launch.py \
  simulator_type:=gazebo \
  robot_namespace:=robot \
  meta_description_file_path:=path/to/camera_meta_description.yaml
```

This launch file:

* starts the simulator through `romea_simulation_meta_bringup`
* generates and spawns the camera URDF as a standalone entity
* starts `camera.launch.py` in `simulation_<simulator_type>` mode

---

## 6) Supported cameras

The supported camera models are defined by the specification and geometry files provided by `romea_camera_description`.

| Manufacturer | Model | Version | Camera family |
|:-------------|:------|:--------|:--------------|
| `axis` | `p1346` | `""` | monocular camera |
| `intel` | `realsense` | `d435` | RGB-D infrared stereo camera |
| `stereolabs` | `zed` | `1` | stereo camera |
| `stereolabs` | `zed` | `2` | stereo camera |
| `zed` | `x` | | stereo camera |

Support for additional camera models can be added in `romea_camera_description`.

---

## 7) Supported ROS2 drivers and bridges

The package currently provides reusable launch files for:

| File | Runtime | Role |
|:-----|:--------|:-----|
| `usb_cam.launch.py` | live | start a USB camera through `usb_cam` |
| `realsense2_camera.launch.py` | live | start an Intel RealSense camera through `realsense2_camera` |
| `gz_bridge.launch.py` | simulation | bridge Gazebo camera topics to ROS2 |

Other camera drivers can be used by adding a dedicated launch file and referencing it from the `launch` section of the camera meta-description.
