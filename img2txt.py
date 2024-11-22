"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse

import cv2
import numpy as np

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.txt", help="Path to output text file")
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--num_cols", type=int, default=150, help="number of character for output's width")
    args = parser.parse_args()
    return args


def main(opt):
    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '  # 如果模式为 "simple"，定义使用的 ASCII 字符集合（10 个字符）
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        # 如果模式为 "complex"，定义更复杂的字符集合（70 个字符）

    num_chars = len(CHAR_LIST)  # 计算字符集合的长度
    num_cols = opt.num_cols  # 获取字符列数（宽度）
    
    image = cv2.imread(opt.input)  # 读取输入图像
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度图
    height, width = image.shape  # 获取图像的高度和宽度
    
    cell_width = width / opt.num_cols  # 每个字符块的宽度（像素数）
    cell_height = 2 * cell_width  # 每个字符块的高度是宽度的 2 倍，保证纵横比接近
    num_rows = int(height / cell_height)  # 计算字符行数
    
    # 检查列数或行数是否超过图像尺寸，如果是，则调整参数
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")  # 提示参数过多，使用默认设置
        cell_width = 6  # 默认每个字符块宽度为 6 像素
        cell_height = 12  # 默认每个字符块高度为 12 像素
        num_cols = int(width / cell_width)  # 更新列数
        num_rows = int(height / cell_height)  # 更新行数
    
    output_file = open(opt.output, 'w')  # 打开输出文件，用于写入 ASCII 艺术
    
    # 遍历每个字符块
    for i in range(num_rows):
        for j in range(num_cols):
            # 计算当前字符块内像素的平均灰度值，并将其映射到字符集合中的字符
            avg_gray = np.mean(image[
                int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width), width)
            ])
            # 根据灰度值找到对应的字符
            char_idx = min(int(avg_gray * num_chars / 255), num_chars - 1)
            output_file.write(CHAR_LIST[char_idx])  # 写入字符到文件中
        output_file.write("\n")  # 每行结束后换行
    output_file.close()  # 关闭文件
