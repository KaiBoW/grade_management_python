import random
import string
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

def generate_captcha():
    # 生成随机验证码
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choices(chars, k=4))
    
    # 创建图片
    width = 120
    height = 40
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 设置字体
    try:
        # 尝试使用 Windows 系统字体
        font_path = 'C:/Windows/Fonts/Arial.ttf'
        if not os.path.exists(font_path):
            font_path = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑
        font_size = 28
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        # 如果找不到系统字体，使用默认字体
        font = ImageFont.load_default()
    
    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(169, 169, 169))  # 使用深灰色
    
    # 添加干扰点
    for i in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(169, 169, 169))  # 使用深灰色
    
    # 添加文字
    for i, char in enumerate(code):
        x = 15 + i * 25
        y = random.randint(2, 8)
        # 随机文字颜色
        color = (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )
        # 随机旋转角度
        angle = random.randint(-30, 30)
        # 创建单个字符的图片
        char_img = Image.new('RGBA', (30, 40), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((5, 5), char, font=font, fill=color)
        # 旋转字符
        char_img = char_img.rotate(angle, expand=True)
        # 粘贴到主图片
        image.paste(char_img, (x, y), char_img)
    
    # 转换为base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    b64_data = base64.b64encode(buffer.getvalue()).decode()
    
    return code, f"data:image/png;base64,{b64_data}" 