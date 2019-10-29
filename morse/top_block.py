#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Oct 24 13:43:14 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from epy_block_0 import morsecode_enc
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(48e3)
        self.hackRF_samp_rate = hackRF_samp_rate = 960e3
        self.hackRF_freq = hackRF_freq = 432.48e06

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=1,
        	v_offset=0,
        	t_scale=0.01,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0_0.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=1,
        	v_offset=0,
        	t_scale=0.01,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(hackRF_samp_rate/samp_rate),
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(hackRF_samp_rate)
        self.osmosdr_sink_0.set_center_freq(hackRF_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(7, 0)
        self.osmosdr_sink_0.set_gain(20, 0)
        self.osmosdr_sink_0.set_if_gain(30, 0)
        self.osmosdr_sink_0.set_bb_gain(30, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.epy_block_0 = morsecode_enc(wpm=28, samplerate=48000, sleeptime=3, text='SOS')
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 700, 0.9, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.epy_block_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.epy_block_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.epy_block_0, 0), (self.wxgui_scopesink2_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0_0.set_sample_rate(self.samp_rate)

    def get_hackRF_samp_rate(self):
        return self.hackRF_samp_rate

    def set_hackRF_samp_rate(self, hackRF_samp_rate):
        self.hackRF_samp_rate = hackRF_samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.hackRF_samp_rate)

    def get_hackRF_freq(self):
        return self.hackRF_freq

    def set_hackRF_freq(self, hackRF_freq):
        self.hackRF_freq = hackRF_freq
        self.osmosdr_sink_0.set_center_freq(self.hackRF_freq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
