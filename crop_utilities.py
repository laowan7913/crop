import re
import sys
import magic
import requests
import os
import asyncio
import aiohttp
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
        code_num = "".join(re.findall(r"\d", code))
        return code_num
    
    def __str__(self):
        av = Av.get_code_pin(self._avcode) + Av.get_code_num(self._code)
        return f"{av}"


# 设置全局变量
# 大多数可下载
av_code_common = {"soe", "snis", "ssni", "ssis","sone", "midv", "mide", "mifd", "mimk", "mizd",
                    "miab", "ipzz", "ipx", "ipz", "iptd", "juq", "jux", "jul", "juy", "hmn",
                    "roe", "cawd", "kawd", "same", "adn", "atid", "rbk", "meyd", "mdyd",
                    "pgd", "pred"}
# Prestige
av_code_prestige = {"abf", "abw", "abs", "abp", "chn", "yrh", "tre", "fir", "tus", "ppt", "sga"}
# S1 & Faleno
av_code_sod = {"start", "stars", "star", "sdnm", "sdmm", "sply", "sdjs", "sdde", "sdab", "mogi", 
               "sw", "suwk"}
av_code_faleno = {"fsdss"}
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
def crop_image(input_image,output_path="."):
    for image_path in input_image:
        try:
        # 打开图片
            image = Image.open(image_path)
            # 剪切图片
            cropped_image = image.crop((420, 0, 800, 538))        
            # 分解图片文件名           
            filename_left, filename_right = get_file_name(image_path)
            output_image_name = filename_left + "_crop" + filename_right
            # 保存图片
            ouput_image = os.path.join(output_path, output_image_name)
            cropped_image.save(ouput_image)
            print(f"Image {image_path} cropped and saved to {ouput_image}")
        except Exception as e:
            sys.exit(print(f"Failed to crop image: {str(e)}"))

# download 函数
def download(url, folder="."):
    try:
        # 创建目标文件夹（如果不存在）
        os.makedirs(folder, exist_ok=True)
        # 提取 URL 中的文件名
        file_name = os.path.basename(url)
        # 构造文件保存路径
        file_path = os.path.join(folder, file_name)
        # 检查目标文件是否已经存在
        if os.path.exists(file_path):
            print(f"File {file_name} already exists in the folder.")
            return file_name
        # 发送请求，获取文件数据
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        total_size = int(response.headers.get('content-length', 0))  # 文件总大小
        # 使用 tqdm 创建进度条
        with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
            # 保存文件
            with open(file_path, 'wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    # 更新进度条
                    progress_bar.update(len(data))
                    file.write(data)
        print(f"File {file_name} downloaded successfully and saved as {file_path}")
        return file_name
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

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
    elif av_code_c in av_code_faleno:
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
    # faleno
    elif av_code_c in av_code_faleno:
        # 设置url参数
        av_faleno_code = "1" + av_code_c + av_code_n
        one_code= av_faleno_code[:1]
        one_three_code = av_faleno_code[:3] 
        # 组合url
        vdo_url = vdo_urlbase + one_code +"/"+ one_three_code +"/"+ av_faleno_code +"/"+ av_faleno_code
    # Prestige  
    elif av_code_c in av_code_prestige:
        # 设置url参数
        av_prestige_code = "118" + av_code_c + av_code_n
        one_code= av_prestige_code[:1]
        one_three_code = av_prestige_code[:3] 
        # 组合url
        vdo_url = vdo_urlbase + one_code +"/"+ one_three_code +"/"+ av_prestige_code +"/"+ av_prestige_code
    else:
        sys.exit(print_erorr(3))
    return vdo_url

# 获取文件名左边名称与文件格式(包含点)
def get_file_name(file_name):
    file_name_left = os.path.splitext(os.path.basename(file_name))[0]
    file_name_right = os.path.splitext(os.path.basename(file_name))[1]
    return file_name_left, file_name_right

# 根据abc-110 -120自动生成包含所有番号的list
def get_avcode_list(avcode_list):
    av_pin = Av.get_code_pin(avcode_list[0])
    av_start_num = int(Av.get_code_num(avcode_list[0]))
    av_end_num = int(Av.get_code_num(avcode_list[1]))
    
    # 确定数字范围和步长
    start, end = min(av_start_num, av_end_num), max(av_start_num, av_end_num)
    step = 1
    # 生成AV号列表
    av_list = [f"{av_pin}-{num:03d}" for num in range(start, end + step, step)]
    return av_list

# 输入参数错误提示
def print_erorr(n):
    match n:
        case 1:
            print("Usage: Invalid input parameters. Type 'crop -help' to see more about the function for crop.")
        case 2:
            print("Usage: Download Erorr!")
        case 3:
            print("Unable to download file of this AV code.")

# 检查图片番号url是否存在
async def check_av_code_img(avcode):
    # 存储存在的番号的列表
    existing_code_url = []
    existing_avcode = []
    unexisting_avcode = []
    async def check_url(session, code):
        url = get_img_url(code)
        try:
            async with session.head(url) as response:
                av_code = Av.get_code_pin(code) + "-" + Av.get_code_num(code)
                if response.status == 200:
                    existing_avcode.append(av_code)
                    existing_code_url.append(url)
                else:
                    unexisting_avcode.append(av_code)
        except aiohttp.ClientError as e:
            # 可以根据实际需求进行错误处理
            print(f"Error checking URL {url}: {e}")
    async with aiohttp.ClientSession() as session:
        tasks = [check_url(session, code) for code in avcode]
        await asyncio.gather(*tasks)
    return existing_code_url, existing_avcode, unexisting_avcode if existing_code_url else False

# 检查视频番号url是否存在
async def check_av_code_vdo(avcode):
    existing_code_url = []
    existing_avcode = []
    unexisting_avcode = []
    async def check_url(session, code, suffix):
        # 检查给定后缀的视频链接是否存在。        
        url = get_vdo_url(code) + suffix
        try:
            async with session.head(url) as response:
                av_code = Av.get_code_pin(code) + "-" + Av.get_code_num(code)
                if response.status == 200:
                    existing_code_url.append(url)
                    existing_avcode.append(av_code)
                    return True
                else:
                    return False
        except aiohttp.ClientError as e:
            print(f"Error checking URL {url}: {e}")
            return False
        
    async with aiohttp.ClientSession() as session:
        for code in avcode:
            suffixes = ["_hhb_w.mp4","_mhb_w.mp4", "_dmb_w.mp4"]
            existing = False  # 用于标记是否已经找到存在的视频
            for suffix in suffixes:
                if await check_url(session, code, suffix):
                    existing = True
                    # 一旦找到存在的视频，立即跳出内部循环
                    break
            if not existing:
                av_code = Av.get_code_pin(code) + "-" + Av.get_code_num(code)
                unexisting_avcode.append(av_code)            
    return existing_code_url, existing_avcode, unexisting_avcode if existing_code_url else False

# 找到各种类型的文件(图片类型,视频类型,文本类型等),返回文件名称，文件路径，文件类型的字典。
def get_file(folder_path,file_type):
    # 创建 Magic 实例
    mime = magic.Magic(mime=True)
    found_files = {}
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_name = filename
        file_path = os.path.join(folder_path, filename)
        # 判断是否为文件
        if os.path.isfile(file_path):
            # 获取文件类型
            filetype = mime.from_file(file_path)
            if file_type in filetype:
                found_files[filename] = {
                    "file_path": file_path,
                    "file_type": filetype
                }
    return found_files

# ffmpeg 合并视屏
def merge_videos(video_list, output_file):
    # 创建一个ffmpeg合并器
    ffmpeg_concat = ffmpeg.concat(*[ffmpeg.input(video) for video in video_list])

    # 执行合并操作
    ffmpeg_concat.output(output_file).run()

def add_cover_img(input_vdo, input_img, output_vdo):
    # 使用 ffmpeg 添加封面
    ffmpeg.input(input_img, loop=1, t=3).output(output_vdo).run(overwrite_output=True)