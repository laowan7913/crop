usage: crop.py [-h] [-a avcode [avcode ...]] [-c input_image,[output_image] [input_image,[output_image] ...]]
               [-f input_image output_image input_image output_image] [-d avcode,[path] [avcode,[path] ...]] [-i avcode,[path]
               [avcode,[path] ...]] [-v avcode,[path] [avcode,[path] ...]] [-to last_num last_num]

cropper function(version 0.1.3) Copyright (c) 2024.2.03 the laowan7913 developers

options:
  -h, --help            show this help message and exit
  -a avcode [avcode ...], --down_cut_img avcode [avcode ...]
                        auto to down cover_image and cut image for video.
  -c input_image,[output_image] [input_image,[output_image] ...], --cut_img input_image,[output_image] [input_image,[output_image] ...]     
                        cut image defualt_size for video.
  -f input_image output_image input_image output_image, --format_img input_image output_image input_image output_image
                        format image type.
  -d avcode,[path] [avcode,[path] ...], --download avcode,[path] [avcode,[path] ...]
                        download cover_image and pre_video.
  -i avcode,[path] [avcode,[path] ...], --img_download avcode,[path] [avcode,[path] ...]
                        download cover_image.
  -v avcode,[path] [avcode,[path] ...], --vdo_download avcode,[path] [avcode,[path] ...]
                        download pre-video.
  -to last_num last_num, --pre_download last_num last_num
                        download pre-image or pre-video for last code
