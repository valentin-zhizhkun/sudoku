"""Digit recognition"""
import os
from PIL import Image
import numpy as np
from sklearn import neighbors as knn
from sklearn.model_selection import KFold
from collections import defaultdict
import pickle
import zlib

from image import shrink_vertically


DIGIT_BITMAP_SIZE = 16
MODEL_FILE = os.path.join(os.path.dirname(__file__), 'model.dat')
_CLASSIFIER = None

def extend_vertically(a, pixels):
    top = pixels // 2
    bottom = pixels - top
    width = a.shape[1]
    return np.concatenate((
        np.full((top, width), True),
        a,
        np.full((bottom, width), True)
    ))


def resize_bitmap(a, height, width):
    im = Image.fromarray(a).resize((width, height))
    return np.asarray(im)


def reshape_bitmap(a):
    # Crop out white margins
    a, _ = shrink_vertically(a, 0)
    a = np.transpose(shrink_vertically(np.transpose(a), 0)[0])
    # Extend into a square
    diff = a.shape[0] - a.shape[1]
    if diff < 0:
        a = extend_vertically(a, -diff)
    elif diff > 0:
        a = np.transpose(extend_vertically(np.transpose(a), diff))
    return resize_bitmap(a, DIGIT_BITMAP_SIZE, DIGIT_BITMAP_SIZE)


def read_image(fname):
    im = Image.open(fname)
    bitmap = im.convert('1')  # Monochrome bitmap
    a = np.asarray(bitmap)
    a = reshape_bitmap(a)
    return a, bitmap


def read_image_set(basedir='data/digits'):
    """Read dataset for training/evaluating 1-9 digit recognition model"""
    instances = []
    classes = []
    bitmaps = []
    for digit in range(1, 10):
        dirname = os.path.join('data/digits', str(digit))
        for fname in [os.path.join(dirname, f) for f in os.listdir(dirname)]:
            a, bitmap = read_image(fname)
            instances.append(a.flatten())
            classes.append(digit)
            bitmaps.append(bitmap)
    return np.array(instances), np.array(classes), bitmaps


def get_classifier():
    return knn.KNeighborsClassifier(5, weights='distance')


def train_model(output_file='model.dat'):
    instances, classes, bitmaps = read_image_set()
    c = get_classifier()
    c.fit(instances, classes)
    with open(output_file, 'wb') as f:
        f.write(zlib.compress(pickle.dumps(c)))


def load_model(file=MODEL_FILE):
    with open(file, 'br') as f:
        return pickle.loads(zlib.decompress(f.read()))


def initialize_predictor():
    global _CLASSIFIER
    _CLASSIFIER = load_model()


def predict(a):
    """Identify a 1-9 digit given a bitmap array"""
    a = reshape_bitmap(a)
    instance = a.flatten()
    result = _CLASSIFIER.predict([instance])
    return result[0]

def evaluate_classifier():
    """Evaluate digit bitmap classifier using cross-validation"""
    instances, classes, bitmaps = read_image_set()
    kfold = KFold(5, shuffle=True)
    accuracies = []
    confusion = defaultdict(int)
    test_instance_cnt = 0
    for train, test in kfold.split(instances):
        c = get_classifier()
        c.fit(instances[train], classes[train])
        predictions = c.predict(instances[test])
        accuracy = np.sum(predictions == classes[test]) / len(test)
        accuracies.append(accuracy)
        test_instance_cnt += len(test)
        for i, error in enumerate(test):
            if predictions[i] != classes[error]:
                confusion[classes[error], predictions[i]] += 1
                #if (predictions[i], classes[error]) == (2, 7):
                #    bitmaps[error].show()
                #    input()

    accuracies = np.array(accuracies)
    print('Accuracy: {} +- {}'.format(accuracies.mean(), accuracies.std()))
    print('Top errors:',
          [(err, cnt/test_instance_cnt)
           for err, cnt in sorted(confusion.items(), key=lambda x: -x[1])]
          )

# train_model()
# evaluate_classifier()