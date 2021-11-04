import os
from PIL import Image
from numpy import number

from elementary_cellular_automata import ElementaryCellularAutomata

def create_image(original, scale=1):
    '''
    Creates a black and white image from an array containing 1s and 0s.

    Parameters
    ----------
    original : numpy array

    Returns
    -------
    image  
        an image colored by the array original scaled by scale
    '''
    height, width = original.shape

    img = Image.new('L', (width * scale, height * scale), 'white')
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if original[j // scale, i // scale] == 1:
                img.putpixel((i,j), 0)

    return img

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

    for i in range(256):
        elemCA = ElementaryCellularAutomata(i, 400, 200, False)
        img = create_image(elemCA.history, 2)
        fileName = os.path.join(output_dir, "rule_{number}.png".format(number = i))
        with open(fileName, 'wb') as f:
            img.save(f)

if __name__ == '__main__':
    main()