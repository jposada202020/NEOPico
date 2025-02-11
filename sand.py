import math

animation = 0

for i in range(300):
    saturation = math.sin(animation + i * 0.04)
    saturation = (saturation + 1) / 2
    print(saturation)
    animation += 0.2
