import os
import Image
from flask import current_app


EXIV2_CMD = None
if 'OPENSHIFT_APP_UUID' in os.environ:
    EXIV2_CMD = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], "installs", "bin", "exiv2")
else:
    EXIV2_CMD = "D:\workspaces\joylin_openshift\exiv2-0.23-win\exiv2.exe"


def get_image_date(saved_filename="", filepath=""):
    # get saved file
    imagefile = os.path.join(filepath, saved_filename)
    if not os.path.exists(imagefile):
        return None

    # read Exif.Photo.DateTimeOriginal
    read_cmd = "%s -g Exif.Photo.DateTimeOriginal print -Pv %s" % (EXIV2_CMD, imagefile)
    # current_app.logger.info("read_cmd = %s" % (read_cmd))
    result = os.popen(read_cmd).read().strip()
    # current_app.logger.info("result = %s" % (result))
    if len(result) > 0:
        nums = result.replace(" ", ":").split(":")
        if len(nums) == 6:
            return "%s-%s-%s" % (nums[0], nums[1], nums[2])

    # read Exif.Image.DateTime
    read_cmd = "%s -g Exif.Image.DateTime print -Pv %s" % (EXIV2_CMD, imagefile)
    # current_app.logger.info("read_cmd = %s" % (read_cmd))
    result = os.popen(read_cmd).read().strip()
    # current_app.logger.info("result = %s" % (result))
    if len(result) > 0:
        nums = result.replace(" ", ":").split(":")
        if len(nums) == 6:
            return "%s-%s-%s" % (nums[0], nums[1], nums[2])

    # return today as defalt value
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_image_exif(saved_filename="", filepath=""):
    # get saved file
    imagefile = os.path.join(filepath, saved_filename)
    if not os.path.exists(imagefile):
        return None

    # read orientation
    read_cmd = "%s print -pt %s" % (EXIV2_CMD, imagefile)
    current_app.logger.info("read_cmd = %s" % (read_cmd))
    result = os.popen(read_cmd).read().strip()
    current_app.logger.info("result = %s" % (result))
    return  "<pre>%s</pre>" % (result)


def reset_orientation(saved_filename="", filepath=""):
    # get saved file
    imagefile = os.path.join(filepath, saved_filename)
    if not os.path.exists(imagefile):
        return False

    # read orientation
    read_cmd = "%s -g Exif.Image.Orientation print -Pv %s" % (EXIV2_CMD, imagefile)
    current_app.logger.info("read_cmd = %s" % (read_cmd))
    result = os.popen(read_cmd).read().strip()
    orientation = 1
    if len(result) > 0:
        orientation = int(result)
    current_app.logger.info("result = %s, orientation = %d" % (result, orientation))

    # open file
    im = Image.open(imagefile)
    mirror = None
    if orientation == 1:
        # Nothing
        mirror = im.copy()
    elif orientation == 2:
        # Vertical Mirror
        mirror = im.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        # Rotation 180
        mirror = im.transpose(Image.ROTATE_180)
    elif orientation == 4:
        # Horizontal Mirror
        mirror = im.transpose(Image.FLIP_TOP_BOTTOM)
    elif orientation == 5:
        # Horizontal Mirror + Rotation 270
        mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    elif orientation == 6:
        # Rotation 270
        mirror = im.transpose(Image.ROTATE_270)
    elif orientation == 7:
        # Vertical Mirror + Rotation 270
        mirror = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
    elif orientation == 8:
        # Rotation 90
        mirror = im.transpose(Image.ROTATE_90)

    # save transposed image
    filename, fileext = os.path.splitext(saved_filename)
    new_saved_filename = "%s.noexif%s" % (filename, fileext)
    imagefile = os.path.join(filepath, new_saved_filename)
    current_app.logger.info("save to file %s" % (imagefile))
    mirror.save(imagefile)

    # set_cmd = "%s -M'set Exif.Image.Orientation %d' %s" % (EXIV2_CMD, 2, imagefile)
    # result = os.popen(set_cmd).read()
    # print set_cmd

if __name__ == "__main__":
    reset_orientation("a.jpg", "d:\\")
    reset_orientation("1_a.jpg", "d:\\")
