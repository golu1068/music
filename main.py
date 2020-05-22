# -*- coding: utf-8 -*-
import numpy as np
#import time
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty, ListProperty, ReferenceListProperty
from glob import glob
from os.path import dirname, join, basename
import os
from functools import partial
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.graphics.context_instructions import Rotate, PopMatrix, PushMatrix
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import BorderImage
from kivy.uix.slider import Slider
from kivy.clock import Clock
from mutagen import File
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import random
from kivy.uix.filechooser import FileChooserListView
#from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform
from os.path import sep, expanduser, isdir
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer, NavigationDrawerToolbar,\
        NavigationDrawerIconButton, NavigationDrawerDivider, NavigationDrawerSubheader
from kivymd.theming import ThemeManager
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDFloatingActionButton as fab
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from all_button import ImgToggleButton_play, ImgButton_pre, ImgButton_next, tbtn, tbtn_new
from parameter import *
from nav_button import play_pause, previous_song, next_song, song_btn
from song_slider import slid_bind, slid_func, next
#from manage_screen import MenuScreen, change_image1
from my_filemanager import MDFileManager, open_filemanager
#from kivymd.uix.filemanager import MDFileManager
from kivy.uix.modalview import ModalView
from kivy.factory import Factory
from song_play import song_page
from update_image import update_image
from kivy.metrics import dp
from my_toolbar import AppBarActionButton, MDBottomAppBar
from navigator_lyt import navigator_lyt, main_lyt_image, song_btn_image
from kivymd.uix.card import MDSeparator
from kivymd.uix.button import MDRoundFlatButton
from mp3_data_extract import data_extract
from kivymd.uix.ripplebehavior import CircularRippleBehavior
##################################################################################
class ItemMenuForFitness(CircularRippleBehavior, ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ItemMenuForFitness, self).__init__(**kwargs)
        print(self)
    
    def bt_img(self, tool_self):
##        self.source = 'images/image_2.jpg'
        self.size_hint = (None,None)
        self.size = (dp(56), dp(56))
        self.pos_hint = {'center_x':0.5, 'center_y': .5}
        self.pos = [50,20]
        self.color = [1,1,1,0]
        self.canvas.children[2].size = [tool_self.size[0]*0,tool_self.size[1]*0]
        with self.canvas:
            Color(1,1,1,.8)
            self.rect4 = RoundedRectangle(radius=[9000],segments=15)
            self.rect4.source = 'images/my_photo.jpg'
        def update_rect(instance, value):
            instance.rect4.pos = instance.pos#[instance.pos[0],instance.pos[1]]
            instance.rect4.size = instance.size#[instance.size[1], instance.size[1]]   
        self.bind(pos=update_rect, size=update_rect)
        
        self.bind(on_release=self.pri)
        
        tool_self.add_widget(self)
        
    def pri(self,cfda):
        print('done')

class my_FloatButton(AnchorLayout):
    callback = ObjectProperty()
    md_bg_color = ListProperty([1, 1, 1, 1])
    icon = StringProperty()
    
class box(NavigationLayout):
    side_panel_width = (
        (dp(320) * 80) // 100 if dp(320) >= Window.width else dp(280))  ## width of side panel
    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self.main_box = BoxLayout(size=Window.size)
        self.main_box.orientation='vertical'
        self.anim_type='slide_above_simple'
#######################################################################  
        self.lyt_image = main_lyt_image(self)
        self.nav_lyt = navigator_lyt(self,self.main_box)  # for navigation layout
        self.nav_lyt.bind(on_press=partial(open_filemanager, music_app, self.main_box))
        self.nav_lyt.bind(on_release= lambda x : self.toggle_nav_drawer())
####################################################################
        gridlayout = GridLayout(cols=1, size_hint_y=None, spacing=1)
        gridlayout.bind(minimum_height = gridlayout.setter('height'))
        dirpath = os.getcwd()
        index=0;
        ##   r'/storage/emulated/0/'
        for dirpath, dir_name, filename in os.walk(r'/storage/emulated/0/'):
            for fn in glob(dirpath + '/*.mp3'):
#                song_text = fn.split('/')[-1:][0][:-4]
                song_button = tbtn_new()
                song_button.bind(on_press = partial(self.gonext,index, self.main_box))
                songlist[index] = [fn, song_button]
#                song_button.canvas.before.children[0].rgba = [1,1,1,0.15] # Background color of button
                #################################################
                song_name, btn_image = data_extract(fn)
                song_button.text = song_name
                ##################################################
                song_btn_image(song_button, btn_image)  ## Image of button
                ####################################################################
                gridlayout.add_widget(song_button)
                index += 1
                
        scrollview = ScrollView()
        scrollview.add_widget(gridlayout)
        self.main_box.add_widget(scrollview)
        
        self.add_widget(self.main_box)

    def gonext(self,index,curr_song_btn, main_self):
        song_page.update_info(self,index, curr_song_btn, music_app)
        music_app.sm.transition.direction = 'up'
        music_app.sm.current = "playpage"

class main(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    def build(self):
        self.sm = ScreenManager(transition=CardTransition(mode='pop',duration=.09))
        self.bo = box()
        m1 = Screen(name='mainscreen')
        m1.add_widget(self.bo)
        self.sm.add_widget(m1)
        ## play screen
        self.play_page  = song_page(music_app)
        m2 = Screen(name='playpage')
        m2.add_widget(self.play_page)
        self.sm.add_widget(m2)
        
        return self.sm
    
if __name__ == '__main__':
    music_app = main()
    music_app.run()