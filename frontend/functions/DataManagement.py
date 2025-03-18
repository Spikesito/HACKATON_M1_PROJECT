from keras import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import load_model
import joblib

from functions.utils import Preprocess


class DataManagement:
    def __init__(self, X=None, y=None):
        self.X, self.y = X, y
        self.X_train, self.y_train, self.X_test, self.y_test = None, None, None, None
        self.model = None
        self.preprocessor = None

    def init_model(self):
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(self.X_train.shape[1],)),
            Dense(32, activation='relu'),
            Dense(6)
        ])

        self.model.compile(optimizer='adam', loss='mse',
                           metrics=['mse', 'mae', tf.keras.metrics.RootMeanSquaredError(), 'mape'])

    def prepare_data(self, features):
        self.X, self.preprocessor = Preprocess(features, self.X, fit=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                random_state=42)

    def train(self):
        self.init_model()
        self.model.fit(self.X_train, self.y_train, epochs=200, batch_size=32,
                       validation_data=(self.X_test, self.y_test))

    def save(self, filename):
        self.model.save("models/" + filename)
        joblib.dump(self.preprocessor, "models/" + filename + "_preprocessor.pkl")

    def load(self, filename):
        self.model = load_model("models/" + filename)
        self.preprocessor = joblib.load("models/" + filename + "_preprocessor.pkl")

    def predict(self, X, features):
        X_preprocessed, _ = Preprocess(features, X, fit=False, preprocessor=self.preprocessor)
        return self.model.predict(X_preprocessed)