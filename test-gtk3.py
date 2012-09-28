#!/usr/bin/env python

import cairo
from gi.repository import Gtk, Gdk

class MyWin (Gtk.Window):
    def __init__(self):
        super(MyWin, self).__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(30)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            print "yay"
            self.set_visual(self.visual)

#        box = Gtk.Box()
#        btn1 = Gtk.Button(label="foo")
#        box.add(btn1)
#        self.add(box)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect('draw', self.da_redraw)
        self.add(self.drawing_area)

        self.set_app_paintable(True)
        self.connect("draw", self.redraw)
        self.connect("delete-event", Gtk.main_quit)
        self.connect('key-press-event', self.draw_something)
        self.first = True
        self.show()

    def da_redraw(self, widget, cr):
        print "drawable area draw"
        self.cr = cr
        print cr
        cr.set_source_rgba(.2, .2, 1.0, 0.9)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def redraw(self, widget, cr):
        print "redraw"
        self.cr = cr
#        if self.first:
#            self.cr = cr
#            self.first = False
        print cr, self.cr
        self.cr.set_source_rgba(.2, .2, .2, 0.9)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.cr.paint()
        self.cr.set_operator(cairo.OPERATOR_OVER)
    
    def draw_something(self, widget, cr):
        print ("\ndraw something")
        cr = self.cr
        self.queue_draw()
        print cr
        cr.set_source_rgba(1.0, .0, .0, 1.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

MyWin()
Gtk.main()

