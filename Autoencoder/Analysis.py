import numpy as np
import matplotlib.pyplot as plt

def select_images(images, labels, n_images=5):
  """
  Select random images and their labels from a dataset
  """
  indices = np.random.choice(range(len(images)), n_images)
  sample_images = images[indices]
  sample_labels = labels[indices]
  return sample_images, sample_labels


def plot_reconstructed_images(images, reconstructed_images):
  """
  Plot images and their reconstructed images
  """
  fig, axes = plt.subplots(nrows=2, ncols=5, sharex=True, sharey=True, figsize=(22, 8))
  for images, row in zip([images, reconstructed_images], axes):
    for img, ax in zip(images, row):
      ax.imshow(img.reshape((128, 128)))
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)
  fig.tight_layout(pad=0.1)
  plt.show()
  plt.close()


if __name__ == "__main__":
  images = np.load('x.npy')
  labels = np.load('y.npy')
  sample_images, sample_labels = select_images(images, labels)
  plot_reconstructed_images(sample_images, sample_labels)
  print("Done")

