from PIL import Image
import time
from utils.binary_quality_search import binary_quality_search
from utils.logger import logger


if __name__ == '__main__':
    _file = 'rabbit-2.jpg'
    _format = 'JPEG'
    _qulaity = 124
    
    start = time.time()
    binary = binary_quality_search(
        '/Users/mattbozelka/Desktop/images/' + _file,
        '/Users/mattbozelka/Desktop/optimized',
        _qulaity,
        image_format=_format
    )
    im = Image.open('/Users/mattbozelka/Desktop/images/' + _file)
    im.save('/Users/mattbozelka/Desktop/optimized/' + _file, format=_format, quality=binary, optimize=True)
    logger('Time to complete the Binary process:', (time.time() - start))


    # _file = 'download.png'
    # _format = 'PNG'
    # start = time.time()
    # im = Image.open('/Users/mattbozelka/Desktop/images/' + _file)
    # im.save('/Users/mattbozelka/Desktop/optimized' + _file, format=_format, optimize=True)
    # logger('Time to complete the PNG process:', (time.time() - start))
    
    # start = time.time()
    # linear = linear_quality_search(
    #     '/Users/mattbozelka/Desktop/images/test_l.jpg',
    #     '/Users/mattbozelka/Desktop/optimized',
    #     98
    # )
    # compress_image(
    #     image_path='/Users/mattbozelka/Desktop/images/test_l.jpg', 
    #     output_path='/Users/mattbozelka/Desktop/optimized/test_l.jpg', 
    #     quality=linear, 
    #     image_format='JPEG')
    # logger('Time to complete the Linear process:', (time.time() - start))


    logger('Binary quality', binary)
    # logger('Linear quality', linear)