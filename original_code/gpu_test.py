import tensorflow as tf

# Check if GPU is available
if tf.test.is_gpu_available():
    print("GPU is available")
else:
    print("GPU is NOT available")


# Check if GPU is available
print(tf.config.list_physical_devices('GPU'))

