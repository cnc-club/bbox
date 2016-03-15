#!/usr/bin/env python 

import pygtk
pygtk.require("2.0")
import gtk, gobject
import time
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
import hal
import linuxcnc
import hal_glib
import sys
import gladevcp
import os
import ConfigParser
import gladevcp.hal_mdihistory 
import subprocess
import signal

LINUXCNC_INI = "cutmat.ini"
glade_file = "cutmat.glade"

class Cutmat(object):

	def __init__(self):

		self.builder = gtk.Builder()
		self.builder.add_from_file(glade_file)
		self.builder.connect_signals(self)
		self.connect_signals()
		self.halcomp = hal.component("cutmat")
		panel = gladevcp.makepins.GladePanel( self.halcomp, glade_file, self.builder, None)		
		self.window = self.builder.get_object("window1")
		self.linuxcnc_ini = linuxcnc.ini(LINUXCNC_INI)
		self.window.show()
		self.window.connect("key-press-event", self.on_key_down)		
		self.window.connect("delete-event", self.on_window_destroy)		
		# init cfg
		self.c = linuxcnc.command()
		self.err = linuxcnc.error_channel()	
		# post gui
		print "Cutmat: loading postgui hal file"
		postgui_halfile = self.linuxcnc_ini.find("HAL", "POSTGUI_HALFILE")	
		print 	postgui_halfile
		p = subprocess.Popen(['halcmd', '-i', LINUXCNC_INI, "-f", postgui_halfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		print out, err
		

	def connect_signals(self) :
		self.builder.get_object("window1").connect("destroy",self.quit)

	def abort(self) :
		self.c.abort()
		os.killpg(os.getpgid(self.process.pid), signal.SIGTERM) 		
		
	def on_key_down(self, w, event): 
		key = event.keyval	
		if key == 65307 :	
			self.abort()
		
	def quit(self, *arg) : 
		gtk.main_quit()

	
	def on_window_destroy(self, widget, data=None):
		self.quit()	

if __name__ == "__main__":
	app = Cutmat()
	gtk.main() 

