# USAGE python correct_skew.py --image images/neg_28.png

import numpy as np
import argparse, cv2
import imutils
from PIL import Image

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

    return image, blurred_image, edged_image


def save_to_file(letter):

    file = open('reader.txt','wt')

    file.write(letter + '\n')
    file.close()
    return file


def finding_contours(image, canny_img):

    (im2, contours, hierarchy) = cv2.findContours(canny_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:

        cv2.drawContours(image, contours, 0, 255, 0)

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
        cv2.imshow("Sized Image", sized_image)

    print letter
    save_to_file(letter)


def matching_letters(cropped):

    s = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg',
         'A.jpg', 'B.jpg', 'C.jpg', 'D.jpg', 'E.jpg', 'F.jpg', 'G.jpg', 'H.jpg', 'I.jpg', 'J.jpg',
         'K.jpg', 'L.jpg', 'M.jpg', 'N.jpg', 'O.jpg', 'P.jpg', 'Q.jpg', 'R.jpg', 'S.jpg', 'T.jpg',
         'U.jpg', 'V.jpg', 'W.jpg', 'X.jpg', 'Y.jpg', 'Z.jpg']

    min_value = 1

    for i in s:

        template = cv2.imread(i, 0)

        res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val < min_value:
            min_value = min_val
            letter = i[0]
        print min_val

    if min_value < (-5700000):
        print "testing_1"
        return letter

    else:
        print "testing_2"
        return ''


def main():
    global original_image
    image_name = arg_parser()
    original_image, gray_image, canny = processor(image_name)
    finding_contours(gray_image, canny)
    # file = save_to_file()
    # matching_letters(rec_image, file)

    cv2.imshow("Original Image", original_image)
    cv2.imshow("Gray_Image", gray_image)
    cv2.imshow("Canny_Image", canny)
    # cv2.imshow("Rectangular_Image", rec_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
