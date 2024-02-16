import sys
import asyncio
import numpy
import crop_utilities
import argparse

# 根据传入的媒体类型（图片或视频），下载对应的媒体文件。
def download_media(media_type, avcode_list, media_path="."):
    try:
        # 根据媒体类型选择相应的检查和下载函数
        if media_type == "img":
            check_func = crop_utilities.check_av_code_img
        else:
            check_func = crop_utilities.check_av_code_vdo 
        # 执行检查操作
        media_urls, existing_code, unexisting_avcode = asyncio.run(check_func(avcode_list))
        print(f"While Down Av-code: {existing_code}")
        if unexisting_avcode != []:
            print(f"NOT FOUND: {unexisting_avcode}")
        for media_url in media_urls:
            # 执行下载操作并返回文件名
            file_name = crop_utilities.download(media_url, media_path)
            yield file_name
    except Exception as e:
        # 处理异常情况
        print(f"Error processing {avcode_list}: {e}")
    # 验证媒体类型是否有效
    if media_type not in ["img", "vdo"]:
        print("Invalid media type. Please specify 'img' for image or 'vdo' for video.")
        return

# 主程序
if __name__ == "__main__":
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="cropper function(version 0.1.3)\nCopyright (c) 2024.2.03 the laowan7913 developers")

    # 添加参数选项
    parser.add_argument("-a", "--down_cut_img", nargs="+", action="append", help="auto to down cover_image and cut image for video.", metavar="avcode")
    parser.add_argument("-c", "--cut_img", nargs="+", help="cut image defualt_size for video.", metavar="input_image,[output_image]")
    parser.add_argument("-f", "--format_img", nargs=2, help="format image type.", metavar="input_image output_image")
    parser.add_argument("-d", "--download", nargs="+", help="download cover_image and pre_video.", metavar="avcode,[path]")
    parser.add_argument("-i", "--img_download", nargs = "+", help="download cover_image.", metavar="avcode,[path]")
    parser.add_argument("-v", "--vdo_download", nargs = "+", help="download pre-video.", metavar="avcode,[path]")
    parser.add_argument("-to", "--pre_download", nargs= 2, help="download pre-image or pre-video for last code", metavar="last_num")

    # 解析命令行参数
    args = parser.parse_args()

    # 获取命令行参数的值并进行相应的操作    
    # -a 下载图片并剪切
    if args.down_cut_img:
        # 把二维列表转换为一维列表([[]] -> [])
        avcode = list(numpy.array(args.down_cut_img).flatten())
        # 下载图片并剪切
        for filename in download_media("img",avcode):
            crop_utilities.crop_image([filename])

    # -d 下载图片或者视频
    if args.download:
        avcode = list(numpy.array(args.download).flatten())        
        list(download_media("img", avcode))        
        list(download_media("vdo", avcode))
        
    # -i 下载图片
    if args.img_download:
        avcode = list(numpy.array(args.img_download).flatten())        
        list(download_media("img", avcode))

    # -v 下载者视频
    if args.vdo_download:
        avcode = list(numpy.array(args.vdo_download).flatten())        
        list(download_media("vdo", avcode))
    
    # -to 下载预览
    if args.pre_download:
        avcode = list(numpy.array(args.pre_download).flatten())
        avcode_list = crop_utilities.get_avcode_list(avcode)
        list(download_media("img", avcode_list, "pre_downloads"))        
        list(download_media("vdo", avcode_list, "pre_downloads"))
    
    # -c 剪切图片
    if args.cut_img:
        filename = list(numpy.array(args.cut_img).flatten())
        crop_utilities.crop_image(filename)

    # -f 转换图片格式
    if args.format_img:
        filename = list(numpy.array(args.format_img).flatten())
        crop_utilities.convert_image(filename[0],filename[1])