import re
import sys
import requests
import os
import ffmpeg
from tqdm import tqdm
import imageio
from PIL import Image


# 定义AvCode类
class Av:
    def __init__(self, code, name=None, actress=None, date=None, dist=None,img_pre_url=None, vdo_pre_url=None):
        # 番号
        self._code = code  
        # 作品名称
        self._name = name
        # 主演
        self._actress = actress
        # 发行日期
        self._date = date
        # 发行商
        self._dist = dist
        # 封面图片
        self._img_pre_url = img_pre_url
        # 预览视频
        self._vdo_pre_url = vdo_pre_url

    @property
    def code(self):
        return self._avcode    

    @classmethod    #获取番号字母
    def get_code_pin(cls, code):
        code_pin = "".join(re.findall("[a-z]", code.lower()))        
        return code_pin
    
    @classmethod    #获取番号数字
    def get_code_num(cls, code):
        code_num = "".join(re.findall(r"\d", code.lower()))
        return code_num
    
    def __str__(self):
        av = Av.get_code_pin(self._avcode) + Av.get_code_num(self._code)
        return f"{av}"


# 设置全局变量
# 大多数可下载
av_code_common = {"soe", "snis", "ssni", "ssis","sone", "midv", "mide", "mifd", "mimk",
                    "miab", "ipzz", "ipx", "ipz", "iptd", "juq", "jux", "jul", "juy", "hmn",
                    "roe", "cawd", "kawd", "same", "adn", "atid", "rbk", "meyd", "mdyd",
                    "ebwh", "ebod"}
# Prestige
av_code_prestige = {"abf", "abw", "abs", "abp", "chn", "yrh", "tre", "fir", "tus", "ppt", "evo"}
# S1
av_code_sod = {"stars", "star", "sdnm", "sply", "sdab", "mogi"}
# other
av_code_3 = {"clot"}
# pre-video URL前缀
vdo_urlbase = "https://cc3001.dmm.co.jp/litevideo/freepv/"
# image URL前缀
img_urlbase = "https://pics.dmm.co.jp/mono/movie/adult/"


# convert 转换图片格式函数
def convert_image(input_image, output_image):
    try:
        # 读取图片文件
        image = imageio.v3.imread(input_image)        
        # 转换图片格式
        imageio.v3.imwrite(output_image, image)
        print(f"Image converted successfully to format and saved as {output_image}")
    except Exception as e:
        sys.exit(print(f"Failed to convert image: {str(e)}"))

# crop 剪切图片函数
def crop_image(input_image,output_image="."):
    try:
       # 打开图片
        image = Image.open(input_image)
        # 剪切图片
        cropped_image = image.crop((420, 0, 800, 538))        
        # 保存图片
        cropped_image.save(output_image)
        print(f"Image cropped and saved to {output_image}")
    except Exception as e:
        sys.exit(print(f"Failed to crop image: {str(e)}"))

# download 函数
def download(url, folder="."):
    try:
        # 创建目标文件夹（如果不存在）
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 提取 URL 中的文件名
        file_name = os.path.basename(url)        
        # 检查目标文件是否已经存在
        file_path = os.path.join(folder, file_name)
        if os.path.exists(file_path):
            print(f"File {file_name} already exists in the folder.")
            return file_name
        # 发送请求，获取文件数据
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        total_size = int(response.headers.get('content-length', 0))  # 文件总大小
        # 使用 tqdm 创建进度条
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        # 保存文件
        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
            # 更新进度条
                progress_bar.update(len(data))
                file.write(data)
        # 关闭进度条
        progress_bar.close()
        print(f"File {file_name} downloaded successfully and saved as {file_path}")
        return file_name        
    except Exception as e:        
        sys.exit(print(f"Failed to download file: {str(e)}"))

def get_img_url(av_code):
    # 解析AVpin 返回字母和数字
    av_code_c = Av.get_code_pin(av_code)
    av_code_n = Av.get_code_num(av_code)
    # 设置AVCODE-LIST
    global img_urlbase, av_code_common, av_code_prestige, av_code_sod, av_code_3
    # 组合image 地址
    if av_code_c in av_code_common:
        img_url = img_urlbase + av_code_c + av_code_n + "/" + av_code_c + av_code_n + "pl.jpg"
    elif av_code_c in av_code_prestige:
        img_url = img_urlbase + "118" + av_code_c + av_code_n + "/" + "118" + av_code_c + av_code_n + "pl.jpg"
    elif av_code_c in av_code_sod:
        img_url = img_urlbase + "1" + av_code_c + av_code_n + "/" + "1" + av_code_c + av_code_n + "pl.jpg"
    elif av_code_c in av_code_3:
        img_url = img_urlbase + "h_237" + av_code_c + av_code_n + "/h_237" + av_code_c + av_code_n + "pl.jpg"
    else:
        sys.exit(print("Unable to download pre-images of this AV code."))
    return img_url

def get_vdo_url(av_code):
    # 解析AVpin 返回字母和数字
    av_code_c = Av.get_code_pin(av_code)
    av_code_n = Av.get_code_num(av_code)
    # 设置AVCODE-LIST
    global vdo_urlbase, av_code_common, av_code_prestige, av_code_sod, av_code_3   
    # 组合pre-video 地址
    if av_code_c in av_code_common:
        # 设置url参数
        one_code = av_code_c[:1]
        one_three_code = av_code_c[:3]
        av_code_00 = av_code_c + "00" + av_code_n
        # 组合url 
        vdo_url = vdo_urlbase + one_code +"/"+ one_three_code +"/"+ av_code_00 +"/"+ av_code_00
    # S1
    elif av_code_c in av_code_sod:
        # 设置url参数
        av_sod_code = "1" + av_code_c + av_code_n
        one_code= av_sod_code[:1]
        one_three_code = av_sod_code[:3] 
        # 组合url
        vdo_url = vdo_urlbase + one_code +"/"+ one_three_code +"/"+ av_sod_code +"/"+ av_sod_code
    # Prestige  
    elif av_code_c in av_code_prestige:
        # 设置url参数
        av_prestige_code = "118" + av_code_c + av_code_n
        one_code= av_prestige_code[:1]
        one_three_code = av_prestige_code[:3] 
        # 组合url
        vdo_url = vdo_urlbase + one_code +"/"+ one_three_code +"/"+ av_prestige_code +"/"+ av_prestige_code
    else:
        sys.exit(print("Unable to download pre-video of this AV code."))
    return vdo_url

# 获取文件名左边名称与文件格式(包含点)
def get_file_name(file_name):
    file_name_left = os.path.splitext(os.path.basename(file_name))[0]
    file_name_right = os.path.splitext(os.path.basename(file_name))[1]
    return file_name_left, file_name_right

# 获取argv参数-arg 后的值 n=1 参数后第一位的值，n=2: 参数后第二位的值
def get_argv(arg,n):
    arg_parameter = sys.argv.index(arg) + n
    arg_value = sys.argv[arg_parameter]
    return arg_value

# 输入参数错误提示
def print_erorr(n):
    match n:
        case 1:
            print("Usage: Invalid input parameters. Type 'crop -help' to see more about the function for crop.")
        case 2:
            print("Usage: Invalid input parameters")

# ffmpeg 合并视屏
def merge_videos(video_list, output_file):
    # 创建一个ffmpeg合并器
    ffmpeg_concat = ffmpeg.concat(*[ffmpeg.input(video) for video in video_list])

    # 执行合并操作
    ffmpeg_concat.output(output_file).run()