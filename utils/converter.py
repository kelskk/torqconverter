import subprocess
from PIL import Image

IMAGE_FORMATS = [

    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "bmp",
    "tiff",
    "ico"

]

def ffmpeg_convert(

    input_file,

    output_file

):

    result = subprocess.run(

        [

            "ffmpeg",

            "-y",

            "-i",

            input_file,

            output_file

        ],

        stdout=
        subprocess.DEVNULL,

        stderr=
        subprocess.DEVNULL

    )

    if result.returncode != 0:

        raise Exception(
            "Erro ffmpeg"
        )


def image_convert(

    input_file,

    output_file,

    ext

):

    img = Image.open(
        input_file
    )

    if ext.lower() in [

        "jpg",
        "jpeg"

    ]:

        img = img.convert(
            "RGB"
        )

        img.save(

            output_file,

            "JPEG"

        )

    else:

        img.save(

            output_file,

            ext.upper()

        )


def convert_file(

    input_file,

    output_file,

    ext

):

    ext = ext.lower()

    if ext in IMAGE_FORMATS:

        image_convert(

            input_file,

            output_file,

            ext

        )

    else:

        ffmpeg_convert(

            input_file,

            output_file

        )
