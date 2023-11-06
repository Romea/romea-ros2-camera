# 1 Overview #

This package contains the description of camera sensors used in romea projects

# 2 Package organization #

This package is organized into subdirectories as follows:

  - config/ contains characteristic description of following camera:

    - axis
    - TODO add others cameras

  - python/ contains romea_camera_description python module able to create camera URDF description according their xacro representations and required parameters given by user

  - urdf/ contains (xacro representations of) urdf descriptions of supported cameras.
