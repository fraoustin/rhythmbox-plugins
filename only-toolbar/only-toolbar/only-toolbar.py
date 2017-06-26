#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio
from gi.repository import GLib
from gi.repository.GLib import Variant


class OnlyToolBar(GObject.Object, Peas.Activatable):

    __gtype_name = 'OnlyToolBar'
    object = GObject.property(type=GObject.Object)
    GSETTINGS_KEY = "org.gnome.rhythmbox"
    KEY_SIZE = "size"
    THEME = "HighContrast"
    ICON = "view-fullscreen"
    ICON_SIZE = 24
    MARGIN = 12
    NAME_TOOLBAR = "GtkToolbar"

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings.new(self.GSETTINGS_KEY)
        self.visible = True
        self._app = None
        self._win = None
        self._height = None
        self._visible_button_when_only_toolbar = []
        self._visible_button_when_all = []
        self._visible_buildable_when_only_toolbar = []
        self._visible_buildable_when_all = []

    @property
    def app(self):
        if self._app:
            return self._app
        self._app = self.object.props.application
        return self._app

    @property
    def win(self):
        if self._win:
            return self._win
        self._win = self.object.props.window
        return self._win


    def do_activate(self):
        """ add
            - action
            - menu in view
            - accelerator F12
            - button in toolbar and hide button
            - identified button
            - identified Buildable
        """
        print("%s do_activate" % self.__gtype_name)
        self._action = Gio.SimpleAction.new_stateful("view-only-toolbar", None, GLib.Variant.new_boolean(not self.visible))
        self._action.connect("activate", self.toggle_visibility, None)
        self.win.connect("destroy", self.window_deleted)
        window = self.object.props.window
        window.add_action(self._action)
        item = Gio.MenuItem.new(label="view only toolbar", detailed_action="win.view-only-toolbar")
        self.app.add_plugin_menu_item("view", "view-only-toolbar", item)
        self.app.add_accelerator("F12", "win.view-only-toolbar", None)
        #add compatibility 3.4.1
        self.app.set_accels_for_action("win.view-only-toolbar", ["F12",])
        self._height = self.win.get_size()[1]
        for child in self.win.get_children()[0]:
            if isinstance(child, Gtk.Buildable):
                if child.get_name() == self.NAME_TOOLBAR:
                    self._visible_buildable_when_only_toolbar.append(child)
                    self._visible_button_when_all.append(child.get_children()[-1].get_children()[-1])
                    #add button expand Separator, Box > ToolItem > Button > Image > PixBuf
                    toolbutton = Gtk.ToolItem()
                    child.add(toolbutton)
                    toolbutton.show()
                    box = Gtk.Box()
                    box.set_margin_top(self.MARGIN)
                    box.set_margin_bottom(self.MARGIN)
                    toolbutton.add(box)
                    box.show()
                    button = Gtk.Button()
                    theme = Gtk.IconTheme()
                    theme.set_custom_theme(self.THEME)#Gtk.Settings.get_default().get_property("gtk-icon-theme-name"))
                    pixbuf = theme.load_icon(self.ICON, self.ICON_SIZE, 0)
                    image = Gtk.Image()
                    image.set_from_pixbuf(pixbuf)
                    button.set_image(image)
                    button.connect("clicked", self.toggle_visibility)
                    box.add(button)
                    button.show()
                    self._visible_button_when_only_toolbar.append(toolbutton)
                    for i in self._visible_button_when_only_toolbar:
                        i.hide()
                else:
                    self._visible_buildable_when_all.append(child)

    def do_deactivate(self):
        print("%s do_deactivate" % self.__gtype_name)
        self.app.remove_plugin_menu_item("view", "view-only-toolbar")

    def load_complete(self, *args, **kwargs):
        print("%s load_complete" % self.__gtype_name)

    def window_deleted(self, *args, **kwargs):
        """ svg size initial if view only toolbar"""
        print("%s window_deleted" % self.__gtype_name)
        if not self.visible:
            size = self.settings.get_value(self.KEY_SIZE)
            self.settings.set_value(self.KEY_SIZE, Variant('(ii)',(size[0],self._height)))

    def toggle_visibility(self, action=None, parameter=None, data=None):
        """ toggle visible and co """
        print("%s toggle_visibility" % self.__gtype_name)
        self.visible =  not self.visible
        self._action.change_state(GLib.Variant.new_boolean(not self.visible))
        if not self.visible:
            for i in self._visible_buildable_when_all:
                i.set_visible(False)
            for i in self._visible_button_when_only_toolbar:
                i.show()
            for i in self._visible_button_when_all:
                i.hide()
            self._height = self.win.get_size()[1]
            self.win.resize (self.win.get_size()[0],1)
        else:
            for i in self._visible_buildable_when_all:
                i.show()
            for i in self._visible_button_when_only_toolbar:
                i.hide()
            for i in self._visible_button_when_all:
                i.show()
            self.win.resize(self.win.get_size()[0],self._height)
