from kivy.core.audio import SoundLoader
from parameter import *
from all_button import ImgToggleButton_play, ImgButton_pre, ImgButton_next
from mutagen import File
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from song_slider import slid_bind, slid_func, next
#from main_lyt import box
##########################################################################
def song_btn(index, main_lyt, self):
    global other_layout, len_btn, len_btn2
    global curr_song, pre_song,pre_sound, song_counter, bt2
    global len_slid, sh, val_pre
    curr_song = index
    file3 = File(songlist[index][0])
    song_length = float(file3.info.pprint().split(',')[-1:][0][:-8])
    time = song_length/60
    minute = int(time)
    min_str = "{0:0=2d}".format(minute)
    second = int(round((time - minute)*60, 2))
    sec_str = "{0:0=2d}".format(second)
########################################################################
    if (other_layout == True):
        grid_2 = GridLayout(cols=3, size_hint=(1,0.05),row_force_default=True, 
                            row_default_height=40, opacity=1)
        b1 = Label(text='00:00', size_hint_x=None,width=main_lyt.width*0.15)
        grid_2.add_widget(b1)
        slid = Slider(min=0, max=100,cursor_width='8dp', cursor_height='8dp',
                      value_track=True,background_width = '8dp',value_track_width = '0.5dp',
                      value_track_color = [0, 1, 1, 1], step=1)
        slid.pos = (1,100)
        grid_2.add_widget(slid)
        b2 = Label(text='min'+':'+'sec',size_hint_x=None,width=main_lyt.width*0.15)
        grid_2.add_widget(b2)
        
        len_btn = b2
        len_btn2 = b1
        len_slid = slid
        
        print(slid_bind)
        
        slid.bind(value = slid_bind)        

        main_lyt.add_widget(grid_2)
    
    ###################################################################################
        fl = FloatLayout(size_hint=(1,0.1), opacity=1)
      
        bt1 = ImgButton_pre(prev_normal_img, prev_press_img,id='pre')
        bt1.bind(on_press = partial(previous_song))
        fl.add_widget(bt1)
        
        bt2 = ImgToggleButton_play(play_img, pause_img, id='pp')
        bt2.bind(on_press = partial(play_pause))
        fl.add_widget(bt2)
        
        bt3 = ImgButton_next(next_normal_img, next_press_img,id='next')
        bt3.bind(on_press = partial(next_song))
        fl.add_widget(bt3)
    
        main_lyt.add_widget(fl)
        other_layout = False
        
        
    
    len_btn.text = min_str+':'+sec_str
    len_slid.min = 0
    len_slid.value = 0
    len_slid.max = int(song_length)
    len_btn2.text = '00:00'
    
    try:
        print(songlist[pre_song][0] + '   :    stoped')
        bt2.state = 'normal'
        ImgToggleButton_play.on_state(bt2, 'fwfwf','normal')
        pre_sound.stop()
        pre_sound.unload()
        pre_song = -1
    except:
        pre_song = -1
    if (curr_song != pre_song):
        if (self.state == 'down'):
            sound = SoundLoader.load(songlist[index][0])  # songlist[index]
            bt2.state = 'down'
            ImgToggleButton_play.on_state(bt2, 'fwfwf','down')
            if (sound != None):
                val_pre = -1
                slid_func(sound, len_slid, len_btn2)
                sound.play()
                pre_song = index
                song_counter = index
                pre_sound = sound
                songlist[pre_song][1].state = 'down'
                print(songlist[pre_song][0] + '   :    playing')
def play_pause(self):
    global curr_song, pre_song,pre_sound, song_counter, len_slid, len_btn2, sh, song_position
    if (self.state == 'normal'):
        try:
            song_position = pre_sound.get_pos()
            sh.cancel()
            pre_sound.stop()
            #pre_sound.unload()
            songlist[pre_song][1].state = 'normal'
            print(songlist[pre_song][0] + '   :    stoped')
        except:
            pass
    else:
        index = pre_song
        sound = SoundLoader.load(songlist[index][0])
        bt2.state = 'down'
        ImgToggleButton_play.on_state(bt2, 'fwfwf','down')
        
        if (sound != None):
            val_pre = -1
            sound.play()
            #sound.seek(40.0)
            slid_func(sound, len_slid, len_btn2)
            pre_song = index
            song_counter = index
            pre_sound = sound
            songlist[pre_song][1].state = 'down'
            print(songlist[pre_song][0] + '   :    playing')
    
def previous_song(self):
    global curr_song, pre_song,pre_sound, song_counter
    pre_sound.stop()
    pre_sound.unload()
    songlist[song_counter][1].state = 'normal'
    song_counter = song_counter - 1
    if (song_counter < 0):
        song_counter=0
    song_btn(song_counter, 'nvef',self)

def next_song(self):
    global curr_song, pre_song,pre_sound, song_counter
    pre_sound.stop()
    pre_sound.unload()
    songlist[song_counter][1].state = 'normal'
    song_counter = song_counter + 1
    if (song_counter == len(songlist)):
        song_counter=len(songlist) - 1
    song_btn(song_counter, 'vnvv',self) 