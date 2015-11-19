# ------------------------------------ #
# File: main.py                        #
# Brief: A simple demonstration      / #
# / application for the PyGtk (2.0)  / #
# / library.                           #
# Author: Philipp Schaad               #
# Creation Date: 191115                #
# Copyright: *LICENSE.txt*             #
# ------------------------------------ #

import sys
import string

from gi.repository import Gtk

# Main application class.
class HelloWorld:

    # Callback method, prints to console.
    def hello(self, widget, data=None):
        # Simply print out a console message.
        print("Hello World")

    # Callback for the delete-event. Propagate it, without action.
    def delete_event(self, widget, event, data=None):
        # Allow propagation of delete event to destroy.
        return False

    # Callback for the window destroy event.
    def destroy(self, widget, data=None):
        # Exit the Application.
        Gtk.main_quit();

    # Callback for the popup event.
    def open_popup(self, widget, data=None):
        self.popup_window.display()

    # Initialization method for the HelloWorld class.
    def __init__(self):
        # Initialize the main application window.
        self.main_window = Gtk.Window()
        self.main_window.connect("delete_event", self.delete_event)
        self.main_window.connect("destroy", self.destroy)
        self.main_window.set_title("Sample GTK Application")
        self.main_window.set_border_width(10)

        # Create the popup window.
        self.popup_window = PopupWindow()
        
        # Set up the content holding box. (vertical)
        self.button_holder = Gtk.VBox()

        # Set up the hello-world button.
        self.hello_button = Gtk.Button("Hi!")
        self.hello_button.connect("clicked", self.hello, None)

        # Set up the quit button.
        self.quit_button = Gtk.Button("Quit")
        self.quit_button.connect_object(
                "clicked", Gtk.Widget.destroy, self.main_window)

        # Set up the popup button.
        self.popup_button = Gtk.Button("Popup!")
        self.popup_button.connect("clicked", self.open_popup)

        # Add all elements to the main window and display everything. 
        # Packing detail: Expand - true, Fill - true, Padding - 5px.
        self.button_holder.pack_start(
                self.hello_button, True, True, 5)
        self.button_holder.pack_start(
                self.popup_button, True, True, 5)
        self.button_holder.pack_start(
                self.quit_button, True, True, 5)
        self.main_window.add(self.button_holder)
        self.main_window.show_all()

    # Main method for the HelloWorld class.
    def main(self):
        Gtk.main()


# A simple popup window.
class PopupWindow:

    # Callback for the delete-event. Hide the window again.
    def delete_event(self, widget, data=None):
        self.main_window.hide()
        return True

    # Method to display the popup.
    def display(self):
        self.main_window.show_all()

    # Initialize the window
    def __init__(self):
        # Initialize the window.
        self.main_window = Gtk.Window()
        self.main_window.connect("delete_event", self.delete_event)
        self.main_window.set_title("Popup!")
        self.main_window.set_border_width(10)

        # Create a label to add to the popup.
        self.message = Gtk.Label("You opened a popup. Congratulations!")

        self.main_window.add(self.message)


# ========================================================= #

# Entry point method. 
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
