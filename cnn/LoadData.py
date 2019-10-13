import numpy as np
from keras.preprocessing.image import *
from sklearn.model_selection import train_test_split

class LoadData:
    img_rows, img_cols = 50, 30
    seed = 23
    np.random.seed(seed)
    folder_data_train = "D:/Projects/Python/PycharmProjects/OMR/cnn/data_training/"
    folder_data_test = "D:/Projects/Python/PycharmProjects/OMR/cnn/data_testing/"
    folder_data_test_sheet = "D:/Projects/Python/PycharmProjects/OMR/cnn/data_testing_sheet/"

    def loadDataTrain(self):
        x = []
        y = []

        datagen = ImageDataGenerator(rescale=1./255)
        train_generator = datagen.flow_from_directory(self.folder_data_train,
                                                      target_size=(self.img_rows, self.img_cols),
                                                      color_mode="grayscale",
                                                      batch_size=1,
                                                      class_mode="categorical",
                                                      shuffle=True,
                                                      seed=self.seed)

        batch_index = 0
        while batch_index <= train_generator.batch_index:
            a, b = train_generator.next()
            x.append(a[0])
            y.append(b[0])
            batch_index = batch_index + 1

        x = np.asarray(x)
        y = np.asarray(y)

        x_train, x_vald, y_train, y_vald = train_test_split(x, y, test_size=0.2, random_state=0)

        return train_generator, x_train, y_train, x_vald, y_vald

    def loadDataTest(self, folder):
        x_test = []

        datagen = ImageDataGenerator(rescale=1. / 255)
        test_generator = datagen.flow_from_directory(folder,
                                                     target_size=(self.img_rows, self.img_cols),
                                                     color_mode="grayscale",
                                                     batch_size=1,
                                                     class_mode=None,
                                                     shuffle=False,
                                                     seed=self.seed)

        batch_index = 0
        while batch_index <= test_generator.batch_index:
            z = test_generator.next()
            x_test.append(z[0])
            batch_index = batch_index + 1

        x_test = np.asarray(x_test)

        return test_generator, x_test




