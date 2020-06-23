from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD, Adam
from sklearn.metrics import classification_report
import numpy as np
import os
import split_folders
import argparse
import glob

from .GCP_Data_Handler import download_data_to_local_directory



def get_number_of_images_in_directory(directory):
    totalcount = 0
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in [".png", ".jpg", ".jpeg"]:
                totalcount += 1

    return totalcount


def get_number_of_classes(directory_of_images_folders):

    list_of_images_folders = glob.glob(os.path.join(directory_of_images_folders, '*'))
    nbr_classes = 0

    for directory in list_of_images_folders:
        if os.path.isdir(directory):
            nbr_classes += 1

    return nbr_classes



def run_training(bucket_name, username, task_name):

    #path_to_downloaded_data = os.path.join('./training_data/downloaded_data/data/classification/', username, task_name)
    path_to_downloaded_data = os.path.join('./training_data/downloaded_data')
    if not os.path.isdir(path_to_downloaded_data):
        os.makedirs(path_to_downloaded_data)
    print('path_to_downloaded_data : ', path_to_downloaded_data)

    # Download data
    print("Downloading data ...")
    download_data_to_local_directory(path_to_downloaded_data, bucket_name, username)
    print("Done downloading data.")

    path_to_splitted_data = os.path.join('./training_data/splitted_data/', username, task_name)
    if not os.path.isdir(path_to_splitted_data):
        os.makedirs(path_to_splitted_data)
    print('path_to_splitted_data : ', path_to_splitted_data)


    path_to_folders_of_images = os.path.join(path_to_downloaded_data, 'data/classification', username, task_name)

    nbr_classes = get_number_of_classes(path_to_folders_of_images)
    print('nbr_classes : ', nbr_classes)
    batch_size = 8


    split_folders.ratio(path_to_folders_of_images, output=path_to_splitted_data, seed=27, ratio=(.7, .15, .15))
    print("Done splitting data into train/val/test!")


    trainPath = os.path.join(path_to_splitted_data, 'train')
    if not os.path.isdir(trainPath):
        os.makedirs(trainPath)

    valPath = os.path.join(path_to_splitted_data, 'val')
    if not os.path.isdir(valPath):
        os.makedirs(valPath)

    testPath = os.path.join(path_to_splitted_data, 'test')
    if not os.path.isdir(testPath):
        os.makedirs(testPath)

    # determine the total number of image paths in training, validation,
    # and testing directories
    totalTrain = get_number_of_images_in_directory(trainPath)
    totalVal = get_number_of_images_in_directory(valPath)
    totalTest = get_number_of_images_in_directory(testPath)


    # initialize the training data augmentation object
    trainAug = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=30,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")

    # initialize the validation/testing data augmentation object (which
    # we'll be adding mean subtraction to)
    valAug = ImageDataGenerator(
        rescale=1. / 255,
    )

    # define the ImageNet mean subtraction (in RGB order) and set the
    # the mean subtraction value for each of the data augmentation
    # objects
    mean = np.array([123.68, 116.779, 103.939], dtype="float32")
    trainAug.mean = mean
    valAug.mean = mean

    # initialize the training generator
    trainGen = trainAug.flow_from_directory(
        trainPath,
        class_mode="categorical",
        target_size=(224, 224),
        color_mode="rgb",
        shuffle=True,
        batch_size=batch_size)

    # initialize the validation generator
    valGen = valAug.flow_from_directory(
        valPath,
        class_mode="categorical",
        target_size=(224, 224),
        color_mode="rgb",
        shuffle=False,
        batch_size=batch_size)

    # initialize the testing generator
    testGen = valAug.flow_from_directory(
        testPath,
        class_mode="categorical",
        target_size=(224, 224),
        color_mode="rgb",
        shuffle=False,
        batch_size=batch_size)


    # load the VGG16 network, ensuring the head FC layer sets are left off
    baseModel = InceptionV3(weights="imagenet", include_top=False,
        input_tensor=Input(shape=(224, 224, 3)))

    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(512, activation="relu")(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(nbr_classes, activation="softmax")(headModel)

    # place the head FC model on top of the base model (this will become
    # the actual model we will train)
    model = Model(inputs=baseModel.input, outputs=headModel)

    # loop over all layers in the base model and freeze them so they will
    # *not* be updated during the first training process
    for layer in baseModel.layers:
        layer.trainable = False

    # compile our model (this needs to be done after our setting our
    # layers to being non-trainable
    print("[INFO] compiling model...")
    #opt = SGD(lr=1e-4, momentum=0.9)
    opt = Adam(lr=1e-5)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
        metrics=["accuracy"])

    # train the head of the network for a few epochs (all other layers
    # are frozen) -- this will allow the new FC layers to start to become
    # initialized with actual "learned" values versus pure random
    print("[INFO] training head...")
    H = model.fit_generator(
        trainGen,
        steps_per_epoch=totalTrain // batch_size,
        validation_data=valGen,
        validation_steps=totalVal // batch_size,
        epochs=1)





    print("[INFO] evaluating after fine-tuning network...")
    testGen.reset()
    predIdxs = model.predict_generator(testGen,
                                       steps=(totalTest // batch_size) + 1)
    predIdxs = np.argmax(predIdxs, axis=1)
    print(classification_report(testGen.classes, predIdxs,
                                target_names=testGen.class_indices.keys()))

    print("Done training and testing!")
    #plot_training(H, 20, config.UNFROZEN_PLOT_PATH)
    print(H.history)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--bucket_name", type=str, help="bucket name from GCP buckets", default="neurify-bucket")
    parser.add_argument("--local_directory", type=str, help="local directory where downloaded data will be saved",
                        default="./deeplearning/downloaded_data")

    parser.add_argument("--username", type=str, help="Username in the backend.", default='stuned')
    parser.add_argument("--task_name", type=str, help="User's task name in the backend to fetch his/her data",
                        default='cats_and_dogs')

    args = parser.parse_args()

    run_training(args.bucket_name, args.username, args.task_name)


