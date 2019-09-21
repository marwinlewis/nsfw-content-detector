#!/usr/bin/env python
import sys
import argparse
import tensorflow as tf

from open_nsfw.model import OpenNsfwModel, InputType
from open_nsfw.image_utils import create_tensorflow_image_loader
from open_nsfw.image_utils import create_yahoo_image_loader

import numpy as np
import json

IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"

MODEL_WEIGHTS = "open_nsfw/data/open_nsfw-weights.npy"

parser = argparse.ArgumentParser()

# parser.add_argument("input_file","--input",
#                     default=IMAGE_PATH,
#                     help="Path to the input image. Only jpeg images are supported.")

parser.add_argument("-m", "--model_weights",
                    default=MODEL_WEIGHTS,
                    help="Path to trained model weights file")

parser.add_argument("-l", "--image_loader",
                    default=IMAGE_LOADER_YAHOO,
                    help="image loading mechanism",
                    choices=[IMAGE_LOADER_YAHOO, IMAGE_LOADER_TENSORFLOW])

parser.add_argument("-i", "--input_type",
                    default=InputType.TENSOR.name.lower(),
                    help="input type",
                    choices=[InputType.TENSOR.name.lower(),
                            InputType.BASE64_JPEG.name.lower()])

args = parser.parse_args()

model = OpenNsfwModel()

def classify_nsfw(IMAGE_PATH):
    with tf.compat.v1.Session() as sess:
        input_type = InputType[args.input_type.upper()]
        model.build(weights_path=args.model_weights, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if args.image_loader == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(sess(graph=tf.Graph()))
            else:
                fn_load_image = create_yahoo_image_loader()
        elif input_type == InputType.BASE64_JPEG:
            import base64
            fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())

        image = fn_load_image(IMAGE_PATH)

        predictions = sess.run(model.predictions,
                    feed_dict={model.input: image})

        print("Results for '{}'".format(IMAGE_PATH))
        print("\tSFW score:\t{}\n\tNSFW score:\t{}".format(*predictions[0]))

        return ({
            'sfw': str(predictions[0][0]),
            'nsfw': str(predictions[0][1])
        })