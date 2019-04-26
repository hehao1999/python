"""
    GPS实习数据录入---图片识别与制表
"""
import cv2
import csv
import threading
import tesserocr
from PIL import Image

img_base_path = r'./imgs/  ({img_id}).jpg'

csv_file = open('data.csv', 'w', encoding='gb2312', newline='')
writer = csv.writer(csv_file)
writer.writerow(['ID', 'N', 'E', 'Z', 'sigmaN', 'sigmaE', 'sigmaZ', 'aim_high'])


def ocr(a, b):
    """
    识别影像
    :param a: 起始编号
    :param b: 结束编号
    :return:
    """
    for i in range(a, b):
        img = cv2.imread(img_base_path.format(img_id=i))

        # 选取图片识别区域，从上到下多少行，从左到右到多少列
        N = img[380:470, 140:530]
        E = img[470:550, 140:530]
        Z = img[550:640, 140:430]
        sigmaN = img[380:470, 680:910]
        sigmaE = img[470:550, 680:910]
        sigmaZ = img[550:640, 680:910]
        # point_id = img[680:770, 270:400]

        #  ************测试图像截取是否正确***************
        # cv2.namedWindow("roi")
        # cv2.imshow("roi", point_id)
        # cv2.waitKey(0)

        # 数组转为image对象
        N = Image.fromarray(N)
        E = Image.fromarray(E)
        Z = Image.fromarray(Z)
        sigmaN = Image.fromarray(sigmaN)
        sigmaE = Image.fromarray(sigmaE)
        sigmaZ = Image.fromarray(sigmaZ)
        # point_id = Image.fromarray(point_id).convert('L')

        # 识别结果
        N_TEMP = tesserocr.image_to_text(N).strip().replace('.', '').replace(' ', '')
        N = N_TEMP[0:7] + '.' + N_TEMP[7:]  # 也可以先转化为为二值图像后使用参数OEM=2直接识别小数点，但速度太慢
        E_TEMP = tesserocr.image_to_text(E).strip()
        E = N_TEMP[0:6] + '.' + N_TEMP[6:]
        Z = tesserocr.image_to_text(Z).strip()
        sigmaN = tesserocr.image_to_text(sigmaN).strip()
        sigmaE = tesserocr.image_to_text(sigmaE).strip()
        sigmaZ = tesserocr.image_to_text(sigmaZ).strip()
        # point_id = tesserocr.image_to_text(point_id).strip()
        point_id = str(i).zfill(3)
        # 写入文件
        print([point_id, N, E, Z, sigmaN, sigmaE, sigmaZ, 2.0])
        writer.writerow([point_id, N, E, Z, sigmaN, sigmaE, sigmaZ, 2.0])


def main():
    """主函数"""
    t1 = threading.Thread(target=ocr, args=(1, 60))  # 起始文件编号（1开始计数，结束文件编号+1）
    t2 = threading.Thread(target=ocr, args=(60, 113))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    csv_file.close()


if __name__ == '__main__':
    main()
