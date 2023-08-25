import warnings
warnings.filterwarnings("ignore", message=r"Passing", category=FutureWarning)


from mrcnn.config import Config
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
    DETECTION_MIN_CONFIDENCE = 0.9