# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
from my_toolbar import my_MDToolbar
from kivy.uix.image import Image
#from nav_button import play_pause, previous_song, next_song, song_btn
from kivymd.uix.toolbar import MDToolbar, MDBottomAppBar
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty, \
ListProperty, ReferenceListProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.ripplebehavior import CircularRippleBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from circular_progress_bar import CircularProgressBar
##############################################################
global co
co=0;
class my_FloatButton(AnchorLayout):
    callback = ObjectProperty()
    md_bg_color = ListProperty([1, 1, 1, 1])
    icon = StringProperty()

class ItemMenuForFitness(CircularRippleBehavior, ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ItemMenuForFitness, self).__init__(**kwargs)
        pass
    
    def bt_img(self, tool_self):
##        self.source = 'images/image_2.jpg'
        self.size_hint = (None,None)
        self.size = (dp(56), dp(56))
        self.pos_hint = {'center_x':0.5, 'center_y': .5}
        self.pos = [50,20]
        self.color = [1,1,1,0]
#        self.canvas.children[2].size = [tool_self.size[0]*0.5,tool_self.size[1]*0.5]
        with self.canvas:
            Color(1,1,1,.8)
            self.rect4 = RoundedRectangle(radius=[9000],segments=15)
            self.rect4.source = 'images/my_photo.jpg'
        def update_rect(instance, value):
            instance.rect4.pos = instance.pos#[instance.pos[0],instance.pos[1]]
            instance.rect4.size = instance.size#[instance.size[1], instance.size[1]]   
        self.bind(pos=update_rect, size=update_rect)
        
        tool_self.add_widget(self)
        

        
class song_page(FloatLayout):
    def __init__(self, music_app_self, **kwargs):
        super(song_page, self).__init__(**kwargs)
        global other_layout, len_btn, len_btn2, song_page_self
        global curr_song, pre_song,pre_sound, song_counter, bt2,bt1,bt3
        global len_slid, sh, val_pre
        ########################################################################
        song_page_self = self
#        self.song_page_box  = BoxLayout(orientation = 'vertical')
#        tool_box.size_hint = (self.size_hint[0]*0.2,self.size_hint[1]*0.2)
#        self.song_page_box.pos = (0,540)
        self.tb = my_MDToolbar(title='song name',anchor_title='center',
        background_palette= 'Primary')
        self.tb.md_bg_color = [1,1,1,0.3]
        self.tb.pos_hint = {'x':0, 'y':0.9}
        self.tb.left_action_items= [['chevron-down', lambda x : self.gonext(music_app_self)]]
#        self.song_page_box.add_widget(self.tb)
        self.add_widget(self.tb)
        
        self.song_page_float = FloatLayout(size=(100,100))
        ############################################################
        with self.song_page_float.canvas.after:
            self.song_page_float.rect = RoundedRectangle(segments=15, radius=[50])
            self.song_page_float.rect.source = 'images/image_2.jpg'
        def update_rect(instance, value):
            instance.rect.size = [instance.size[0]*0.8, instance.size[0]*0.6]
            instance.rect.pos = [instance.pos[0]+instance.size[0]*0.1,instance.pos[1]+instance.size[1]*0.4]
        self.song_page_float.bind(pos=update_rect, size=update_rect)
        ###########################################################
#        self.im1 = Image(source='images/image_2.jpg', color=(1,1,1,.5),
#                    size_hint=(self.size_hint[0]*0.3,self.size_hint[1]*0.3))
#
#        self.im1.pos_hint={'x':.35, 'y':.4}
#        
#        self.song_page_float.add_widget(self.im1)
#        
        self.add_widget(self.song_page_float)
        #########################################################
        self.grid_2 = GridLayout(cols=3, size_hint=(1,0.2),row_force_default=True, 
                            row_default_height=40, opacity=1)
#        print(self.grid_2.size_hint)
        self.b1 = Label(text='00:00',color=(0,0,1,0.5),size_hint_x=None,width=self.width)
        self.grid_2.add_widget(self.b1)
        
        self.slid = Slider(min=-1, max=100,value=0,cursor_width='8dp', cursor_height='30dp',
                      value_track=True,background_width = '8dp',value_track_width = '1.5dp',
                      value_track_color = [0, 0, 1, 1], step=1)
        self.slid.pos = (1,100)
        self.grid_2.add_widget(self.slid)
        self.b2 = Label(text='min'+':'+'sec',size_hint_x=None,width=self.width,color=(0,0,1,0.5))
        self.grid_2.add_widget(self.b2)
        
        len_btn = self.b2
        len_btn2 = self.b1
        len_slid = self.slid

        self.slid.bind(value = slid_bind)        
        self.add_widget(self.grid_2)
        
    
        fl = FloatLayout(size_hint=(1,0.05), opacity=1)
        
        bt1 = ImgButton_pre(prev_normal_img, prev_press_img,id='pre')
#        bt1.bind(on_press = partial(self.previous_song))
        fl.add_widget(bt1)
        
        bt2 = ImgToggleButton_play(play_img, pause_img, id='pp')
#        bt2.bind(on_press = partial(self.play_pause))
        fl.add_widget(bt2)
        
        bt3 = ImgButton_next(next_normal_img, next_press_img,id='next')
#        bt3.bind(on_press = partial(self.next_song))
        fl.add_widget(bt3)
        
        self.add_widget(fl)
