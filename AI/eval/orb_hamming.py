import cv2
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity

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
        return 0, matches
    return len(similar_regions) / len(matches), matches

# Needs images to be same dimensions
def structural_sim(img1, img2):
    sim, diff = structural_similarity(img1, img2, full=True)
    return sim

img_youtube = cv2.imread('images/postprocess/original_mario.png', 0)
img_not_youtube = cv2.imread('images/postprocess/original_mario.png', 0)

orb_similarities = []
all_matches = []
distances = range(101)

for distance in distances:
    orb_similarity, matches = orb_sim(img_youtube, img_not_youtube, distance)  # 1.0 means identical. Lower = not similar
    orb_similarities.append(orb_similarity)
    all_matches.append(matches)

# Visualize Hamming distances for a specific threshold
distance_threshold = 70  # Example threshold
_, matches = orb_sim(img_youtube, img_not_youtube, distance_threshold)

# Extracting Hamming distances
hamming_distances = [match.distance for match in matches]

# Plotting Hamming distances
plt.figure(figsize=(10, 6))
plt.hist(hamming_distances, bins=30, edgecolor='black')
plt.title('Distribution of Hamming Distances')
plt.xlabel('Hamming Distance')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
