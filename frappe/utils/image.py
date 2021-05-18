# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import os
import cv2

def resize_images(path, maxdim=700):
	from PIL import Image
	size = (maxdim, maxdim)
	for basepath, folders, files in os.walk(path):
		for fname in files:
			extn = fname.rsplit(".", 1)[1]
			if extn in ("jpg", "jpeg", "png", "gif"):
				im = Image.open(os.path.join(basepath, fname))
				if im.size[0] > size[0] or im.size[1] > size[1]:
					im.thumbnail(size, Image.ANTIALIAS)
					im.save(os.path.join(basepath, fname))

					print("resized {0}".format(os.path.join(basepath, fname)))

def strip_exif_data(content, content_type):
	""" Strips EXIF from image files which support it.

	Works by creating a new Image object which ignores exif by
	default and then extracts the binary data back into content.

	Returns:
		Bytes: Stripped image content
	"""

	from PIL import Image
	import io

	original_image = Image.open(io.BytesIO(content))
	output = io.BytesIO()

	new_image = Image.new(original_image.mode, original_image.size)
	new_image.putdata(list(original_image.getdata()))
	new_image.save(output, format=content_type.split('/')[1])

	content = output.getvalue()

	return content

def image_resize(image, width=None, height=None, inter=None):
	if not inter:
		inter = cv2.INTER_AREA
	# initialize the dimensions of the image to be resized and
	# grab the image size
	dim = None
	(h, w) = image.shape[:2]

	# if both the width and height are None, then return the
	# original image
	if width is None and height is None:
		return image

	# check to see if the width is None
	if width is None:
		# calculate the ratio of the height and construct the
		# dimensions
		r = height / float(h)
		dim = (int(w * r), height)

	# otherwise, the height is None
	else:
		# calculate the ratio of the width and construct the
		# dimensions
		r = width / float(w)
		dim = (width, int(h * r))

	# resize the image
	resized = cv2.resize(image, dim, interpolation = inter)

	# return the resized image
	return resized