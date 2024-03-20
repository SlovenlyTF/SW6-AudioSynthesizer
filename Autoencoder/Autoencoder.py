import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Conv2D, LeakyReLU, \
  BatchNormalization, Flatten, Dense, Reshape, Conv2DTranspose, \
  Activation, Lambda
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import tensorflow as tf

tf.compat.v1.disable_eager_execution()


class VAE:
  """
  VAE class
  """

  def __init__(
      self,
      spectrogram_dim,
      conv_filters,
      conv_kernels,
      conv_strides,
      latent_space_dim
    ):
    """
    Autoencoder initializer
    """
    self.spectrogram_dim = spectrogram_dim # (128, 128, 1)
    self.conv_filters = conv_filters
    self.conv_kernels = conv_kernels
    self.conv_strides = conv_strides
    self.latent_space_dim = latent_space_dim # 2

    self.encoder = None
    self.decoder = None

    self._shape_before_bottleneck = None
    self._model_input = None

    self.loss_weight = 1000000
    self.num_conv_layers = len(conv_filters)

    self._build()


  def _build(self):
    """
    Build the encoder and decoder
    """
    self._build_encoder()
    self._build_decoder()
    self._build_autoencoder()


  def summary(self):
    """
    Print model summary
    """
    self.encoder.summary()
    self.decoder.summary()
    self.autoencoder.summary()


  def _calculate_reconstruction_loss(self, y_true, y_pred):
    """
    Calculate the reconstruction loss
    """
    error = y_true - y_pred
    reconstruction_loss = K.mean(K.square(error), axis=[1, 2, 3])
    return reconstruction_loss


  def _calculate_kl_loss(self, y_true, y_pred):
    """
    Calculate the KL loss
    y_true and y_pred are not used, 
    but are required for Keras to use this loss function
    """
    print(f"log_var: {self.log_var}")
    kl_loss = -0.5 * K.sum(1 + self.log_var - K.exp(self.log_var) - K.square(self.mu), axis=1)
    return kl_loss
  

  def _calculate_total_loss(self, y_true, y_pred):
    """
    Calculate the total loss
    """
    reconstruction_loss = self._calculate_reconstruction_loss(y_true, y_pred)
    kl_loss = self._calculate_kl_loss(y_true, y_pred)
    total_loss = self.loss_weight * reconstruction_loss + kl_loss
    return total_loss
  

  def compile(self, learning_rate = 0.0001):
    """
    Compile the autoencoder
    """
    optimizer = Adam(learning_rate)
    # mse_loss = MeanSquaredError()
    self.autoencoder.compile(optimizer=optimizer, loss=self._calculate_total_loss, metrics=[self._calculate_kl_loss, self._calculate_reconstruction_loss])


  def train(self, x_train, y_train, batch_size, num_epochs):
    """
    Train the autoencoder
    """

    # Define the callbacks
    early_stopper = EarlyStopping(monitor='loss', min_delta=10, patience=3)

    callbacks = [early_stopper]

    # # Create an iterator for your dataset
    # dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))

    # # Define any transformations or preprocessing steps
    # dataset = dataset.batch(batch_size)  # Example: Batch the dataset

    # # Create an iterator for your dataset
    # iterator = tf.compat.v1.data.make_one_shot_iterator(dataset)
    # data = iterator.get_next()

    # # Start a TensorFlow session
    # with tf.compat.v1.Session() as sess:
    #   # Initialize global variables
    #   sess.run(tf.compat.v1.global_variables_initializer())

    #   # Train your model
    #   for epoch in range(num_epochs):
    #     print(f'Epoch {epoch + 1}/{num_epochs}')
    #     for batch in range(batch_size):
    #       print(f'Batch {batch + 1}/{batch_size}')
    #       x_batch, y_batch = sess.run(data)  # Fetch data from the iterator
    #       self.autoencoder.train_on_batch(x_batch, y_batch)


    self.autoencoder.fit(
      x_train, y_train,
      batch_size=batch_size,
      epochs=num_epochs,
      shuffle=True,
      callbacks=callbacks
    )

  ### Encoder
  def _build_encoder(self):
    """
    Create the Encoder
    """
    encoder_input = self._add_encoder_input()
    conv_layers = self._add_conv_layers(encoder_input)
    bottleneck = self._add_bottleneck(conv_layers)
    self._model_input = encoder_input
    self.encoder = Model(encoder_input, bottleneck, name='encoder')


  def _add_encoder_input(self):
    """
    Create encoder input layer
    """
    return Input(shape=self.spectrogram_dim, name='encoder_input')
  

  def _add_conv_layers(self, encoder_input):
    """
    Create all convolutional blocks in encoder
    """
    MLgraph = encoder_input
    for layer_index in range(self.num_conv_layers):
      MLgraph = self._add_conv_layer(layer_index, MLgraph)
    return MLgraph
  

  def _add_conv_layer(self, layer_index, MLgraph):
    """
    Add a convolutional block to a graph of layers, consisting of
    Conv2D, LeakyReLU, and BatchNormalization.
    """
    layer_number = layer_index + 1
    conv_layer = Conv2D(
        filters=self.conv_filters[layer_index],
        kernel_size=self.conv_kernels[layer_index],
        strides=self.conv_strides[layer_index],
        padding='same',
        name=f'encoder_conv_layer_{layer_number}'
    )
    MLgraph = conv_layer(MLgraph)
    MLgraph = LeakyReLU(name=f'encoder_leaky_relu_{layer_number}')(MLgraph)
    MLgraph = BatchNormalization(name=f'encoder_bn_{layer_number}')(MLgraph)
    return MLgraph
  

  def _add_bottleneck(self, MLgraph):
    """
    Flatten data and add bottleneck with Gaussian sampling (Dense layers)
    """

    self._shape_before_bottleneck = K.int_shape(MLgraph)[1:]
    MLgraph = Flatten(name='encoder_flatten')(MLgraph)
    self.mu = Dense(self.latent_space_dim, name='mu')(MLgraph)
    self.log_var = Dense(self.latent_space_dim, name='log_var')(MLgraph)

    def _sampling(args):
      """
      Sample from the latent space
      """
      mu, log_var = args
      epsilon = K.random_normal(shape=K.shape(mu), mean=0., stddev=1.)
      return mu + K.exp(log_var / 2) * epsilon

    MLgraph = Lambda(_sampling, name='encoder_output')([self.mu, self.log_var])
    return MLgraph


  ### Decoder
  def _build_decoder(self):
    """
    Create the decoder
    """
    decoder_input = self._add_decoder_input()
    dense_layer = self._add_dense_layer(decoder_input)
    reshape_layer = self._add_reshape_layer(dense_layer)
    conv_transpose_layers = self._add_conv_transpose_layers(reshape_layer)
    decoder_output = self._add_decoder_output(conv_transpose_layers)
    self.decoder = Model(decoder_input, decoder_output, name='decoder')


  def _add_decoder_input(self):
    """
    Create decoder input layer
    """
    return Input(shape=(self.latent_space_dim,), name='decoder_input')


  def _add_dense_layer(self, decoder_input):
    """
    Add dense layer to the decoder
    """
    num_neurons = np.prod(self._shape_before_bottleneck)
    dense_layer = Dense(num_neurons, name='decoder_dense')(decoder_input)
    return dense_layer
  

  def _add_reshape_layer(self, dense_layer):
    """
    Reshape the dense layer into a shape which can be fed into the
    convolutional transpose layers
    """
    return Reshape(self._shape_before_bottleneck)(dense_layer)


  def _add_conv_transpose_layers(self, MLgraph):
    """
    Add convolutional transpose layers
    """
    for layer_index in reversed(range(1, self.num_conv_layers)):
      MLgraph = self._add_conv_transpose_layer(layer_index, MLgraph)
    return MLgraph


  def _add_conv_transpose_layer(self, layer_index, MLgraph):
    """
    Add a convolutional transpose block to a graph of layers, consisting of
    Conv2DTranspose, LeakyReLU, and BatchNormalization.
    """
    layer_number = self.num_conv_layers - layer_index
    conv_transpose_layer = Conv2DTranspose(
        filters=self.conv_filters[layer_index],
        kernel_size=self.conv_kernels[layer_index],
        strides=self.conv_strides[layer_index],
        padding='same',
        name=f'decoder_conv_transpose_layer_{layer_number}'
    )
    MLgraph = conv_transpose_layer(MLgraph)
    MLgraph = LeakyReLU(name=f'decoder_leaky_relu_{layer_number}')(MLgraph)
    MLgraph = BatchNormalization(name=f'decoder_bn_{layer_number}')(MLgraph)
    return MLgraph
  

  def _add_decoder_output(self, MLgraph):
    """
    Add the decoder output layer
    """
    decoder_output = Conv2DTranspose(
        filters=1,
        kernel_size=self.conv_kernels[0],
        strides=self.conv_strides[0],
        padding='same',
        name=f'decoder_output'
    )
    MLgraph = decoder_output(MLgraph)
    MLgraph = Activation('sigmoid', name='sigmoid_layer')(MLgraph)
    return MLgraph 


  ### Autoencoder
  def _build_autoencoder(self):
    """
    Create the full autoencoder
    """
    model_input = self._model_input
    model_output = self.decoder(self.encoder(model_input))
    self.autoencoder = Model(model_input, model_output, name='autoencoder')


  ### Save and Load
  def save(self, path = '.'):
    """
    Save the autoencoder
    """
    self._create_dir_if_not_exists(path)
    self._save_parameters(path)
    self._save_weights(path)


  def _create_dir_if_not_exists(self, path):
    """
    Create directory if it does not exist
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
      os.makedirs(directory)


  def _save_parameters(self, path):
    """
    Save the parameters of the autoencoder
    """
    parameters = {
        'spectrogram_dim': self.spectrogram_dim,
        'conv_filters': self.conv_filters,
        'conv_kernels': self.conv_kernels,
        'conv_strides': self.conv_strides,
        'latent_space_dim': self.latent_space_dim
    }
    with open(os.path.join(path, 'parameters.pkl'), 'wb') as f:
      pickle.dump(parameters, f)


  def _save_weights(self, path):  
    """
    Save the weights of the autoencoder
    """
    self.autoencoder.save_weights(os.path.join(path, 'weights.h5'))


  @classmethod
  def load(cls, path):
    """
    Load the autoencoder
    """
    with open(os.path.join(path, 'parameters.pkl'), 'rb') as f:
      parameters = pickle.load(f)
    autoencoder = VAE(**parameters)
    autoencoder.autoencoder.load_weights(os.path.join(path, 'weights.h5'))
    return autoencoder


  ### reconstruction
  def reconstruct(self, spectrograms):
    """
    Reconstruct the spectrograms
    """
    latent_representations = self.encoder.predict(spectrograms)
    reconstructed_spectrograms = self.decoder.predict(latent_representations)
    return reconstructed_spectrograms, latent_representations
  

### Test
if __name__ == "__main__":
  ae = VAE(
      spectrogram_dim=(128, 128, 1),
      conv_filters=(32, 64, 64, 64),
      conv_kernels=(3, 3, 3, 3),
      conv_strides=(1, 2, 2, 1),
      latent_space_dim=2
  )
  ae.summary()