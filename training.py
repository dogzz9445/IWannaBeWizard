from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

class ShapeClassifier:
    
    def __init__(self, data_folder: str):
         # Split dataset into Train, Validation & Test sets
        self.data_folder = data_folder
        self.size = 299   # Resize all images to (size,size)
        self.batch_size = 32      # Batch size

    def load_data(self):
        # Data augmentation on train dataset only
        train_data_gen = ImageDataGenerator(width_shift_range = 0.1, height_shift_range = 0.1, zoom_range=0.1, shear_range=0.1, brightness_range=[0.8,1.2], validation_split=0.15, preprocessing_function=preprocess_input)
        self.train_data = train_data_gen.flow_from_directory(self.data_folder, class_mode='categorical', target_size=(self.size,self.size), color_mode='rgb', batch_size=self.batch_size, seed=42, subset='training')

        validation_data_gen = ImageDataGenerator(validation_split=0.15, preprocessing_function=preprocess_input)
        self.validation_data = validation_data_gen.flow_from_directory(self.data_folder, class_mode='categorical', target_size=(self.size,self.size), color_mode='rgb', batch_size=self.batch_size, seed=42, subset='validation')

        test_data_gen = ImageDataGenerator(validation_split=0.10, preprocessing_function=preprocess_input)
        self.test_data = test_data_gen.flow_from_directory(self.data_folder, class_mode='categorical', target_size=(self.size,self.size), color_mode='rgb', subset='validation', shuffle=False)
    
        # Assign essential variables
        self.shape = self.train_data.image_shape                 # Shape of train images (height,width,channels)
        self.n_classes = self.train_data.num_classes                     # Total number of labels or classes
        self.train_samples = self.train_data.samples             # Total number of images in train set
        self.validation_samples = self.validation_data.samples   # total number of images in validation set
        
    def make_model(self):
        # Build the model
        input = Input(shape=self.shape)
        
        basemodel = InceptionResNetV2(include_top=False, weights='imagenet', input_shape=self.shape, pooling='avg')   # Basemodel is InceptionV3 with pretrained weights trained on imagenet dataset
        basemodel.trainable = False                                                                        # Freeze the weights in all layers of the CNN
        
        x = basemodel(input)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.2)(x)
        output = Dense(self.n_classes, activation='softmax')(x)
        
        self.model = Model(input,output)
        
        # Compile the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
    def fit_model(self):
        # Initialize callbacks
        stop = EarlyStopping(monitor='val_loss', patience=4, mode='min', restore_best_weights=True)                                             # Stops training early to prevent overfitting
        checkpoint = ModelCheckpoint(filepath='./weights/{val_loss:.4f}-weights-{epoch:02d}.hdf5', monitor='val_loss', mode='min', save_best_only=True)   # Saves the model for every best val_loss
        
        # Train the model
        ep = 50                      # Number of epochs
        spe = self.train_samples / self.batch_size       # Steps per epoch
        vs = self.validation_samples / self.batch_size   # Validation steps
        
        r = self.model.fit(self.train_data, validation_data=self.validation_data, steps_per_epoch=spe, validation_steps=vs, epochs=ep, callbacks=[stop,checkpoint])
    
    def test_model(self):
        # Predictions on the test data
        pred = self.model.predict(self.test_data).argmax(axis=1)
        labels = list(self.train_data.class_indices.keys())
        
    def save_model(self, file_name : str):
        self.model.save(file_name)
        
if __name__ == '__main__':
    shapeClassifier = ShapeClassifier('./train_data')
    shapeClassifier.load_data()
    shapeClassifier.make_model()
    shapeClassifier.fit_model()
    shapeClassifier.test_model()
    shapeClassifier.save_model('model/model_classification')
