import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.window_main import Window

if __name__ == "__main__":
    win = Window()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
