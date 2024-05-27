#Fully made by chatGPT 3.5

from PIL import Image, ImageEnhance
import numpy as np
import random

def add_noise(image, noise_factor=0.9):
    """
    Adds Gaussian noise to an image.
    
    Parameters:
    image (PIL.Image): Input image.
    noise_factor (float): Strength of the noise. Default is 0.1.
    
    Returns:
    PIL.Image: Image with added noise.
    """
    np_img = np.array(image)
    noise = np.random.normal(scale=noise_factor, size=np_img.shape).astype(np.uint8)
    noisy_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

def random_rotation(image, max_angle=10):
    """
    Rotates an image by a random angle within the range [-max_angle, max_angle].
    
    Parameters:
    image (PIL.Image): Input image.
    max_angle (float): Maximum absolute angle for rotation in degrees. Default is 10.
    
    Returns:
    PIL.Image: Rotated image.
    """
    angle = random.uniform(-max_angle, max_angle)
    rotated_img = image.rotate(angle)
    return rotated_img

if __name__ == "__main__":
    # Replace with your image file path
    input_image_path = 'images/jack.jpg'
    
    # Load the image
    original_image = Image.open(input_image_path)
    
    # Add noise
    noisy_image = add_noise(original_image, noise_factor=0.1)
    
    # Rotate image
    rotated_image = random_rotation(noisy_image, max_angle=20)
    
    # Save or display the modified image
    rotated_image.show()  # This will display the image
    # rotated_image.save('output_image.jpg')  # Uncomment this line to save the image
