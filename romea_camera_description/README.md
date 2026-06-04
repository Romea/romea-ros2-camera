# romea_camera_description

## 1) Overview

`romea_camera_description` provides configuration utilities and URDF descriptions for camera sensors.

It follows the same specification-based approach as the other ROMEA sensor description packages:

* user configuration identifies the camera model and optional overrides
* specification files provide default camera characteristics
* geometry files provide physical dimensions and inertial properties
* the Python API combines these inputs with the camera location on the robot
* xacro templates generate the camera URDF fragment, including simulation sensors when requested

This package is normally used by `romea_camera_meta_bringup`.

---

## 2) Camera description concept

A camera description is built from two user inputs:

| Input | Role |
|:------|:-----|
| camera configuration | manufacturer, model, version and optional camera stream settings |
| camera location | parent link and pose of the camera on the robot |

The configuration is completed with files from `config/`:

| File pattern | Content |
|:-------------|:--------|
| `<manufacturer>_<model>_<version>_specifications.yaml` | sensor type, frame rate, resolution, field of view and image format |
| `<manufacturer>_<model>_<version>_geometry.yaml` | geometry, mass and visual description used by URDF generation |
| `specifications_units.yaml` | units used when generating YAML configuration files |

The `xyz` values are expressed in meters. The `rpy` values are expressed in degrees in YAML files and converted to radians when generating URDF.

---

## 3) Configuration examples

### Monocular camera

```yaml
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
```

### Multi-component camera

Some cameras, such as RGB-D or stereo cameras, contain several image components. Each component can override the defaults defined in the specification file.

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

location:
  parent_link: base_link
  xyz: [1.0, 0.0, 1.2]
  rpy: [0.0, 0.0, 0.0]
```

---

## 4) URDF descriptions

The `urdf/` directory contains xacro templates for the supported camera families:

| Template | Camera family |
|:---------|:--------------|
| `monocular_camera.xacro` | monocular camera |
| `stereo_camera.xacro` | stereo camera |
| `rgbd_stereo_camera.xacro` | RGB-D stereo camera |
| `rgbd_infrared_stereo_camera.xacro` | RGB-D camera with infrared stereo pair |
| `rgbd_tof_camera.xacro` | RGB-D time-of-flight camera |

The generated URDF fragment contains:

* the camera base link attached to the configured parent link
* optical frames and component links when required by the camera family
* optional visual meshes and inertial properties from the geometry file
* Gazebo sensor descriptions when generated in simulation mode

The fragment is intended to be combined with the mobile base reference URDF and the other device URDF fragments by `romea_robot_meta_bringup`.

---

## 5) Python API

The Python module `romea_camera_description` provides the main helpers used by meta-bringup packages.

| Function | Role |
|:---------|:-----|
| `get_specifications(camera_description)` | load the specification file associated with the selected camera |
| `get_geometry(camera_description)` | load the geometry file associated with the selected camera |
| `get_complete_configuration(camera_name, camera_description, camera_location)` | merge user configuration, specifications and location |
| `generate_configuration_file(configuration, extended)` | generate a YAML configuration string |
| `generate_urdf_description(prefix, mode, camera_name, camera_description, camera_location, ros_namespace, standalone=False)` | generate the camera URDF fragment |

Example:

```python
from romea_camera_description import (
    generate_configuration_file,
    generate_urdf_description,
    get_complete_configuration,
)

camera_name = "front_camera"
camera_description = {
    "manufacturer": "axis",
    "model": "p1346",
    "version": "",
    "frame_rate": 30,
    "resolution": "1280x720",
}
camera_location = {
    "parent_link": "base_link",
    "xyz": [1.0, 0.0, 1.2],
    "rpy": [0.0, 0.0, 0.0],
}

configuration = get_complete_configuration(
    camera_name,
    camera_description,
    camera_location,
)

configuration_yaml = generate_configuration_file(configuration, extended=False)

urdf = generate_urdf_description(
    "robot_",
    "simulation_gazebo",
    camera_name,
    camera_description,
    camera_location,
    "/robot/cameras/front_camera",
)
```

---

## 6) Supported cameras

The package currently provides specification files for:

| Manufacturer | Model | Version | Camera family |
|:-------------|:------|:--------|:--------------|
| `axis` | `p1346` | `""` | monocular camera |
| `intel` | `realsense` | `d435` | RGB-D infrared stereo camera |
| `stereolabs` | `zed` | `1` | stereo camera |
| `stereolabs` | `zed` | `2` | stereo camera |
| `zed` | `x` | | stereo camera |

Support for additional camera models can be added by providing matching specification and geometry files in `config/`.



! ajouter une section qui décrit comment on ajoute une nouvelle Camera
