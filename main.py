import cv2
import csv

def divide_interval(start, end, parts):
    interval_size = (end - start + 1) / parts  # Calculate the size of each interval
    intervals = [start + interval_size * i for i in range(parts)]  # Create intervals
    return intervals

image = cv2.imread('', 1)  # image name

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresholded = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on width and height
filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > 100]

data_points = []
for contour in filtered_contours:
    x, y, w, h = cv2.boundingRect(contour)
    data_points.append((x, y, w, h))

# Sort data points based on x-coordinate
sorted_data_points = sorted(data_points, key=lambda x: x[0])

x_range = input('Enter x-axis range (start-end): ').split('-')
x_range = [int(value) for value in x_range]

# Error handling for y-axis range
try:
    y_range = input('Enter y-axis range (start-end): ').split('-')
    y_range = [int(value) for value in y_range]
except ValueError:
    print("Invalid input for y-axis range. Please enter valid integers.")
    exit(1)

img_height = image.shape[0]

with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['x-axis', 'y-axis'])
    
    # Divide x-axis range into intervals
    intervals = divide_interval(x_range[0], x_range[1], len(sorted_data_points))
    
    for i in range(len(sorted_data_points)):
        height = sorted_data_points[i][3] / img_height * (y_range[1] - y_range[0])
        y_coor = height + y_range[0]
        csvwriter.writerow([int(intervals[i]), y_coor])

print("Output CSV generated successfully.")
