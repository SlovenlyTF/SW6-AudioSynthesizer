#Fully made by chatGPT 3.5

import cv2
from matplotlib import pyplot as plt

def draw_keypoints(img, keypoints):
    """Draw keypoints on the image."""
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 0, 255), flags=0)
    return img_with_keypoints

def draw_matches(img1, kp1, img2, kp2, matches):
    """Draw matches between two images."""
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img_matches

# Load images
img_youtube = cv2.imread('images/postprocess/original_mario.png', 0)
img_not_youtube = cv2.imread('images/postprocess/original_mario.png', 0)

# Initialize ORB detector
orb = cv2.ORB_create()

# Detect keypoints and descriptors
kp1, des1 = orb.detectAndCompute(img_youtube, None)
kp2, des2 = orb.detectAndCompute(img_not_youtube, None)

# Draw keypoints
img_youtube_keypoints = draw_keypoints(img_youtube, kp1)
img_not_youtube_keypoints = draw_keypoints(img_not_youtube, kp2)

# Create the bruteforce matcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Perform matches
matches = bf.match(des1, des2)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw top N matches
N = 100  # Number of matches to draw
img_matches = draw_matches(img_youtube, kp1, img_not_youtube, kp2, matches[:N])

# Plotting the results
plt.figure(figsize=(20, 10))

plt.subplot(1, 3, 1)
plt.title('Keypoints in Image 1')
plt.imshow(img_youtube_keypoints, cmap='gray')

plt.subplot(1, 3, 2)
plt.title('Keypoints in Image 2')
plt.imshow(img_not_youtube_keypoints, cmap='gray')

plt.subplot(1, 3, 3)
plt.title(f'Top {N} Matches')
plt.imshow(img_matches)

plt.show()
