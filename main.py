# Importing opencv and numpy
import cv2 as cv
import numpy as np

# Function to calculate the center given a contour
def calculate_center(contours):
  # Calculate the corner points and add some padding
  min = np.amin(contours, axis=0)[0] + [-10, -10]
  max = np.amax(contours, axis=0)[0] + [10, 5]
  
  # Calculate center of current cone
  center_x = (min[0] + max[0])//2
  center_y = (min[1] + max[1])//2
  center = (center_x, center_y)

  # Return the center (tuple of x and y)
  return center

def append_centers(cones, filter_result, cones_contours_left, cones_contours_right, index):
  # Calculate left and right centers for starting cones
  left_center = calculate_center(cones_contours_left[index])
  right_center = calculate_center(cones_contours_right[index])
  
  # Append centers to cones
  cones[0].append(left_center)
  # Add half of width of image to center to get correct coordinate on second half of image
  cones[1].append((right_center[0] + filter_result.shape[1]//2, right_center[1]))

# Function to calculate a line given two points and size of image. Ensures that line will extend throughout image
def calculate_line(x1, y1, x2, y2, width, height):
  # Calculate slope with two points
  slope = (y2 - y1)/(x2 - x1)

  # Calculate starting point
  start_x = int(0)
  start_y = int((-x1) * slope + y1)

  # Calculate ending point
  end_x = int(width)
  end_y = int(-(x2 - width) * slope + y2)

  # Return as tuple of the points stored as tuples
  return ((start_x, start_y), (end_x, end_y))

# Function to draw a line with two points
def draw_line(cone, width, height, img):
  # Extract coordinates from cone tuple
  x1 = cone[0][0]
  y1 = cone[0][1]
  x2 = cone[1][0]
  y2 = cone[1][1]
  
  # Calculate two points to create line across image
  p1, p2 = calculate_line(x1, y1, x2, y2, width, height)
  # Draw line between two points
  line = cv.line(img, p1, p2, (0, 0, 255), 2)

  return line

# Main function to run
def main():
  # Get the input image
  img = cv.imread('red.png', 1)

  # Convert color from default BGR to HSV
  hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

  # Use lower and upper range of orange
  lower_range = np.array([0, 210, 60])
  upper_range = np.array([179, 255, 255])

  # Create the mask on hsv using ranges
  mask = cv.inRange(hsv, lower_range, upper_range)

  # Create the filtered result based on the image and mask
  filter_result = cv.bitwise_and(img, img, mask=mask)
  # Blur the result to reduce noise of image
  filter_result = cv.medianBlur(filter_result, 15)
  # Detect the cone edges from filtered result
  filter_result = cv.Canny(filter_result, 155, 155)

  # Find contours for left and right portions of the image
  cones_contours_left, _ = cv.findContours(filter_result[:, :filter_result.shape[1]//2], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  cones_contours_right, _ = cv.findContours(filter_result[:, filter_result.shape[1]//2:], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

  # Initialize 2d array to store centers from left and right
  cones = [[], []]

  # Append starting and ending centers for both left and right side of image
  append_centers(cones, filter_result, cones_contours_left, cones_contours_right, 0)
  append_centers(cones, filter_result, cones_contours_left, cones_contours_right, -1)
  
  # Draw lines for left and right set of cones
  img = draw_line(cones[0], filter_result.shape[1], 0, img)
  img = draw_line(cones[1], filter_result.shape[1], 0, img)

  # Save the image
  cv.imwrite("answer.png", img)

  # Destroy all the windows to terminate program
  cv.destroyAllWindows()

if __name__ == "__main__":
  main()
