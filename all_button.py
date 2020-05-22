from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
#############################################################################
class ImgToggleButton_play(ToggleButtonBehavior, Image):
    def __init__(self, img_normal, img_down,**kwargs):
        super(ImgToggleButton_play, self).__init__(**kwargs)
        self.size_hint= (0.33, 0.7)
        self.pos_hint= {"x":0.33,"top":1}
        self.background_normal=''
        self.background_color=(1,1,1,1)
        self.source = img_normal
        self.mipmap = True
        self.img_normal = img_normal
        self.img_down = img_down

    def on_state(self, widget, value):
        print(value)
        if value == 'down':
            self.source = self.img_down
        else:
            self.source = self.img_normal

class ImgButton_pre(ButtonBehavior, Image):
    def __init__(self, img_normal, img_press, **kwargs):
        super(ImgButton_pre, self).__init__(**kwargs)
        self.size_hint= (0.30, 0.7)
        self.pos_hint= {"left":1,"top":1}
        self.background_normal=''
        self.background_color=(1,0,1,1)
        self.normal = img_normal
        self.press = img_press
        self.source = self.normal
        self.allow_stretch = True
        self.mipmap = False
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal
class ImgButton_next(ButtonBehavior, Image):
    def __init__(self, img_normal, img_press, **kwargs):
        super(ImgButton_next, self).__init__(**kwargs)
        self.size_hint= (0.33,0.7)
        self.pos_hint= {"right":1,"top":1}
        self.background_normal=''
        self.background_color=(1,1,1,1)
        self.normal = img_normal
        self.press = img_press
        self.source = self.normal
        self.allow_stretch = True
        self.mipmap = False
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal
        
class tbtn(ToggleButton):
    global curr_song, pre_song
    def __init__(self, song_index, **kwargs):
        super(tbtn, self).__init__(**kwargs)
        self.song = song_index
        self.background_normal=''
        self.background_color=(0,0,0,0.2)
        self.color=(0,0,1,1)
        self.size_hint=(1,None)
        self.pos_hint = (1,None)
        self.size = (self.width,self.height*2)
        self.group = 'song_button'
        self.border = (1,1,1,1)
        self.pos = (0,self.height/2)

    def on_state(self, instance, value):
        if value == 'down':
          list(self.children)[0].color = (0,0,1,0.5)
        else:
           list(self.children)[0].color = (1,1,1,1)

class tbtn_new(ToggleButton):
    global curr_song, pre_song
    def __init__(self, **kwargs):
        super(tbtn_new, self).__init__(**kwargs)
#        self.song = song_index
        self.background_normal=''
        self.background_color=(0,0,0,0.2)
        self.color=(1,1,1,1)
        self.size_hint=(1,None)
        self.pos_hint = (1,None)
        self.size = (self.width,self.height*2)
        self.group = 'song_button'
        self.border = (1,0,1,1)
        self.pos = (0,self.height/2)
        self.text_size = (self.width*5, None)
        self.valign = 'middle'
        self.halign = 'left'
        self.shorten = True
        self.shorten_from = 'right'
        self.markup = True
        
#        self.lbl_txt.text_size = (self.width*6, None)
#        self.lbl_txt.text_color = [1,1,1,1]
#        self.lbl_txt.valign = 'middle'
#        self.lbl_txt.halign = 'left'
#        self.lbl_txt.shorten = True
#        self.lbl_txt.shorten_from = 'right'
#        print(dir(self))
    def on_state(self, instance, value):
        if value == 'down':
            print(self.text)
            self.color = [0,0,1,0.5]
#          list(self.children)[0].color = (0,0,1,0.5)
        else:
            self.color = [1,1,1,1]
#           list(self.children)[0].color = (1,1,1,1)

######################################################################