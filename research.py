# USAGE python correct_skew.py --image images/neg_28.png

from __future__ import print_function
import numpy as np
import argparse, cv2
import imutils
from PIL import Image
import os

original_image = ""


def arg_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image file path")
    args = vars(ap.parse_args())
    return args["image"]


def processor(image):

    image = cv2.imread(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edged_image = cv2.Canny(blurred_image, 50, 200)

    return image, gray_image, edged_image


def save_to_file(letters):

    file = open('reader.txt','wt')
    file.write(letters)
    file.close()
    return file


def finding_contours(image, canny_img, count):

    (im2, contours, hierarchy) = cv2.findContours(canny_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print (contours)
    # plate = "T"
    if len(contours) != 0:

        # cv2.drawContours(image, contours, 0, 255, 0)

        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 1)

    if w/h > 1.5:
        letter = '-'


    else:
        x = x+1
        y = y+1
        w=w-2
        h=h-2
        crop_img = image[y: (y+2) + (h-1), x: (x+2) + (w-1)]
        # crop_img = image[y: (y-2) + (h-2), x: (x+2) + (w-2)]

        dim = (26, 50)

        sized_image = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)

        #Invert the colors of the image
        sized_image = (255 - sized_image)

        letter = matching_letters(sized_image)

        # cv2.imshow("Sized_Image_%d" %count, sized_image)
        # cv2.imwrite("Output/Sized_Image_%d.jpg" %count, sized_image)

    return letter


def matching_letters(cropped):

    s = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg',
         'A.jpg', 'B.jpg', 'C.jpg', 'D.jpg', 'E.jpg', 'F.jpg', 'G.jpg', 'H.jpg', 'I.jpg', 'J.jpg',
         'K.jpg', 'L.jpg', 'M.jpg', 'N.jpg', 'O.jpg', 'P.jpg', 'Q.jpg', 'R.jpg', 'S.jpg', 'T.jpg',
         'U.jpg', 'V.jpg', 'W.jpg', 'X.jpg', 'Y.jpg', 'Z.jpg', '10.jpg', '70.jpg', '#.jpg']

    max_value = 1

    for i in s:

        #Load the image in gray scale
        template = cv2.imread(i, 0)

        res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        #abs(max_val) gives the highest value
        if max_val > max_value:
            max_value = max_val
            letter = i[0]

    return letter


def main():
    global original_image
    plate = ''

    # d=['data1/3.jpg']

    # d = ['data1/1.jpg', 'data1/2.jpg', 'data1/3.jpg', 'data1/4.jpg', 'data1/5.jpg', 'data1/6.jpg', 'data1/7.jpg',
    #      'data1/8.jpg', 'data1/9.jpg']

    d = ['data2/0.jpg', 'data2/1.jpg', 'data2/2.jpg', 'data2/3.jpg', 'data2/4.jpg', 'data2/5.jpg', 'data2/6.jpg',
         'data2/7.jpg', 'data2/8.jpg', 'data2/9.jpg']

    # d = ['data3/0.jpg', 'data3/1.jpg', 'data3/2.jpg', 'data3/3.jpg', 'data3/4.jpg', 'data3/5.jpg', 'data3/6.jpg',
    #      'data3/7.jpg', 'data3/8.jpg']

    # d = ['data4/1.jpg', 'data4/2.jpg', 'data4/3.jpg', 'data4/4.jpg', 'data4/5.jpg', 'data4/6.jpg', 'data4/7.jpg',
    #      'data4/8.jpg', 'data4/9.jpg']

    # d = ['data5/1.jpg', 'data5/2.jpg', 'data5/3.jpg', 'data5/4.jpg', 'data5/5.jpg', 'data5/6.jpg', 'data5/7.jpg']

    count = 0

    for i in d:

        # image_name = arg_parser()
        original_image, gray_image, canny = processor(i)
        letter = finding_contours(gray_image, canny, count)

        plate = plate + letter

        # cv2.imwrite("Output/Gray_%d.jpg" %count, gray_image)
        # cv2.imwrite("Output/Canny_Image_%d.jpg" %count, canny)

        count=count+1

    save_to_file(plate)
    print(plate)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