#        self.add_widget(self.song_page_box)

        
    def gonext(self, music_app_self):
        music_app_self.sm.transition.direction = 'down'
        music_app_self.sm.current = 'mainscreen'
        
    def update_info(btn_self,index, main_self, music_app_self,*args):
        global song_page_self, co, pre_sound, bt2, ite,pre_song,bt1,bt3,sh, len_btn2,len_slid
        global cpb, ite, my_fb
#        def animate(self,dt, song_len):
 #           bar = self.children[0]
 #           if bar.value < bar.max:
 #               bar.value_normalized += 1/(self.children[0]._max_progress)
        
        curr_song = index
        file = File(songlist[index][0])
        song_length = float(file.info.pprint().split(',')[-1:][0][:-8])
        time = song_length/60
        minute = int(time)
        min_str = "{0:0=2d}".format(minute)
        second = int(round((time - minute)*60, 2))
        sec_str = "{0:0=2d}".format(second)
        try:
            singer = file['TPE1'].text[0]
        except:
            try:
                singer = file['TALB'].text[0]
            except:
                singer = ''
        try:
            song_name = file['TIT2'].text[0]
        except:
            song_name = (file.filename.split('/'))[-1:][0]
            
        song_page_self.tb.title = '[b]'+song_name+'[/b]'
        song_page_self.tb.ids['lbl2'].text = singer
        song_page_self.b2.text=min_str+':'+sec_str
        song_page_self.slid.max = int(song_length)
#        song_page_self.im1.source = cover_album[index]
        song_page_self.song_page_float.rect.source = cover_album[index]
#        ########################################################
        if (co == 0):
            my_fb = FloatLayout()
            my_fb.size_hint = [1,0.09]
#            ############################################3
            ite = ItemMenuForFitness()
            ite.bt_img(my_fb)
            ite.bind(on_release=partial(song_page_self.gonext_playpage,music_app_self))
            ############################################3
            cpb = CircularProgressBar(ite)
            cpb.size_hint = ite.size_hint
            my_fb.add_widget(cpb)
            #############################################
            co += 1
            main_self.add_widget(my_fb)
            ##################################################
            bt1.bind(on_press = partial(song_page_self.previous_song, btn_self, main_self,music_app_self))
            bt2.bind(on_press = partial(song_page_self.play_pause, btn_self))
            bt3.bind(on_press = partial(song_page_self.next_song, btn_self, main_self,music_app_self))
            ################################################
        ite.rect4.source = cover_album[index]
        cpb._max_progress = int(song_length)
#        try:
#            csh.cancel()
#        except:
#            pass    
 #       csh = Clock.schedule_interval(partial(animate, my_fb, (song_length)), 1)
#        ########################################################
#####################################################################
        ## play song
        try:
            bt2.state = 'down'
            ImgToggleButton_play.on_state(bt2, 'fwfwf','normal')
            pre_sound.stop()
            pre_sound.unload()
            pre_song = -1
        except:
            pre_song = -1    
        if (curr_song != pre_song):
            if (btn_self.state == 'down'):
                bt2.state = 'down'
                ImgToggleButton_play.on_state(bt2, 'fwfwf','down')
                sound = SoundLoader.load(songlist[index][0])
                if (sound != None):
                    val_pre = -1
                    sh = slid_func(sound, len_slid, len_btn2, my_fb, song_page_self)
                    sound.play()
                    pre_sound = sound
                    pre_song = index
                    song_counter = index
                    songlist[pre_song][1].state = 'down'
            
######################################################################
        
    
    def gonext_playpage(self,music_app_self,bke):
        music_app_self.sm.transition.direction = 'up'
        music_app_self.sm.current = "playpage"
    
    def play_pause(self, whjfvwh, btn_self):
        global curr_song, pre_song,pre_sound, song_counter, len_slid, len_btn2, sh, song_position
        global my_fb
        if (btn_self.state == 'normal'):
            try:
                song_position = pre_sound.get_pos()
                sh.cancel()
                pre_sound.stop()
                pre_sound.unload()
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
                sound.seek(song_position)
                sh = slid_func(sound, len_slid, len_btn2, my_fb, song_page_self)
                pre_song = index
                song_counter = index
                pre_sound = sound
                songlist[pre_song][1].state = 'down'
                print(songlist[pre_song][0] + '   :    playing')
        
    def previous_song(self, amdvh, btn_self, main_self,music_app_self):
        global curr_song, pre_song,pre_sound, song_counter, up_btn_self, up_main_self, up_music_app_self
        pre_sound.stop()
        pre_sound.unload()
        songlist[song_counter][1].state = 'normal'
        song_counter = song_counter - 1
        if (song_counter < 0):
            song_counter=0
        song_page.update_info(music_app_self,song_counter , main_self, btn_self)
    
    def next_song(self, ahvdhj, btn_self, main_self,music_app_self):
        global curr_song, pre_song,pre_sound, song_counter, up_btn_self, up_main_self, up_music_app_self
        pre_sound.stop()
        pre_sound.unload()
        songlist[song_counter][1].state = 'normal'
        song_counter = song_counter + 1
        if (song_counter == len(songlist)):
            song_counter=len(songlist) - 1
        song_page.update_info(music_app_self,song_counter , main_self, btn_self)
