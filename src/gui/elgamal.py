# from gui.handler import encode, decode, psnr
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from elgamal.key_generator import generate_random_prime, generate_public_key
from elgamal import elgamal
import utils
import json
import textwrap


def generate_and_save(button, prime_entry, g_entry, private_key_entry,
                      save_path):
    p = int(prime_entry.get_text())
    g = int(g_entry.get_text())
    x = int(private_key_entry.get_text())
    try:
        res = generate_public_key(g, x, p)
        with open(save_path.get_text() + '.pub', 'w') as f:
            json.dump(res, f)
        with open(save_path.get_text() + '.pri', 'w') as f:
            json.dump({'x': x}, f)
    except Exception as e:
        print(e)


def open_key(widget, public_key_entry):
    path = widget.get_filename()
    with open(path, 'r') as f:
        line = f.readlines()[0]
        public_key_entry.set_text(line)


def file_select(widget, plain_text):
    path = widget.get_filename()
    with open(path, 'rb') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.decode("utf-8"), lines))
        text = ''.join(lines)
        plain_text.set_text(text)


def encrypt(button, public_key_entry, k_entry, plain_text, buffer, data):
    k = int(k_entry.get_text())
    public_key = json.loads(public_key_entry.get_text())
    plain = utils.to_numpy_array(plain_text.get_text())
    result = elgamal.encrypt(plain, public_key, k)
    result = utils.int_to_hex(result)
    data['text'] = result
    lines = textwrap.wrap(result, 60)
    if len(lines) > 10:
        result = 'cipher text to large. use save'
    else:
        result = '\n'.join(lines)
    buffer.set_text(result, -1)


def decrypt(button, public_key_entry, private_key_entry, cipher_text, buffer,
            data):
    private_key = json.loads(private_key_entry.get_text())
    public_key = json.loads(public_key_entry.get_text())
    cipher = utils.hex_to_int(cipher_text.get_text())
    result = elgamal.decrypt(cipher, private_key, public_key['p'])
    result = utils.to_string(result)
    data['text'] = result
    lines = textwrap.wrap(result, 60)
    if len(lines) > 10:
        result = 'plain text to large. use save'
    else:
        result = '\n'.join(lines)
    buffer.set_text(result, -1)


def save_to_file(button, data, save_path):
    path = save_path.get_text()
    with open(path, 'w') as f:
        f.write(data['text'])


