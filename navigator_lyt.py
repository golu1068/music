# -*- coding: utf-8 -*-
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer, NavigationDrawerToolbar,\
        NavigationDrawerIconButton, NavigationDrawerDivider, NavigationDrawerSubheader
from kivy.metrics import dp
from parameter import naviagtion_img, default_img
import numpy as np
from kivy.core.window import Window
from my_filemanager import MDFileManager, open_filemanager
#######################################################

def navigator_lyt(self,main_box_self):
#    tool_box = FloatLayout(
#                          size_hint=[1,0.9],
#                          pos=(main_box_self.width, main_box_self.height*0.9))
    tb = MDToolbar(title='',background_palette= 'Primary')
    tb.md_bg_color = [0,0,0,0] 
    tb.left_action_items= [['menu', lambda x : self.toggle_nav_drawer()]]
#    tb.left_action_items= [['menu', lambda x : main_box_self.toggle_nav_drawer()]]
    tb.pos_hint = {'x':0, 'y':0.9}
#        self.tb.size = [self.main_box.width, self.main_box.height*0.1]
#    tool_box.add_widget(tb)
    #########################################################################
    self.nav_drawer = MDNavigationDrawer(spacing=dp(0))
    self.nav_drawer.canvas.children[1].rgba = [1,1,1,0.8]
    self.nav_drawer.canvas.children[3].source = 'images/menu_image.jpg'
#        self.nav_drawer.ids['drawer_title'].text = 'Nagendra'
    self.nav_drawer.ids['drawer_logo'].source = naviagtion_img
    self.nav_drawer.ids['drawer_logo'].color = [1,1,1,0]
##############################################################################
    with self.nav_drawer.ids['drawer_logo'].canvas.after:
        Color(1,1,1,.8)
        self.nav_drawer.ids['drawer_logo'].rect1 = RoundedRectangle(segments=15, radius=[9000])
        self.nav_drawer.ids['drawer_logo'].rect1.source = 'images/my_photo.jpg' # my_photo
        
    def update_rect1(instance, value):
        instance.rect1.pos=[instance.pos[0]+68,instance.pos[1]+30]
        instance.rect1.size = [instance.size[1]*0.8, instance.size[1]*0.8]
#        instance.rect1.pos=[instance.pos[0]+(instance.size[0]-instance.size[1])/2+5,instance.pos[1]+dp(30)]
#        instance.rect1.size = [instance.size[0]*0.6, instance.size[1]*0.75]
#            instance.rect1.radius = [instance.rect1.size[0]-(instance.rect1.size[0])/2]
    self.nav_drawer.ids['drawer_logo'].bind(pos=update_rect1, size=update_rect1)
    
#        ##########################################################
#        nav_sub = NavigationDrawerSubheader(text='sepera')
#        self.nav_drawer.add_widget(nav_sub)
    self.nav_draw_icon1 = NavigationDrawerIconButton(icon='folder',text='Change wallpaper',
                                                     icon_color=[0,0,0,0.5],use_active=False)
#        self.nav_draw_icon1.text_color = [1,0,0,0.1]
#    self.nav_draw_icon1.bind(on_release=partial(open_filemanager))
    self.nav_drawer.add_widget(self.nav_draw_icon1)
    line_sep = NavigationDrawerDivider()
    self.nav_drawer.add_widget(line_sep)

    self.add_widget(self.nav_drawer)
        
#    main_box_self.add_widget(tool_box)
    main_box_self.add_widget(tb)
    
    return self.nav_draw_icon1
    
#    return tool_box
def main_lyt_image(self):
    with self.main_box.canvas.before:
        self.main_box.rect = Rectangle(pos = self.main_box.pos, size =np.array(Window.size))
        self.main_box.rect.source = default_img
    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    self.main_box.bind(pos=update_rect, size=update_rect)

def song_btn_image(song_button, btn_image):
    with song_button.canvas.after:
        song_button.rect3 = RoundedRectangle(radius=[40])
        song_button.rect3.source = btn_image#'images/image_2.jpg'
    def update_rect(instance, value):
        instance.rect3.size = [instance.size[0]*0.15, instance.size[1]*0.8]
        instance.rect3.pos=[instance.pos[0]+dp(15),instance.pos[1]+instance.size[1]*0.1]
#        instance.rect3.pos=[instance.pos[0]+dp(15),instance.pos[1]+dp(21)]
    song_button.bind(pos=update_rect,size=update_rect)
