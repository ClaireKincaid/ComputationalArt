""" Computational Art Project"""
#Claire Kincaid
#February 17 2016

from random import *
from PIL import Image
from math import *

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
	#you can't write doctests for this... but I tested it and it works
    """
    depth = max_depth
    if min_depth == 0:
        depth = randint(0, max_depth)
    if depth == 0:
        if randint (1,2) == 1:
            return ["x"]
        else:
            return ["y"]
    i = randint(1, 6)
    if i == 1:
        return ["prod", build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth -1)]
    if i == 2:
        return ["avg", build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
    if i == 3:
        return ["cos_pi", build_random_function(min_depth - 1, max_depth - 1)]
    if i == 4:
        return ["sin_pi", build_random_function(min_depth - 1, max_depth - 1)]
    if i == 5:
        return ["cube_x", build_random_function(min_depth - 1, max_depth - 1)]
    if i == 6:
        return ["square_x", build_random_function(min_depth - 1, max_depth - 1)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value
        -I don't have any time to add more doctests but I've run this a ridiculous 
        amount of times while I was debugging.  It works. Trust me.  
        And the six people that I bothered to help me.       
    >>> evaluate_random_function(['x'], 1., 1.)
    1.0
    >>> evaluate_random_function(['y'], 1., 1.)
    1.0
    """
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y
    if f[0] == "prod":
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    if f[0] == "avg":
        return 0.5*(evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))
    if f[0] == "cos_pi":
        return cos(pi*(evaluate_random_function(f[1], x, y)))
    if f[0] == "sin_pi":
        return sin(pi*(evaluate_random_function(f[1], x, y)))
    if f[0] == "cube_x":
        return (evaluate_random_function(f[1], x, y))**3
    if f[0] == "square_x":
        return (evaluate_random_function(f[1], x, y))**2

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_span = input_interval_end - input_interval_start
    output_span = output_interval_end - output_interval_start
    valScaled = float(val - input_interval_start) / float(input_span)
    return output_interval_start + (valScaled * output_span)


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,11)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

# Create some computational art!
generate_art("myart.png")