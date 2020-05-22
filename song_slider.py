from parameter import *
from kivy.clock import Clock
from functools import partial
from parameter import *


def slid_bind(self, value):
    global slid_val, val, val_pre
    val = float("{0:0=2d}".format(int(self.value)))
    #file_wr.write('all = '+str(val) + '    '+str(val-val_pre)+'   \n')
    if (val - val_pre != 1 and val != 0 and val - val_pre != 0):
        slid_val = 1  
    val_pre = val
    
def slid_func(sound, len_slid, len_btn2, my_fb, song_page_self):
    global sh
    try:
        sh.cancel()
    except:
        pass
    sh = Clock.schedule_interval(partial(nextt, sound, len_slid, len_btn2, my_fb, song_page_self), 1)
    #len_btn2.text = "{0:0=2d}".format(int(len_slid.value))#str(int(self.value)) 
    return sh

def next(sound, len_slid, len_btn2, my_fb, song_page_self, self):
    global slid_val, val
    if (len_slid.value > len_slid.max): 
        return False
    if (slid_val == 1):
        sound.stop()
        sound.unload()
        sound.play()
        sound.seek(val)
        slid_val = 0
    song_pos = sound.get_pos()
    time = song_pos/60
    minu = int(time)
    minu_str = "{0:0=2d}".format(minu)
    seco = int(round((time - minu)*60, 2))
    seco_str = "{0:0=2d}".format(seco)
    len_slid.value = song_pos
    len_btn2.text = minu_str + ':' + seco_str
    #################################################
    bar = my_fb.children[0]
    bar.value = int(song_pos)
    if bar.value < bar.max:
        bar.value_normalized += 1/(my_fb.children[0]._max_progress)
    #########################################
    if (int(song_pos) == int((my_fb.children[0]._max_progress))):
        sh.cancel()
        song_page_self.children[0].children[0].trigger_action(0)
