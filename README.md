# square_image_cropper

## Description
This code generates such square images with the power of 2 size from images of various sizes.

## Installation
Develop environment can be installed by:
```
make install_poetry
poetry install
```

## Usage
Put image files under the directory written in `cfg.yaml`,
then run: 
```
make main
```
After the process is completed,
square-sized images are output to the specified directory.

## Configulation
If you want to change the calculation conditions, edit the parameters described in　`./config/config.yaml`.
Each parameter is described below:

- path_to_image_directory: 
    - Path to the directory where the input image is stored.
- target_extension: 
    - Input image extension
- output_image_size: 
    - Size of output image; must be a power of 2.
    - If output image size is larger than input image, then crop in smaller size and resize in larger size with bicubic interpolation.
- output_directory: 
    - Path to the directory where the output image will be stored.
- output_extension: 
    - Output image extension.

## Motivations
When using images to create machine learning models, the training data is often required to be square images with a size power of two.
However, most datasets or the images we took are not in such a format.

This code easily prepares such required images with a single command.