class DialogElgamal(Gtk.Dialog):

    def __init__(self, parent):
        self.data = {}
        Gtk.Dialog.__init__(self, "Elgamal", parent, 0)
        self.set_border_width(10)

        box = self.get_content_area()
        notebook = Gtk.Notebook()
        box.add(notebook)

        page1 = self.key_generator_page()
        page1.set_border_width(10)
        notebook.append_page(page1, Gtk.Label('Key Generator'))

        page2 = self.encrypt_decrypt_page(True)
        page2.set_border_width(10)
        notebook.append_page(page2, Gtk.Label('Encrypt'))

        page3 = self.encrypt_decrypt_page(False)
        page3.set_border_width(10)
        notebook.append_page(page3, Gtk.Label('Decrypt'))

        notebook.connect('switch-page', self.callback_tab)

        self.show_all()

    def callback_tab(self, notebook, tab, index):
        if index == 0:
            print("KEY PAGE")
        elif index == 1:
            print("ENCRYPT PAGE")
        else:
            pass

    def key_generator_page(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        prime_info = Gtk.Label("suggested prime number: {}".format(
            generate_random_prime()))
        prime_entry = Gtk.Entry()
        g_entry = Gtk.Entry()
        private_key_entry = Gtk.Entry()

        save_path = Gtk.Entry()

        button_generate = Gtk.Button.new_with_label("Generate & Save")
        button_generate.connect("clicked", generate_and_save, prime_entry,
                                g_entry, private_key_entry, save_path)

        grid.attach(prime_info, 0, 0, 4, 1)
        grid.attach(Gtk.Label("Prime Number"), 0, 1, 1, 1)
        grid.attach(prime_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("G Number"), 0, 2, 1, 1)
        grid.attach(g_entry, 1, 2, 3, 1)
        grid.attach(Gtk.Label("Private Key"), 0, 3, 1, 1)
        grid.attach(private_key_entry, 1, 3, 3, 1)

        grid.attach(Gtk.Label("Save File Path"), 0, 4, 1, 1)
        grid.attach(save_path, 1, 4, 3, 1)

        grid.attach(button_generate, 0, 5, 4, 1)

        return grid

    def encrypt_page(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        public_key_entry = Gtk.Entry()
        public_key_open = Gtk.FileChooserButton("Open File")
        public_key_open.set_width_chars(15)
        public_key_open.connect("selection-changed", open_key, public_key_entry)

        plain_text = Gtk.Entry()
        buffer = Gtk.TextBuffer()
        cipher_text = Gtk.TextView(buffer=buffer)
        cipher_text.set_editable(False)

        file_open = Gtk.FileChooserButton("Open File")
        file_open.set_width_chars(15)
        file_open.connect("selection-changed", file_select, plain_text)

        save_path = Gtk.Entry()
        data = {'text': ""}
        save_to = Gtk.Button.new_with_label("Save to File")
        save_to.connect("clicked", save_to_file, data, save_path)

        k_entry = Gtk.Entry()

        button_encrypt = Gtk.Button.new_with_label("Encrypt!")
        button_encrypt.connect("clicked", encrypt, public_key_entry, k_entry,
                               plain_text, buffer, data)

        grid.attach(Gtk.Label("Public Key"), 0, 0, 1, 1)
        grid.attach(public_key_entry, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Open public key"), 0, 1, 1, 1)
        grid.attach(public_key_open, 1, 1, 3, 1)
        grid.attach(Gtk.Label("K value"), 0, 2, 1, 1)
        grid.attach(k_entry, 1, 2, 3, 1)
        grid.attach(Gtk.Label("Open file"), 0, 3, 1, 1)
        grid.attach(file_open, 1, 3, 3, 1)
        grid.attach(Gtk.Label("Plain text"), 0, 4, 4, 1)
        grid.attach(plain_text, 0, 5, 4, 1)
        grid.attach(Gtk.Label("Cipher text"), 0, 6, 4, 1)
        grid.attach(cipher_text, 0, 7, 4, 1)
        grid.attach(button_encrypt, 0, 8, 4, 1)
        grid.attach(Gtk.Label("Save Path"), 0, 9, 1, 1)
        grid.attach(save_path, 1, 9, 3, 1)
        grid.attach(save_to, 0, 10, 4, 1)

        return grid

    def encrypt_decrypt_page(self, is_encrypt):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        public_key_entry = Gtk.Entry()
        private_key_entry = Gtk.Entry()
        public_key_open = Gtk.FileChooserButton("Open File")
        public_key_open.set_width_chars(15)
        public_key_open.connect("selection-changed", open_key, public_key_entry)

        private_key_open = Gtk.FileChooserButton("Open File")
        private_key_open.set_width_chars(15)
        private_key_open.connect("selection-changed", open_key,
                                 private_key_entry)

        plain_text = Gtk.Entry()
        buffer = Gtk.TextBuffer()
        cipher_text = Gtk.TextView(buffer=buffer)
        cipher_text.set_editable(False)

        file_open = Gtk.FileChooserButton("Open File")
        file_open.set_width_chars(15)
        file_open.connect("selection-changed", file_select, plain_text)

        save_path = Gtk.Entry()
        data = {'text': ""}
        save_to = Gtk.Button.new_with_label("Save to File")
        save_to.connect("clicked", save_to_file, data, save_path)

        k_entry = Gtk.Entry()

        button_encrypt = Gtk.Button.new_with_label("Encrypt!")
        button_encrypt.connect("clicked", encrypt, public_key_entry, k_entry,
                               plain_text, buffer, data)
        button_decrypt = Gtk.Button.new_with_label("Decrypt!")
        button_decrypt.connect("clicked", decrypt, public_key_entry,
                               private_key_entry, plain_text, buffer, data)

        grid.attach(Gtk.Label("Public Key"), 0, 0, 1, 1)
        grid.attach(public_key_entry, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Open public key"), 0, 1, 1, 1)
        grid.attach(public_key_open, 1, 1, 3, 1)

        if is_encrypt:
            grid.attach(Gtk.Label("K value"), 0, 2, 1, 1)
            grid.attach(k_entry, 1, 2, 3, 1)
            grid.attach(Gtk.Label("Open file"), 0, 3, 1, 1)
            grid.attach(file_open, 1, 3, 3, 1)
            grid.attach(Gtk.Label("Plain text"), 0, 4, 4, 1)
            grid.attach(plain_text, 0, 5, 4, 1)
            grid.attach(Gtk.Label("Cipher text"), 0, 6, 4, 1)
            grid.attach(cipher_text, 0, 7, 4, 1)
            grid.attach(button_encrypt, 0, 8, 4, 1)
            grid.attach(Gtk.Label("Save Path"), 0, 9, 1, 1)
            grid.attach(save_path, 1, 9, 3, 1)
            grid.attach(save_to, 0, 10, 4, 1)
        else:
            grid.attach(Gtk.Label("Private Key"), 0, 2, 1, 1)
            grid.attach(private_key_entry, 1, 2, 3, 1)
            grid.attach(Gtk.Label("Open private key"), 0, 3, 1, 1)
            grid.attach(private_key_open, 1, 3, 3, 1)
            grid.attach(Gtk.Label("Open file"), 0, 4, 1, 1)
            grid.attach(file_open, 1, 4, 3, 1)
            grid.attach(Gtk.Label("Cipher text"), 0, 5, 4, 1)
            grid.attach(plain_text, 0, 6, 4, 1)
            grid.attach(Gtk.Label("Plain text"), 0, 7, 4, 1)
            grid.attach(cipher_text, 0, 8, 4, 1)
            grid.attach(button_decrypt, 0, 9, 4, 1)
        return grid