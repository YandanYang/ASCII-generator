"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from utils import get_data


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output text file")
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"],
                        help="background's color")
    parser.add_argument("--num_cols", type=int, default=300, help="number of character for output's width")
    args = parser.parse_args()
    return args


def main(opt):
    if opt.background == "white":
        bg_code = 255 # 如果背景为白色，像素值设置为 25
    else:
        bg_code = 0 # 如果背景为黑色，像素值设置为 0

    # 使用自定义函数 get_data 获取字符集（char_list）、字体对象（font）、示例字符（sample_character）和缩放比例（scale）
    char_list, font, sample_character, scale = get_data(opt.language, opt.mode)
    num_chars = len(char_list)  # 字符集的长度
    num_cols = opt.num_cols  # 输出的列数
    image = cv2.imread(opt.input)  # 读取输入图像
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    height, width = image.shape  # 获取图像的高度和宽度
    cell_width = width / opt.num_cols  # 每个字符块的宽度
    cell_height = scale * cell_width  # 每个字符块的高度（基于缩放比例）
    num_rows = int(height / cell_height)  # 计算字符块的行数

    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        # 如果列数或行数超过图像尺寸，使用默认设置
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    
    char_width, char_height = font.getsize(sample_character)
    # 获取每个字符的宽度和高度
    out_width = char_width * num_cols
    # 输出图像的宽度 = 单字符宽度 × 列数
    out_height = scale * char_height * num_rows
    # 输出图像的高度 = 单字符高度 × 缩放比例 × 行数

    out_image = Image.new("L", (out_width, out_height), bg_code)
    # 创建空白图像，模式为 "L"（灰度图），大小为 (out_width, out_height)
    draw = ImageDraw.Draw(out_image)  # 创建绘图对象

    for i in range(num_rows):  # 遍历每一行
        line = "".join([  # 构建当前行的字符串
            char_list[min(int(np.mean(image[
                int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width), width)
            ]) / 255 * num_chars), num_chars - 1)]  # 根据灰度值选择字符
            for j in range(num_cols)]) + "\n"
        draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)
        # 将字符行绘制到图像上，颜色与背景相反

    for i in range(num_rows):  # 遍历每一行
        line = "".join([  # 构建当前行的字符串
            char_list[min(int(np.mean(image[
                int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width), width)
            ]) / 255 * num_chars), num_chars - 1)]  # 根据灰度值选择字符
            for j in range(num_cols)]) + "\n"
        draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)
        # 将字符行绘制到图像上，颜色与背景相反


    if opt.background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
        # 如果背景为白色，将图像反转后获取非空边界
    else:
        cropped_image = out_image.getbbox()
        # 如果背景为黑色，直接获取非空边界

    out_image = out_image.crop(cropped_image)  # 裁剪图像
    out_image.save(opt.output)  # 保存输出图像



if __name__ == '__main__':
    opt = get_args()
    main(opt)
