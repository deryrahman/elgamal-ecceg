import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.elgamal import DialogElgamal
from gui.ecc import DialogECCEG


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Elgamal + ECCEG")
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        label = Gtk.Label()
        label.set_markup("<big><b>Elgamal + ECCEG</b></big>")
        label.set_justify(Gtk.Justification.CENTER)
        label_sub = Gtk.Label("Elgamal and ECCEG encrypt/decrypt")
        separator = Gtk.HSeparator()
        button_video = Gtk.Button(label="Elgamal")
        button_video.connect("clicked", self.on_button_clicked, "elgamal")
        button_audio = Gtk.Button(label="ECCEG")
        button_audio.connect("clicked", self.on_button_clicked, "ecceg")

        grid.attach(label, 0, 0, 2, 2)
        grid.attach(label_sub, 0, 2, 2, 1)
        grid.attach(separator, 0, 3, 2, 1)
        grid.attach(button_audio, 1, 4, 1, 1)
        grid.attach(button_video, 0, 4, 1, 1)

    def on_button_clicked(self, widget, dialog_name):
        dialog = None
        if dialog_name == "elgamal":
            dialog = DialogElgamal(self)
        elif dialog_name == "ecceg":
            dialog = DialogECCEG(self)
        dialog.run()
        dialog.destroy()
