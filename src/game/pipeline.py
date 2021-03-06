import cv2
import numpy
import math
from enum import Enum

class GripPipeline:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__rgb_threshold_0_red = [71.08812949640289, 144.0358361774744]
        self.__rgb_threshold_0_green = [0.0, 33.93508463474335]
        self.__rgb_threshold_0_blue = [0.0, 25.035250112041922]

        self.rgb_threshold_0_output = None

        self.__cv_erode_0_src = self.rgb_threshold_0_output
        self.__cv_erode_0_kernel = None
        self.__cv_erode_0_anchor = (-1, -1)
        self.__cv_erode_0_iterations = 1.0
        self.__cv_erode_0_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_0_bordervalue = (-1)

        self.cv_erode_0_output = None

        self.__cv_dilate_0_src = self.cv_erode_0_output
        self.__cv_dilate_0_kernel = None
        self.__cv_dilate_0_anchor = (-1, -1)
        self.__cv_dilate_0_iterations = 1.0
        self.__cv_dilate_0_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_0_bordervalue = (-1)

        self.cv_dilate_0_output = None

        self.__find_contours_0_input = self.cv_dilate_0_output
        self.__find_contours_0_external_only = False

        self.find_contours_0_output = None


        self.__rgb_threshold_1_red = [87.85071942446044, 235.0]
        self.__rgb_threshold_1_green = [71.79856115107913, 135.0]
        self.__rgb_threshold_1_blue = [120.14388489208633, 255.0]

        self.rgb_threshold_1_output = None

        self.__cv_erode_1_src = self.rgb_threshold_1_output
        self.__cv_erode_1_kernel = None
        self.__cv_erode_1_anchor = (-1, -1)
        self.__cv_erode_1_iterations = 2.0
        self.__cv_erode_1_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_1_bordervalue = (-1)

        self.cv_erode_1_output = None

        self.__cv_dilate_1_src = self.cv_erode_1_output
        self.__cv_dilate_1_kernel = None
        self.__cv_dilate_1_anchor = (-1, -1)
        self.__cv_dilate_1_iterations = 2.0
        self.__cv_dilate_1_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_1_bordervalue = (-1)

        self.cv_dilate_1_output = None

        self.__find_contours_1_input = self.cv_dilate_1_output
        self.__find_contours_1_external_only = False

        self.find_contours_1_output = None


    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step RGB_Threshold0:
        self.__rgb_threshold_0_input = source0
        (self.rgb_threshold_0_output) = self.__rgb_threshold(self.__rgb_threshold_0_input, self.__rgb_threshold_0_red, self.__rgb_threshold_0_green, self.__rgb_threshold_0_blue)
        # cv2.imshow('frame',self.rgb_threshold_0_output)

        # Step CV_erode0:
        self.__cv_erode_0_src = self.rgb_threshold_0_output
        (self.cv_erode_0_output) = self.__cv_erode(self.__cv_erode_0_src, self.__cv_erode_0_kernel, self.__cv_erode_0_anchor, self.__cv_erode_0_iterations, self.__cv_erode_0_bordertype, self.__cv_erode_0_bordervalue)

        # Step CV_dilate0:
        self.__cv_dilate_0_src = self.cv_erode_0_output
        (self.cv_dilate_0_output) = self.__cv_dilate(self.__cv_dilate_0_src, self.__cv_dilate_0_kernel, self.__cv_dilate_0_anchor, self.__cv_dilate_0_iterations, self.__cv_dilate_0_bordertype, self.__cv_dilate_0_bordervalue)

        # Step Find_Contours0:
        self.__find_contours_0_input = self.cv_dilate_0_output
        (self.find_contours_0_output) = self.__find_contours(self.__find_contours_0_input, self.__find_contours_0_external_only)

        # Step RGB_Threshold1:
        self.__rgb_threshold_1_input = source0
        (self.rgb_threshold_1_output) = self.__rgb_threshold(self.__rgb_threshold_1_input, self.__rgb_threshold_1_red, self.__rgb_threshold_1_green, self.__rgb_threshold_1_blue)
        # cv2.imshow('frame', self.rgb_threshold_1_output)

        # Step CV_erode1:
        self.__cv_erode_1_src = self.rgb_threshold_1_output
        (self.cv_erode_1_output) = self.__cv_erode(self.__cv_erode_1_src, self.__cv_erode_1_kernel, self.__cv_erode_1_anchor, self.__cv_erode_1_iterations, self.__cv_erode_1_bordertype, self.__cv_erode_1_bordervalue)

        # Step CV_dilate1:
        self.__cv_dilate_1_src = self.cv_erode_1_output
        (self.cv_dilate_1_output) = self.__cv_dilate(self.__cv_dilate_1_src, self.__cv_dilate_1_kernel, self.__cv_dilate_1_anchor, self.__cv_dilate_1_iterations, self.__cv_dilate_1_bordertype, self.__cv_dilate_1_bordervalue)

        # Step Find_Contours1:
        self.__find_contours_1_input = self.cv_dilate_1_output
        (self.find_contours_1_output) = self.__find_contours(self.__find_contours_1_input, self.__find_contours_1_external_only)


    @staticmethod
    def __rgb_threshold(input, red, green, blue):
        """Segment an image based on color ranges.
        Args:
            input: A BGR numpy.ndarray.
            red: A list of two numbers the are the min and max red.
            green: A list of two numbers the are the min and max green.
            blue: A list of two numbers the are the min and max blue.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        return cv2.inRange(out, (red[0], green[0], blue[0]),  (red[1], green[1], blue[1]))

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __cv_dilate(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of higher value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for dilation. A numpy.ndarray.
           iterations: the number of times to dilate.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after dilation.
        """
        return cv2.dilate(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours



