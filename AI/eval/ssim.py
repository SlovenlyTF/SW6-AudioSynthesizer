# https://youtu.be/16s3Pi1InPU

#https://github.com/bnsreenu/python_for_microscopists/blob/master/191_measure_img_similarity.py
"""
Comparing images using ORB/SIFT feature detectors
and structural similarity index. 

@author: Sreenivas Bhattiprolu
Adapted by: chatGPT
"""

import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity
import cv2

# Works well with images of different dimensions
def orb_sim(img1, img2, distance_threshold):
    # SIFT is no longer available in cv2 so using ORB
    orb = cv2.ORB_create()

    # detect keypoints and descriptors
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    # define the bruteforce matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # perform matches
    matches = bf.match(desc_a, desc_b)
    # Look for similar regions with distance < distance_threshold
    similar_regions = [i for i in matches if i.distance < distance_threshold]
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)

# Needs images to be same dimensions
def structural_sim(img1, img2):
    sim, diff = structural_similarity(img1, img2, full=True)
    return sim

img_youtube = cv2.imread('images/postprocess/original_mario.png', 0)
img_not_youtube = cv2.imread('images/postprocess/original_mario.png', 0)

orb_similarities = []
distances = range(101)

for distance in distances:
    orb_similarity = orb_sim(img_youtube, img_not_youtube, distance)  # 1.0 means identical. Lower = not similar
    orb_similarities.append(orb_similarity)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(distances, orb_similarities, marker='o')
plt.title('ORB Similarity vs. Distance Threshold')
plt.xlabel('Distance Threshold')
plt.ylabel('ORB Similarity')
plt.grid(True)
plt.show()

# Calculate SSIM for reference
ssim = structural_sim(img_youtube, img_not_youtube)  # 1.0 means identical. Lower = not similar
print("Similarity using SSIM is: ", ssim)