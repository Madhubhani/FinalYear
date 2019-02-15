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


# for f in (files):
#     parse_pdf(f)


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


def finding_contours(image, canny_img):

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
        crop_img = image[y: (y+1) + h, x: (x+2) + (w-1)]

        dim = (26, 50)

        sized_image = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)

        letter = matching_letters(sized_image)


    print(letter)

    print("testing near plate")
    # cv2.imshow("Sized Image", sized_image)

    return letter


def matching_letters(cropped):


    s = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg',
         'A.jpg', 'B.jpg', 'C.jpg', 'D.jpg', 'E.jpg', 'F.jpg', 'G.jpg', 'H.jpg', 'I.jpg', 'J.jpg',
         'K.jpg', 'L.jpg', 'M.jpg', 'N.jpg', 'O.jpg', 'P.jpg', 'Q.jpg', 'R.jpg', 'S.jpg', 'T.jpg',
         'U.jpg', 'V.jpg', 'W.jpg', 'X.jpg', 'Y.jpg', 'Z.jpg']

    max_value = 1

    for i in s:

        #Load the image in gray scale
        template = cv2.imread(i)    ######,0

        res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        max_val = abs(max_val)

        #abs(max_val) gives the highest value
        if max_val > max_value:
            max_value = max_val
            letter = i[0]
    # print (max_val)s

    # if max_val > (5000000):
    #     print ("testing_1")
    #     return letter
    #
    # else:
    #     print ("testing_2")
    #     return ''
    return letter

def main():
    global original_image
    plate = ''

    d = ['data/30.jpg', 'data/31.jpg', 'data/32.jpg', 'data/33.jpg', 'data/34.jpg', 'data/35.jpg', 'data/36.jpg', 'data/37.jpg', 'data/38.jpg', 'data/39.jpg']
    for i in d:

        # image_name = arg_parser()
        original_image, gray_image, canny = processor(i)
        letter = finding_contours(original_image, canny)

        plate = plate + letter

        cv2.imshow("Original Image", original_image)
        cv2.imshow("Gray_Image", gray_image)
        cv2.imshow("Canny_Image", canny)
        # cv2.imshow("Rectangular_Image", rec_image)

    save_to_file(plate)
    print(plate)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
