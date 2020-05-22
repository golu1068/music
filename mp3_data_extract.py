from mutagen import File
from parameter import *
import random

########################################
def data_extract(fn):
    file = File(str(fn))
#                song_length = float(file2.info.pprint().split(',')[-1:][0][:-8])
#                print(float(song_length))
#    print(fn)
    try:
        song_name = file['TIT2'].text[0]
    except:
        song_name = fn.split('/')[-1:][0] [:-4]   

    try:
        artwork = file.tags['APIC:'].data
        with open(song_name + '.jpg', 'wb') as img:
            img.write(artwork)
        cover_album.append(song_name+'.jpg')
        btn_image = song_name+'.jpg'
    except:
        rand_val = random.randint(0, 9)
        cover_album.append('images/'+m_image[rand_val])
        btn_image = 'images/'+m_image[rand_val]
        
    return song_name, btn_image