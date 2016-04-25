import sys
from PIL import Image
import random
import math
import operator

def distance(first, second):
    return math.sqrt((second[0] - first[0])**2 + (second[1] - first[1])**2)

def get_mean(pixels, coord, k):
    r = 0
    g = 0
    b = 0
    n = {}
    for p in pixels:
        n[distance(coord, p[3])] = p
    ns = []
    keylist = n.keys()
    keylist.sort()
    index = 0
    for key in keylist:
        ns.append(n[key])
        index += 1
        if index >= k:
            break

    for pixel in ns:
        r += p[0]
        g += p[1]
        b += p[2]
    return (r / len(ns), g / len(ns), b / len(ns))

def get_random(pixels):
    index = int(random.random() * len(pixels))
    return pixels[index]

def get_median(pixels, coord, k):
    if k < 3:
        print "Can't use median with k < 3"
        sys.exit(1)
    r = []
    g = []
    b = []
    n = {}
    for p in pixels:
        n[distance(coord, p[3])] = p
    ns = []
    keylist = n.keys()
    keylist.sort()
    index = 0
    for key in keylist:
        ns.append(n[key])
        index += 1
        if index >= k:
            break

    for p in ns:
        r.append(p[0])
        g.append(p[1])
        b.append(p[2])
    r.sort()
    g.sort()
    b.sort()
    if len(ns) < 3:
        return (r[0], g[0], b[0])

    return (r[len(r)/2+1], g[len(g)/2+1], b[len(b)/2+1])

def get_mode(pixels):
    r = {}
    g = {}
    b = {}
    for p in pixels:
        try:
            r[p[0]] += 1
        except:
            r[p[0]] = 1
        try:
            g[p[1]] += 1
        except:
            g[p[1]] = 1
        try:
            b[p[2]] += 1
        except:
            b[p[2]] = 1
    m = 0
    red = 0
    green = 0
    blue = 0
    for k, v in r.items():
        if v > m:
            red = k
            m = v
    m = 0
    for k, v in g.items():
        if v > m:
            green = k
            m = v
    m = 0
    for k, v in b.items():
        if v > m:
            blue = k
            m = v
    return (red, green, blue)

if len(sys.argv) < 4:
    print "Usage: python learn.py <training_file> <test_file> <neighbors>"
    sys.exit(1)

# Open image
try:
    image = Image.open(sys.argv[1])
    image2 = Image.open(sys.argv[2])
    neighbors = int(sys.argv[3])
except:
    print "Unable to open the specified file"
    sys.exit(1)

# Learn
# first one to train, second is test
width, height = image.size
width2, height2 = image2.size
index = 0
data = {}

for p in image.getdata():
    x = index % width
    y = index / width
    av = (p[0] + p[1] + p[2]) / 3
    if not av in data:
        data[av] = [(p[0], p[1], p[2], (x, y))]
    else:
        data[av].append((p[0], p[1], p[2], (x, y)))
    index += 1

# Predict
pixels = []
index = 0
for p in image2.getdata():
    x = index % width2
    y = index / width2
    index += 1
    if p[0] in data:
        #pixels.append(data[p[0]][0])
        #pixels.append(get_mean(data[p[0]], (x, y), neighbors))
        pixels.append(get_median(data[p[0]], (x, y), neighbors))
        #pixels.append(get_mode(data[p[0]]))
        #pixels.append(get_random(data[p[0]]))
    else:
        val = p[0]
        diff = 0
        while True:
            if val == 0:
                pixels.append((0, 0, 0))
                break
            else:
                val -= 1
            if val in data:
                #pixels.append(data[val][0])
                #pixels.append(get_mean(data[val], (x, y), neighbors))
                pixels.append(get_median(data[val], (x,y), neighbors))
                #pixels.append(get_mode(data[val]))
                #pixels.append(get_random(data[val]))
                break
image2.putdata(pixels)

file_name = "col_"+sys.argv[2]
image2.save(file_name)
