
"""
Input: nothing
Return:
- vgg16 model loaded weights but not yet compiled
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.contrib.keras.python.keras import backend as K
from tensorflow.contrib.keras.python.keras.applications.imagenet_utils import _obtain_input_shape
from tensorflow.contrib.keras.python.keras.applications.imagenet_utils import decode_predictions  # pylint: disable=unused-import
from tensorflow.contrib.keras.python.keras.applications.imagenet_utils import preprocess_input  # pylint: disable=unused-import
from tensorflow.contrib.keras.python.keras.engine.topology import get_source_inputs
from tensorflow.contrib.keras.python.keras.layers import Conv2D
from tensorflow.contrib.keras.python.keras.layers import Dense
from tensorflow.contrib.keras.python.keras.layers import Flatten
from tensorflow.contrib.keras.python.keras.layers import GlobalAveragePooling2D
from tensorflow.contrib.keras.python.keras.layers import GlobalMaxPooling2D
from tensorflow.contrib.keras.python.keras.layers import Input
from tensorflow.contrib.keras.python.keras.layers import MaxPooling2D
from tensorflow.contrib.keras.python.keras.models import Model
from tensorflow.contrib.keras.python.keras.utils import layer_utils
from tensorflow.contrib.keras.python.keras.utils.data_utils import get_file


WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels.h5'
WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'


def VGG16(include_top=True,
          weights='imagenet',
          input_tensor=None,
          input_shape=None,
          pooling=None,
          classes=1000):
  """Instantiates the VGG16 architecture.

  Optionally loads weights pre-trained
  on ImageNet. Note that when using TensorFlow,
  for best performance you should set
  `image_data_format="channels_last"` in your Keras config
  at ~/.keras/keras.json.

  The model and the weights are compatible with both
  TensorFlow and Theano. The data format
  convention used by the model is the one
  specified in your Keras config file.

  Arguments:
      include_top: whether to include the 3 fully-connected
          layers at the top of the network.
      weights: one of `None` (random initialization)
          or "imagenet" (pre-training on ImageNet).
      input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
          to use as image input for the model.
      input_shape: optional shape tuple, only to be specified
          if `include_top` is False (otherwise the input shape
          has to be `(224, 224, 3)` (with `channels_last` data format)
          or `(3, 224, 224)` (with `channels_first` data format).
          It should have exactly 3 inputs channels,
          and width and height should be no smaller than 48.
          E.g. `(200, 200, 3)` would be one valid value.
      pooling: Optional pooling mode for feature extraction
          when `include_top` is `False`.
          - `None` means that the output of the model will be
              the 4D tensor output of the
              last convolutional layer.
          - `avg` means that global average pooling
              will be applied to the output of the
              last convolutional layer, and thus
              the output of the model will be a 2D tensor.
          - `max` means that global max pooling will
              be applied.
      classes: optional number of classes to classify images
          into, only to be specified if `include_top` is True, and
          if no `weights` argument is specified.

  Returns:
      A Keras model instance.

  Raises:
      ValueError: in case of invalid argument for `weights`,
          or invalid input shape.
  """
  ### how many weights option can we be allowed
  if weights not in {'imagenet', None}:
    raise ValueError('The `weights` argument should be either '
                     '`None` (random initialization) or `imagenet` '
                     '(pre-training on ImageNet).')

  ### if use imagenet weights and add last 3 dense layers, then class should be 1000
  if weights == 'imagenet' and include_top and classes != 1000:
    raise ValueError('If using `weights` as imagenet with `include_top`'
                     ' as true, `classes` should be 1000')

  ### set input shape : (224, 224, 3)
  # default input shape for VGG16 model, designed for imagenet dataset
  input_shape = _obtain_input_shape(
      input_shape, # if set must be a tuple of 3 integers (50, 50, 3)
      default_size=224, # if input_shape set, here must be None
      min_size=48,
      data_format=K.image_data_format(), # 'channels_first' or 'channels_last'
      include_top=include_top) # True, then must use 224 or False to be other number

  ### Create input tensor: real tensor or container?
  if input_tensor is None:
	# create input tensor placeholder
    img_input = Input(shape=input_shape)
  else:
    img_input = Input(tensor=input_tensor, shape=input_shape)

  # Block 1
  x = Conv2D(
      64, (3, 3), activation='relu', padding='same',
      name='block1_conv1')(img_input)

  ## how to access weights of each layer
  block1_conv1 = x
  block1_conv1_bias=block1_conv1.graph._collections['trainable_variables'][-1] # bias
  block1_conv1_kernel=block1_conv1.graph._collections['trainable_variables'][-2] # kernel

  x = Conv2D(
      64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
  block1_conv2 = x
  block1_conv2_bias=block1_conv2.graph._collections['trainable_variables'][-1] # bias
  block1_conv2_kernel=block1_conv2.graph._collections['trainable_variables'][-2] # kernel

  x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)
  block1_pool = x
  # access trainable_variables or weights with biases
  block1_pool.graph._collections['variables'][-1] # bias
  block1_pool.graph._collections['variables'][-2] # kernel

  # Block 2
  x = Conv2D(
      128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
  block2_conv1 = x

  x = Conv2D(
      128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
  block2_conv2 = x

  x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)
  block2_pool = x

  # Block 3
  x = Conv2D(
      256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
  block3_conv1 = x

  x = Conv2D(
      256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
  block3_conv2 = x

  x = Conv2D(
      256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
  block3_conv3 = x

  x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)
  block3_pool = x

  # Block 4
  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
  block4_conv1 = x

  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
  block4_conv2 = x

  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
  block4_conv3 = x

  x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)
  block4_pool = x

  # Block 5
  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
  block5_conv1 = x

  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
  block5_conv2 = x

  x = Conv2D(
      512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
  block5_conv3 = x

  x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)
  block5_pool = x

  if include_top:
    # Classification block
    x = Flatten(name='flatten')(x)
    flatten = x
    x = Dense(4096, activation='relu', name='fc1')(x)
    fc1 = x
    x = Dense(4096, activation='relu', name='fc2')(x)
    fc2 = x
    x = Dense(classes, activation='softmax', name='predictions')(x)
    predictions = x

  else:
    if pooling == 'avg':
      x = GlobalAveragePooling2D()(x)
    elif pooling == 'max':
      x = GlobalMaxPooling2D()(x)

  # Ensure that the model takes into account
  # any potential predecessors of `input_tensor`.
  if input_tensor is not None:
    inputs = get_source_inputs(input_tensor)
  else:
    inputs = img_input
  # Create model.
  model = Model(inputs, x, name='vgg16')

  # load weights
  if weights == 'imagenet':
    if include_top:
      weights_path = get_file(
          'vgg16_weights_tf_dim_ordering_tf_kernels.h5',
          WEIGHTS_PATH,
          cache_subdir='models')
    else:
      weights_path = get_file(
          'vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5',
          WEIGHTS_PATH_NO_TOP,
          cache_subdir='models')
    model.load_weights(weights_path)
    if K.backend() == 'theano':
      layer_utils.convert_all_kernels_in_model(model)

    if K.image_data_format() == 'channels_first':
      if include_top:
        maxpool = model.get_layer(name='block5_pool')
        shape = maxpool.output_shape[1:]
        dense = model.get_layer(name='fc1')
        layer_utils.convert_dense_weights_data_format(dense, shape,
                                                      'channels_first')
  return model

vgg16 = VGG16()
"""
1. VGG16 model for Keras
2. with each layer's output tensor
3. how a layer in tf.keras is constructed?
	a. tf.Layer class __init__ : added onto graph
	b. tf.keras.Layer class __init__
	c. tf.Layer._Conv class __init__
	d. tf.Layer.Conv2D class __init__
	e. tf.keras.Conv2D class __init__
4. how to get output tensor of this layer?
	1. tf.keras.Layer.__call__
	2. tf.Layer.__call__:
		2.1. tf.keras.Conv2D.build:
			2.1.1 tf.convolution.Conv2D.build
				2.1.1.1. tf.layers._Conv.build: create kernel and bias variables
	2. tf.Layer.__call__:
		2.2. tf.convolutional._Conv.call: get outputs with nn.convolution(), kernel, and bias
	1. tf.keras.Layer.__call__: _add_inbound_node()
	return output

5. how to build a model using input tensor and last output tensor?
	a. tf.keras.Layer
	b. tf.keras.Container.__init__

6. how to compile a model?
	c. tf.keras.Model.compile and other methods

- [Very Deep Convolutional Networks for Large-Scale Image
Recognition](https://arxiv.org/abs/1409.1556)

"""