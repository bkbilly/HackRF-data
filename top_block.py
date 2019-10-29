#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Oct 24 16:08:27 2019
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

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
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
        self.samp_rate = samp_rate = 2.6e6
        self.freq = freq = 2.445e9

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0_1_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=5120,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Source",
        	win=window.rectangular,
        )
        self.Add(self.wxgui_waterfallsink2_0_1_0.win)
        self.wxgui_waterfallsink2_0_1 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=5120,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Source",
        	win=window.rectangular,
        )
        self.Add(self.wxgui_waterfallsink2_0_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "hackrf" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(20, 0)
        self.osmosdr_source_0.set_if_gain(40, 0)
        self.osmosdr_source_0.set_bb_gain(40, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 250e3, 1.25e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(10e-3, 210e-3, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((2, ))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-500e-3, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.blocks_throttle_1, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_waterfallsink2_0_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_throttle_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_waterfallsink2_0_1_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 250e3, 1.25e3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.wxgui_waterfallsink2_0_1.set_baseband_freq(self.freq)
        self.wxgui_waterfallsink2_0_1_0.set_baseband_freq(self.freq)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
