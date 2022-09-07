import numpy as np
import sys
# import the models for further classification experiments
from tensorflow.keras.applications import (vgg19)
# from tensorflow.keras.applications import (mobilenet)

# init the models
vgg_model = vgg19.VGG19(weights='imagenet')
 
# inception_model = inception_v3.InceptionV3(weights='imagenet')
 
# resnet_model = resnet50.ResNet50(weights='imagenet')
 
# mobilenet_model = mobilenet.MobileNet(weights='imagenet')

import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
 
# assign the image path for the classification experiments
filename = f'../Data/Images/{sys.argv[1]}.png'
 
# load an image in PIL format
original = load_img(filename, target_size=(224, 224))
print('PIL image size',original.size)
 
# convert the PIL image to a numpy array
# IN PIL - image is in (width, height, channel)
# In Numpy - image is in (height, width, channel)
numpy_image = img_to_array(original)
print('numpy array size',numpy_image.shape)
 
# Convert the image / images into batch format
# expand_dims will add an extra dimension to the data at a particular axis
# We want the input matrix to the network to be of the form (batchsize, height, width, channels)
# Thus we add the extra dimension to the axis 0.
image_batch = np.expand_dims(numpy_image, axis=0)
print('image batch size', image_batch.shape)
plt.imshow(np.uint8(image_batch[0]))


# prepare the image for the VGG model
processed_image = vgg19.preprocess_input(image_batch.copy())
 
# get the predicted probabilities for each class
predictions = vgg_model.predict(processed_image)
# print predictions
# convert the probabilities to class labels
# we will get top 5 predictions which is the default
label_vgg = decode_predictions(predictions)
# print VGG19 predictions
for prediction_id in range(len(label_vgg[0])):
    print(label_vgg[0][prediction_id])

plt.imshow(original)
plt.show()
