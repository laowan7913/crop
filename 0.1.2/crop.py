import sys
import crop_utilities

# -help 的内容
help_text = """crop version 0.1.2_20240202 Copyright (c) 2024.1.29 the laowan7913 developers
     built with python3.12.1
usage: crop [options] [infile options]  [outfile options]
Getting help:
        -help   -- print crop function
Function options
        -a      -- crop -a avcode(eg:abc-123) to download cover_image and crop image for video. 
        -d      -- crop -d avcode(eg:abc-123) [image-path] to download cover_image.
        -i      -- crop -i input_image(eg:abc123pl.jpg) [-o ouput_image] to crop image for video.
        -f      -- crop -f input_image(eg:abc123.jpg) output_image(abc001.png) to format image type.
        -v      -- crop -v avcode(eg:abc-123) to download pre-video."""

#########################
#   处理argv各种命令      #
# -d -c -a -i           #
#########################  
                      
# argv -d 下载图片           
def argv_d(arg) -> str:
    # 获取命令行参数
    av_code = crop_utilities.get_argv(arg, 1)
    try:
        img_path = crop_utilities.get_argv(arg, 2)
    except:
        img_path = "."
    img_url = crop_utilities.get_img_url(av_code)
    file_name = crop_utilities.download(img_url, img_path)
    return file_name

# argv -i 剪切图片
def argv_i(arg) -> None:
    # 解析命令行参数
    input_image = crop_utilities.get_argv(arg, 1)
    #解析文件名
    input_image_left, _ = crop_utilities.get_file_name(input_image)
    _, input_image_right = crop_utilities.get_file_name(input_image)
    # -o 写output_image地址
    if "-o" in sys.argv:
        arg = "-o"
        output_image = crop_utilities.get_argv(arg, 1)
        _, output_image_right = crop_utilities.get_file_name(output_image)
        if input_image_right.lstrip(".") == output_image_right.lstrip("."):
            crop_utilities.crop_image(input_image, output_image)
        else:
            crop_utilities.convert_image(input_image,output_image)
            crop_utilities.crop_image(output_image,output_image)
    else:
        output_image = input_image_left+"_crop"+input_image_right
        # 剪切图片
        crop_utilities.crop_image(input_image, output_image)

# argv -f 转换图片格式
def argv_f(arg)-> None:
    # 解析命令行参数
    input_image = crop_utilities.get_argv(arg, 1)
    output_image = crop_utilities.get_argv(arg, 2)
    # 转换图片格式
    crop_utilities.convert_image(input_image,output_image)        

# argv -a 输入avcode 下载图片并剪切
def argv_a(arg) -> None:
    input_image = argv_d(arg)
    file_name_left, _ = crop_utilities.get_file_name(input_image)
    _, file_name_right = crop_utilities.get_file_name(input_image)
    output_image = file_name_left+"_crop"+file_name_right
        # 剪切图片
    crop_utilities.crop_image(input_image, output_image)

# argv -v 输入avcode 下载预览视频
def argv_v(arg) -> str:
    # 获取命令行参数
    av_code = crop_utilities.get_argv(arg, 1)
    try:
        vdo_path = crop_utilities.get_argv(arg, 2)
    except:
        vdo_path = "."
    vdo_url = crop_utilities.get_vdo_url(av_code)
    # 先下载mhb看是否存在
    try:
        vdo_rul_mhb = vdo_url + "_mhb_w.mp4"
        file_name = crop_utilities.download(vdo_rul_mhb, vdo_path)
    except:
        vdo_rul_dmb = vdo_url+"_dmb_w.mp4"
        file_name = crop_utilities.download(vdo_rul_dmb, vdo_path)
    return file_name

# argv -help 查看crop命令
def argv_help(arg) -> None:
    print(help_text)

# 主函数
if __name__ == "__main__":
    
    # 定义命令和对应的处理函数,dict可以存储函数
    commands = {
    "-d": (argv_d, [3, 4]),
    "-i": (argv_i, [3, 5]),
    "-f": (argv_f, [4]),
    "-a": (argv_a, [3]),
    "-v": (argv_v, [3, 4]),
    "-help": (argv_help, [2])
}
    
    # 检查参数数量是否正确
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        sys.exit(crop_utilities.print_erorr(1))

    # 获取命令
    command = sys.argv[1]
    if command not in commands:
        sys.exit(crop_utilities.print_erorr(1))

    # 检查参数数量是否正确并执行命令
    if len(sys.argv) not in commands[command][1]:
        sys.exit(crop_utilities.print_erorr(1))

    # 执行命令
    try:
        commands[command][0](command)
    except ValueError:
        sys.exit(crop_utilities.print_erorr(1))