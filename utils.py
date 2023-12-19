""" This file include:
1. Calculate the area of
2.
3.
"""
import cv2 as cv
import numpy as np
class Utils:
    @staticmethod
    def point2arr(pts):
        arr =[]
        for point in pts:
            arr.append((point.x,point.y))
        return arr

    @staticmethod
    def calculates_area(pts):
        """
        @type pts: [(x,y)]
        """
        # print(pts)
        # for point in pts:
        #     print(point[0], point[1])
        # get x and y in vectors
        x = [point[0] for point in pts]
        y = [point[1] for point in pts]
        # shift coordinates
        x_ = x - np.mean(x)
        y_ = y - np.mean(y)
        # calculate area
        correction = x_[-1] * y_[0] - y_[-1] * x_[0]
        main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
        return 0.5 * np.abs(main_area + correction)

    @staticmethod
    def crop_img(img, roi, is_poly=False):
        if not is_poly:
            return img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

    @staticmethod
    def mask_img(img, roi):
        vertices = roi


        mask = np.zeros_like(img)
        # poly_mask = cv.fillPoly(mask, np.int32([vertices]), 255)
        poly_mask = cv.fillPoly(mask, np.int32([vertices]), (255, 255, 255))
        # return img * poly_mask
        # print("shape: ", img.shape, " dtype: ", img.dtype)
        return cv.bitwise_and(img, mask, poly_mask)
