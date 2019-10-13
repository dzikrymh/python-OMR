# Import Dependencies
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras import optimizers

# Create Class CNN
class CNN:

    def __init__(self, input_shape, nb_classes, lr):
        self.input_shape = input_shape
        self.nb_classes = nb_classes
        self.lr = lr

    def set_input_shape(self, input_shape):
        self.input_shape = input_shape

    def set_nb_classes(self, nb_classes):
        self.nb_classes = nb_classes

    def set_lr(self, lr):
        self.lr = lr

    def get_input_shape(self):
        print(self.input_shape)

    def get_nb_classes(self):
        print(self.nb_classes)

    def get_lr(self):
        print(self.lr)

    def my_model(self):
        # Setting
        pool_size = (3, 3)  # size of pooling area for max pooling
        prob_drop_conv = 0.25  # drop probability for dropout @ conv layer
        prob_drop_hidden = 0.3  # drop probability for dropout @ fc layer

        # Architecture Convolutional Neural Network In Sequence Process
        model = Sequential()

        # Conv1 Layer
        model.add(Conv2D(64,
                         (3, 3),
                         padding='same',
                         activation='relu',
                         input_shape=self.input_shape,
                         kernel_initializer="glorot_uniform"))

        # Pooling1 Layer
        model.add(MaxPooling2D(pool_size=pool_size,
                               strides=(2, 2),
                               padding='same'))

        # Conv2 Layer
        model.add(Conv2D(128,
                         (3, 3),
                         padding='same',
                         activation='relu',
                         kernel_initializer="glorot_uniform"))

        # Pooling2 Layer
        model.add(MaxPooling2D(pool_size=pool_size,
                               strides=(2, 2),
                               padding='same'))

        # Conv3 Layer
        model.add(Conv2D(256,
                         (3, 3),
                         padding='same',
                         activation='relu',
                         kernel_initializer="glorot_uniform"))

        # Pooling3 Layer
        model.add(MaxPooling2D(pool_size=pool_size,
                               strides=(2, 2),
                               padding='same'))

        # FC Input Layer || Flatten Layer
        model.add(Flatten())
        model.add(Dropout(prob_drop_conv))

        # FC1 Layer || Hidden Layer
        model.add(Dense(7168,
                        activation='relu',
                        kernel_initializer="glorot_uniform",
                        bias_initializer="zeros"))
        model.add(Dropout(prob_drop_hidden))

        # FC2 Layer Using Activation Softmax
        model.add(Dense(self.nb_classes, activation='softmax'))

        # Setting Optimizers
        adam = optimizers.Adam(lr=self.lr,
                               beta_1=0.9,
                               beta_2=0.999,
                               epsilon=None,
                               decay=0.0,
                               amsgrad=False)

        # Compile Model
        model.compile(optimizer=adam,
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        return model

# if __name__ == '__main__':
#     input_shape = (50, 30, 1)
#     kelas = 90
#     lr = 0.001
#     cnn = CNN(input_shape, kelas, lr)
#     model = cnn.my_model()