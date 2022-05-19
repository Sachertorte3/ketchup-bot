import sys
from PIL import Image
from keras.models import load_model
import numpy as np

def classify(image):
    # name = sys.argv[1]
    # image = Image.open(name)
    image = image.resize((64, 64))
    image.show()

    model = load_model("model.h5")
    np_image = np.array(image)
    np_image = np_image / 255
    np_image = np_image[np.newaxis, :, :, :]
    result = model.predict(np_image)
    

    if result[0][0] > result[0][1]:
        print("ketch")
        a = result[0][0]
        print(a * 100 , "%")
    else:
        print("mayo")
        a = result[0][1]
        print(a * 100 , "%")

def ketch_check(image):
    image = image.resize((64, 64))
    image.show()

    model = load_model("model.h5")
    np_image = np.array(image)
    np_image = np_image / 255
    np_image = np_image[np.newaxis, :, :, :]
    result = model.predict(np_image)

    if result[0][0] > result[0][1]:
        print("OK")
        return False  
    else:
        return True

def ketch_probability(image):
    image = image.resize((64, 64))
    image.show()

    model = load_model("model.h5")
    np_image = np.array(image)
    np_image = np_image / 255
    np_image = np_image[np.newaxis, :, :, :]
    result = model.predict(np_image)

    if result[0][0] > result[0][1]:
        a = result[0][0] * 100
        return a 
    else:
        return 0
        

if __name__ == "__main__":
    pass