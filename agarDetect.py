
# Imports
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.config import Config
from mrcnn.model import MaskRCNN

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

import warnings
warnings.filterwarnings("ignore", message=r"Passing", category=FutureWarning)

# Paths
model_path = 'agar_cfg20221010T2320/mask_rcnn_agar_cfg_0004.h5'
data_path = 'agar2'


# define the prediction configuration
class PredictionConfig(Config):
    # define the name of the configuration
    NAME = "agar_cfg"
    # number of classes (background + kangaroo)
    NUM_CLASSES = 1 + 1
    # simplify GPU config
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MAX_INSTANCES = 1000
    POST_NMS_ROIS_INFERENCE = 8000

# draw an image with detected objects
def draw_image_with_boxes(filename, boxes_list):
     # load the image
     data = pyplot.imread(filename)
     # plot the image
     pyplot.imshow(data)
     # get the context for drawing boxes
     ax = pyplot.gca()
     # plot each box
     for box in boxes_list:
          # get coordinates
          y1, x1, y2, x2 = box
          # calculate width and height of the box
          width, height = x2 - x1, y2 - y1
          # create the shape
          rect = Rectangle((x1, y1), width, height, fill=False, color='red')
          # draw the box
          ax.add_patch(rect)
     # show the plot
     num_colonies = len(boxes_list)
     print('Number of colonies: ', num_colonies)
     pyplot.axis('off')
     pyplot.show()

 
# define the model
rcnn = MaskRCNN(mode='inference', model_dir='./', config=PredictionConfig())
# load coco model weights
rcnn.load_weights(model_path, by_name=True)

def detectResults(im_path):
    # load photograph
    img = load_img(im_path)
    img = img_to_array(img)
    # make prediction
    results = rcnn.detect([img], verbose=0)

    return results


results = detectResults('test.jpg')
# visualize the results
draw_image_with_boxes('test.jpg', results[0]['rois'])

print(results)