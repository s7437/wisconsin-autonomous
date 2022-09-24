# Wisconsin Autonomous Perception Coding Challenge Submission
This is my submission for the Wisconsin Autonomous Perception Coding Challenge.

## Methodolgy
I decided to use color filtering in order to detect all of the cones. OpenCV allows you to convert an image to HSV, and using the HSV range of orange, I could create a mask to find all of the cones. After that, I could then use the Canny function to get all of the contours. Using this information, I could calculate the centers of each cone, and draw the lines.

## What did you try and why do you think it did not work
At first I was using the template functionality built into OpenCV, but I was getting a lot of false positives. I moved and tried using the color filtering, but the image was still very noisy. I then read about different blurring techniques, and utilized the median blur in order to remove all of the noise. This worked because I could then clearly identify the cones and calculate the centers of each one, which allowed me to draw the lines correctly.

## Libraries
* OpenCV
* Numpy
