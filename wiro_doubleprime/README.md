# WIRO Double Prime PyRAF Reduction Script

#### Author: Jackson L. Cole
#### Affiliation: Middle Tennessee State University
#### 2017 University of Wyoming Astronomy REU

## ACKNOWLEDGEMENTS

Dr. Chip Kobulnicky:
- The overscan subtraction and trimming of overscan regions was adapted from a cl script written by Dr. Kobulnicky specifically for the WIRO Double Prime Imager.

David Kasper:
- The utc_update script used in this script was written by David in order to correct an issue found in the DATEOBS keyword in the FITS headers of WIRO images.

## Synopsis:
In a bash shell, and in a directory containing your
data, type

	python wirodoubleprimereductions.py

and follow all given instructions perfectly.

## Description:
`wirodoubleprimereductions.py` is a python script that
is used specifically for reductions of data produced
by the WIRO DoublePrime imager at the University of
Wyoming.

If the initial reductions you require for your data set
from raw to calibrated fits images OF SINGLE OR MULTIPLE
TARGETS FROM ONE NIGHT include:

- overscan subtraction and trimming (specific to the
DoublePrime imager)
- bias combination & subtraction
- dark combination & subtraction (or not)
- flat combination and flat fielding (with flats from
the night on which the uncalibrated science images
were taken OR flats from another night, which will be
transferred into the working directory in a directory
called 'otherflats'... instructions are given as
prompts during the initial script setup)
- calibrated science image combination
- rearrangement of science images based on target name

then this script should work for your purposes.

## Instructions:

Make sure that every numbered image from the night of
data is in the working directory (i.e.: if you took 30
images during the night, then the files present in the
directory should include:

	a001.fit
	a002.fit
	a003.fit
	.
	.
	.
	a028.fit
	a029.fit
	a030.fit

It is also critical that the images follow the naming
convention seen above!!

The initial script setup handles the images based on
several list files that are created in the working
directory. In other words, if you were to be missing
`a001.fit`, each image after `a001.fit` in the directory
would be named correctly, but would be handled as the
image before it. If you have images that you know should
not be used for whatever reason, these images should be
left in the working directory, but should be removed from
any list in which they appear.

You will first be asked to give the two or three digit
numbers corresponding to the first and last images of ANY
number of objects in between. This will generate the file
`object.list`, which will be a list of each image in the
range given by your responses. Please open this file in your
editor of choice (+1 for any vim users) to remove any images
from the list that ARE NOT object images or are not to be used
in the reductions (e.g.: bad images (for whatever reason),
mid-object-range target finding images, you name it) but DO
NOT remove these images from the working directory.

You will then be asked to enter the NUMBER OF OBJECTS OBSERVED
during the night of observing. At this point, you will then
be asked to enter the name of each object WITHOUT SPACES and
the range of images that correspond to that object. Again,
you will be allowed to edit these files before continuing.
They are each named with the naming convention

	object.#.targetname.list

You will then be asked to enter the range of images
corresponding to the bias frames. Again, if for whatever reason
there are breaks in this range, just enter the first and
last bias image number and edit the `bias.list` file that
is generated.

You will then be asked to enter the range of images
corresponding to the flat frames taken during the night.
Again, if for whatever reason there are breaks in this range,
just enter the first and last flat image number and edit the
`flat.list` file that is generated.

IN THE CASE OF FLATS FROM OTHER NIGHTS:
The directions are given by the script itself, but essentially,
you want to make sure first that the filter information is 100%
correct before doing anything else. Then, if you're feeling
proactive you should make a directory in the working directory
called `otherflats` into which you should then copy your flat
frames. You don't have to do this up front, as the script will
tell you what to do, create the directory if it doesn't exist,
etc.

You can also include any darks taken during the evening in the
same manner as above. Operating under the assumption that darks
were not taken during the night (due to exceptionally low dark
current in the DoublePrime CCD), you are given the option to
bypass any use of darks.

## What it does:

The script begins by changing the imagetype and ccdtype keywords
in the fits headers to reflect the type of image. It then
creates list files of flats and their corresponding filters.

Overscan subtraction is then done using a cl script written
by Dr. Chip Kobulnicky at the University of Wyoming, which
has been implemented in PyRAF.

A master bias frame is then created using `bias.list`, and then
is subtracted from each of the other frames in the directory.

Flats are then median combined (with avsigclip rejection and
median weighting) and in the case of errors arising from
the non existance of flats in certain filters, this operation
is simply passed.

The flats are then normalized based on the mean of the
unnormalized master flat images.

Each of the images are flat fielded using the normalized
master flats.

Then, in order to correct an issue with the UTC information in
the image headers, this script invokes another script
written by UW graduate student David Kasper, called
`utc_update.py`. This script is written specifically to solve
this issue.

After all images have been calibrated, the object images are
organized into directories based on the target names given in
the script setup, and then by filter within each target
directory. The convention is as follows:

	object.#.targetname/filter_*/image

## Potential issues:

As of right now, this script calls on other scripts which
are located (for the most part, I believe) in

	/d/www/jcole/public_html/scripts

If this directory is ever deleted, issues would definitely arise.
I would suggest that if this script ever gains any traction,
moving the files on which this script is dependent to the WIRO
directory or elsewhere, so long as the paths are changed to
correspond to these locations.

## Disclaimer:

It has come to my attention through my own interaction
with the finished, calibrated science images that from
time to time, some of the calibration frames get
organized into the target image directories as science
images. I would just use a cl script to display each
image and move images that are clearly NOT science images
into a donotuse directory. Otherwise, to my knowledge,
this is the only issue that has come up.
