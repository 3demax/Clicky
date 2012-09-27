#!/usr/bin/env python
from pyatspi import Registry as registry
from pyatspi import (KEY_SYM, KEY_PRESS, KEY_PRESSRELEASE, KEY_RELEASE)
#import pygtk
#pygtk.require('2.0')
import sys, cairo

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


from time import sleep

class App(gtk.Window):

    iteration = -1
    hack_iteration = 0
    dx = 0
    dy = 0
    history = {}
    reverse_dict = {
        '1': 7, '2': 8, '3': 9,
        '4': 4, '5': 5, '6': 6,
        '7': 1, '8': 2, '9': 3,
    }
    def __init__(self, argv):
        super(App, self).__init__()
#        self.cr = self.win.cairo_create()
        self.set_decorated(False)
#        win.set_size_request(100, 100)
        self.fullscreen()
#        gdk.flush()
        # This sets the windows colormap, so it supports transparency.
        # This will only work if the wm support alpha channel
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.set_app_paintable(True)

        self.drawing_area = gtk.DrawingArea()
        
        self.drawing_area.connect('draw', self.redraw)
        self.connect("delete-event", gtk.main_quit)
        self.connect('key-press-event', self.select)
        
        self.add(self.drawing_area)
        self.show_all()
        gtk.main()

    def redraw(self, widget, cr):
        print "redraw"
        self.cr = cr
        print self.get_size()
        self.w, self.h = self.get_size()
        if self.hack_iteration == 0:
            self.hack_iteration +=1
        elif self.hack_iteration == 1:
            self.down()

    def rectangle(self, cr, x1, y1, x2, y2):
        cr.move_to(x1, y1)
        cr.line_to(x2, y1)
        cr.move_to(x2, y1)
        cr.line_to(x2, y2)
        cr.move_to(x2, y2)
        cr.line_to(x1, y2)
        cr.move_to(x1, y2)
        cr.line_to(x1, y1)

    def draw_grid(self, x, y, w, h):
#        import ipdb; ipdb.set_trace()
        cr = self.cr
        print cr
#        gdk.flush()
#        self.draw(cr)
#        cr.set_operator(cairo.OPERATOR_CLEAR)
#        cr.paint()
##        cr.rectangle(0.0, 0.0, self.w, self.h)
##        cr.fill()
#        cr.set_operator(cairo.OPERATOR_OVER)
        
        cr.set_source_rgba(0.0,1.0,1.0,0.1)
        cr.paint()
#        cr.rectangle(0.0, 0.0, self.w, self.h)
#        cr.fill()
        
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.rectangle(int(x), int(y), int(w), int(h))
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgba(0.0,0.0,0.0,0.2)
        cr.rectangle(int(x), int(y), int(w), int(h))
        cr.fill()
        
#        import ipdb; ipdb.set_trace()
        border = (w/500 + 0.1)
        print "draw", x, y, w, h, "border", border
        cr.set_line_width(border)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        
        for i in range (0,3):
            for j in range(0,3):
                x1 = int(i*w/3) + x
                y1 = int(j*h/3) + y
                x2 = int( (i+1)*w/3 ) + x
                y2 = int( (j+1)*h/3 ) + y
                self.rectangle(cr, x1, y1, x2, y2)
        cr.stroke()
        
#        self.drawing_area.queue_draw()
#        import ipdb; ipdb.set_trace()
        

    def get_rectangle_size(self):
        return self.w*(1./3**self.iteration), self.h*(1./3**self.iteration)
        
    def widow_hide(self):
        self.hide()
        gdk.flush()
    
    def signum(self, x):
        return (x > 0) - (x < 0)

    def get_center(self):
        w, h = self.get_rectangle_size()
        return (self.dx + w/2, self.dy + h/2)

    def click (self, button = 1):
        self.widow_hide()
        x,y = self.get_center()
        registry.generateMouseEvent(x, y, 'b%sc' % button)
        
    def double_click(self, button = 1):
        self.widow_hide()
        x,y = self.get_center()
        registry.generateMouseEvent(x, y, 'b%sd' % button)
        
    def point(self):
        x,y = self.get_center()
        registry.generateMouseEvent(x, y, 'abs')

    def down(self, choice=1, iteration=None):
        print "down iteration", self.iteration
        self.iteration += 1
        if iteration is not None:
            self.iteration = iteration
        w, h = self.get_rectangle_size()
        dx =(self.dx + (choice-1)%3*w)*self.signum(self.iteration)
        dy =(self.dy + (choice-1)/3*h)*self.signum(self.iteration)
        self.history[str(self.iteration)] = (dx, dy,choice)
        self.draw_grid(dx, dy, w, h)
        self.dx, self.dy = dx, dy
        self.point()
        return (w/2, h/2)

    def up(self):
        try:
            dx, dy, choice = self.history[str(self.iteration-1)]
            self.iteration -=1
            w, h = self.get_rectangle_size()
            self.draw_grid(dx, dy, w, h)
            self.dx, self.dy = dx, dy
            self.point()
        except KeyError:
            pass
    
    def select(self, widget, event):
        print "select", event.keyval
        key = event.keyval
#        import ipdb; ipdb.set_trace()
        gtk.keysyms = gdk
        if key == gtk.keysyms.KEY_Escape:
            gtk.main_quit()
        elif key == gtk.keysyms.KEY_space or key == gtk.keysyms.KEY_KP_Enter or key == gtk.keysyms.KEY_KP_Equal:
            self.click()
            gtk.main_quit()
        elif key == gtk.keysyms.KEY_KP_0:
            self.double_click()
            gtk.main_quit()
        elif key == gtk.keysyms.KEY_KP_Decimal:
            self.click(button=3)
            gtk.main_quit()
        elif key == gtk.keysyms.KEY_BackSpace:
            self.up()
        elif gtk.keysyms.KEY_KP_1 <= key <= gtk.keysyms.KEY_KP_9:
            
#            self.cr = widget.window.cairo_create()
            num = event.keyval - gtk.keysyms.KEY_KP_1 + 1
            self.down(self.reverse_dict[str(num)])
        elif key == gtk.keysyms.KEY_Home:
            self.down(iteration=0)
        else:
            pass


if __name__ == "__main__":
    app = App(sys.argv)
