from kivy.graphics import Rectangle
from kivy.core.window import Window
import numpy as np

class update_image():
    def __init__(self, image_path, main_box_self, **kwargs):
        super(update_image, self).__init__(**kwargs)
        path = image_path
        if (path[-4:] == '.jpg' or path[-4:] == '.png' or path[-5:] == '.jpeg'):
            pass
        else:
            return
        with main_box_self.canvas.before:
            main_box_self.rect = Rectangle(pos = main_box_self.pos, 
                                  size =np.array(Window.size))
            main_box_self.rect.source = path
                
        def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
        
        main_box_self.bind(pos=update_rect, size=update_rect)


#    def selection_updated(self, main_lyt, filechooser, selection):            
#            with main_lyt.canvas.before:
#                main_lyt.rect = Rectangle(pos = main_lyt.pos, 
#                                      size =np.array(Window.size))
#                main_lyt.rect.source = selection[0]
#            def update_rect(instance, value):
#                instance.rect.pos = instance.pos
#                instance.rect.size = instance.size
#            
#            main_lyt.bind(pos=update_rect, size=update_rect)