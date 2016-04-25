# colorizing
This repository has some scripts for colorizing black and white images.

The K-Nearest Neighbor script trains on a single image. It turns the training image to grayscale and stores an association of
which colors map to certain grayscale values and the pixels' coordinates on the page. To color an image, it looks up the gray
value and chooses a color from the list of colors that map to the same grayscale value. From those color values, it chooses
the one with the closest coordinates. It is very accurate for similar images, but generalizes very poorly.
It can be run like this:

`python knn.py <some_training_image_file <some_black_and_white_image_file> <number of neighbors>`


For example:

`python knn.py train.jpg gray.jpg 3`
