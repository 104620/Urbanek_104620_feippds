"""This module implements solution for converting image to grayscale using GPU and CPU with CUDA and numba technology.
"""

__author__ = "Paljko Urbanek, Marian Šebeňa, Tomáš Vavro"
__email__ = "xurbanek@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

import numpy as np
import matplotlib.pyplot as plt
from numba import cuda, jit
from datetime import datetime


@cuda.jit
def grayscale_gpu(img, gray):
    """Converting RGB image to grayscale. GPU method
    Args:
        img -- input image as NumPy array
        gray -- output grayscale image
    """
    x, y = cuda.grid(2)
    if x < img.shape[1] and y < img.shape[0]:
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        gray[y, x] = 0.299 * r + 0.587 * g + 0.114 * b


@jit
def grayscale_cpu(img, gray):
    """Converting RGB image to grayscale. CPU method
    Args:
        img -- input image as NumPy array
        gray -- output grayscale image
    """
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            gray[y, x] = 0.299 * r + 0.587 * g + 0.114 * b


def transform_to_gray_scale(pixels):
    """Transform pixels to grayscale picture
    Args:
        pixels -- input image as NumPy array
    """
    # GPU conversion
    if cuda.is_available():
        # Set up CUDA grid and block dimensions
        threads_per_block = (32, 32)
        blocks_per_grid_x = (pixels.shape[1] + threads_per_block[0] - 1) // threads_per_block[0]
        blocks_per_grid_y = (pixels.shape[0] + threads_per_block[1] - 1) // threads_per_block[1]
        blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

        # Allocate device memory for input and output images
        d_rgb_img = cuda.to_device(pixels)
        d_gray_img = cuda.device_array(shape=pixels.shape[:2], dtype=np.float32)

        # Launch the kernel function
        grayscale_gpu[blocks_per_grid, threads_per_block](d_rgb_img, d_gray_img)

        # Copy the output grayscale image back to the host
        gray_img = d_gray_img.copy_to_host()
    # CPU conversion
    else:
        gray_img = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=np.float32)
        grayscale_cpu(pixels, gray_img)

    return gray_img


def main():
    """Run main."""
    while True:
        print("Is cuda available: " + str(cuda.is_available()))
        picture_name = input("Input picture name: ")
        try:
            method_prefix = "_cpu"
            if cuda.is_available():
                method_prefix = "_gpu"
            pixels = plt.imread(picture_name + ".jpg")
            start_time = datetime.now()
            new_pixels = transform_to_gray_scale(pixels)
            plt.imsave(picture_name + "_gray" + method_prefix + ".jpg", new_pixels, cmap="gray", format="jpg")

            print("\nFinished gray_scaling process!")
            end_time = datetime.now()
            timer = end_time - start_time
            print('Total time: {}'.format(timer)+"\n")
        except FileNotFoundError:
            print("Wrong picture name name! Try again\n")


if __name__ == "__main__":
    main()
