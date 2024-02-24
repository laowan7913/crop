import re
import crop_utilities
# 定义AvCode类
class Av:
    def __init__(self, code):
        # 番号
        self._code = code
        # 用于缓存结果
        self._info = None    
        # 作品名称
        self._name = None
        # 主演
        self._actress = None
        # 发行日期
        self._date = None
        # 发行商
        self._av_maker = None
        # 封面图片
        self._img_pre_url = None
        # 作品图片
        self._preview_img_src = None
        # 预览视频
        self._vdo_pre_url = None

    # 返回番号
    @property
    def code(self):
        code = Av.get_code_pin(self._code) + "-" + Av.get_code_num(self._code)
        return code
    
    @property
    def info(self):
        if not self._info:
            self._info = crop_utilities.get_av_class(self._code)
        return self._info

    @property
    def name(self):
        return self.info[0]

    @property
    def date(self):
        return self.info[1]

    @property
    def av_maker(self):
        return self.info[2]
    
    @property
    def actress(self):
        return self.info[3]

    @property
    def cover_image_url(self):
        return self.info[4]

    @property
    def preview_img_src(self):
        return self.info[5]
    
    @classmethod    #获取番号字母
    def get_code_pin(cls, code):
        code_pin = "".join(re.findall("[a-z]", code.lower()))        
        return code_pin
    
    @classmethod    #获取番号数字
    def get_code_num(cls, code):
        code_num = "".join(re.findall(r"\d", code))
        return code_num
    
    def __str__(self):
        av = "AvCode:" + self.code + "\nAvName:" + self.name + "\nAvdate:" + self.date + "\nAvMaker:" + self.av_maker +"\nActress:" + ", ".join(self.actress)
            
        return av
    
if __name__ == "__main__":
    avcode = "ssis888"
    print(Av(avcode))