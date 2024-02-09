# Larvae Counter User Guide

Welcome! This is a web-app that is equipped with a variety of tools to automate the counting
of mosquito larvae and pupae (although mostly pupae at this stage) from images. Currently, this
larvae counting tool has three automatic pupae counting tools based on "old-school" computer
vision techniques. However, a deep-learning method based off of the `YoloV8` architecture
is currently in development. Hypothetically, this deep learning method should be much less
susceptible to noise and allow the simultaneous counting of larvae and pupae, and maybe even
other stages of the mosquito life cycle. See below for a quick getting started guide.

## Workflow

Below is the general workflow used to count mosquito larvae present in an image.

### Step 1: Upload an Image

The first step is to upload an image containing pupae to be counted. This is done by either
clicking on or dragging an image file to the camera icon on the page. If this app is being
used on a smartphone an image can also be taken directly from the smartphone's camera by
tapping on the camera icon. After uploading an image, you can begin tunning parameters.

### Step 2: Parameter Tuning

The next step is select your counting method and begin tuning the counting parameters. The
counting method can be selected in the drop-down list below the image upload box. The 
`Gradient CC w/ filter` is recommended as the default counting algorithm. The parameters
for the selected counting method can be found in the box below the counting method drop-down
list.

It is recommend to click the `count` button with the default parameters to get a general
idea of how the parameters need to be changed in order to get better results. After changing
the parameters, click the `count` button again to re-run the selected algorithm with a new
set of parameters.

In general, parameters should be tuned from top down - meaning that the first parameter from the
top should be tuned to get satisfactory results, then the second parameter, and so on. The
images provided in the `Visualization` section of the results box (below the parameters box)
should be used to tune the parameters. More details will be given on each counting method and
its parameters below.

### Step 3: Check Results

After the parameters have been tuned, the final results are available in the results box - which
is situated just below the counting parameters box.

## Counting Algorithms

The larvae-count tool currently has three counting algorithms available, `Gradient CC w/ Filter`,
`Gradient CC`, and `Countour`. 

### Gradient CC w/ filter

`Gradient CC w/ Filter` (short for Gradient Connected Components with Elliptical Filter) counts
the pupae present in an image utilizing clusters. The algorithm first creates a gray scale image
from the provided image and applies a simple threshold in order to find pixels that are in a region
containing pupae. A filter is then applied to filter out any pixels flagged as pupae that aren't part
of a roughly elliptical pixel region. The algorithm than iterates over each overlapping cluster of 
pupae (hence the connected components) and calculated the number of pupae in each cluster by
the area of the cluster in pixels.

#### Parameters

- `Color Threshold`: Cutoff below which a pixel in the gray-scale image will be considered to be
    in a region containing pupae. The allowed values range from (0-255).
- `Average Area`: Average area (in pixels) of one pupae.
- `Max Pupae Per Cluster (Optional)`: Maximum number of pupae per cluster, used to filter out any
    large dark blobs in the image.
- `Filter Kernel Width (Pixels)`: Width (in pixels) of the elliptical filter.
- `Filter Kernel Height (Pixels)`: Height (in pixels) of the elliptical filter.

### Gradient CC

Same as `Gradient CC w/ Filter` but without the elliptical filter.

#### Parameters

- `Color Threshold`: Cutoff below which a pixel in the gray-scale image will be considered to be
    in a region containing pupae. The allowed values range from (0-255).
- `Average Area`: Average area (in pixels) of one pupae.
- `Max Pupae Per Cluster (Optional)`: Maximum number of pupae per cluster, used to filter out any
    large dark blobs in the image.

### Gradient Contour w/ Filter

Similar to `Gradient CC w/ Filter`, but instead of iterating over every blob of "pupae pixels"
it iterates over regions contained within (an) elliptical contour(s).

#### Parameters

- `Color Threshold`: Cutoff below which a pixel in the gray-scale image will be considered to be
    in a region containing pupae. The allowed values range from (0-255).
- `Average Area`: Average area (in pixels) of one pupae.
- `Max Pupae Per Cluster (Optional)`: Maximum number of pupae per cluster, used to filter out any
    large dark blobs in the image.
- `Filter Kernel Width (Pixels)`: Width (in pixels) of the elliptical filter.
- `Filter Kernel Height (Pixels)`: Height (in pixels) of the elliptical filter.

### YoloV8 (Coming Soon!!)

Deep learning implementation of the larvae/pupae counter. Not only should a deep learning
approach have far less parameters to tune, it should perform **much** better than the old-school
computer vision approaches currently in use.
