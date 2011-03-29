from util import prepare_for_display, window_manager, GuiLockError
from scikits.image.io import ImageCollection
import os.path

try:
    # we try to aquire the gui lock first
    # or else the gui import might trample another
    # gui's pyos_inputhook.
    window_manager.acquire('gtk')
except GuiLockError, gle:
    print gle
else:
    try:
        import gtk
        import gtk.glade
    except ImportError:
        print 'pygtk libraries not installed.'
        print 'plugin not loaded.'
        window_manager._release('gtk')
    else:

        class ImageBrowser():

            def __init__(self, image_data):
                self.image_data = image_data
                self.counter = 0

                #Set the Glade file
    		cur_dir = os.path.dirname(__file__)
    		self.gladefile = os.path.join(cur_dir, 'scigui1.glade'
                self.wTree = gtk.glade.XML(self.gladefile) 

                #Get the Main Window, and connect the "destroy" event
                self.window = self.wTree.get_widget("window1")
    
                if (self.window):
                    self.window.connect("destroy", gtk.main_quit)               
                self.window.show()

                dic1 = { "on_next_clicked" : self.btnnext_clicked }
                self.wTree.signal_autoconnect(dic1)
                dic2 = { "on_previous_clicked" : self.btnprevious_clicked }
                self.wTree.signal_autoconnect(dic2)
    
                self.update_image()

            def update_image(self):
                arr = prepare_for_display(self.image_data[self.counter])
                width = arr.shape[1]
                height = arr.shape[0]
                rstride = arr.strides[0]
                pb = gtk.gdk.pixbuf_new_from_data(arr.data,
                                                  gtk.gdk.COLORSPACE_RGB,
                                                  False, 8, width, height,
                                                  rstride)

                self.img = self.wTree.get_widget("image1")
                self.img.set_from_pixbuf(pb)                        
                                    
            def btnnext_clicked(self,widget):
                self.counter = (self.counter + 1) % len(self.image_data)
                self.update_image()
    
            def btnprevious_clicked(self,widget):
                self.counter = (self.counter - 1) % len(self.image_data)
                self.update_image()	
                
        def imshow(image_data):
            if not isinstance(image_data, ImageCollection):
                image_data = ImageCollection([image_data], load_func=lambda x: x)               

            w = ImageBrowser(image_data)


        def _app_show():
            if window_manager.has_windows():
                window_manager.register_callback(gtk.main_quit)
                gtk.main()
            else:
                print 'no images to display'

