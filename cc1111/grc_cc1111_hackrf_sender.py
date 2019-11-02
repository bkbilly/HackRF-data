#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: grc_cc1111_hackrf_sender
# Author: Jerome Nokin
# Generated: Sat Nov  2 20:14:19 2019
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

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cc1111
import osmosdr
import time
import wx


class grc_cc1111_hackrf_sender(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="grc_cc1111_hackrf_sender")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 800
        self.samp_rate = samp_rate = 2e6
        self.samp_per_sym = samp_per_sym = int(samp_rate / symbole_rate)
        self.preamble = preamble = '0101010101010101'
        self.myqueue_in = myqueue_in = gr.msg_queue(2)
        self.frequency = frequency = 433.6e6
        self.bit_per_sym = bit_per_sym = 1
        self.access_code = access_code = '11010011100100011101001110010001'

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0_1 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
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
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(frequency, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(20, 0)
        self.osmosdr_sink_0.set_if_gain(40, 0)
        self.osmosdr_sink_0.set_bb_gain(40, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=int(samp_per_sym),
        	bt=1,
        	verbose=False,
        	log=False,
        )
        self.cc1111_cc1111_packet_encoder_0 = cc1111.cc1111_packet_mod_base(cc1111.cc1111_packet_encoder(
                        samples_per_symbol=samp_per_sym,
                        bits_per_symbol=bit_per_sym,
                        preamble=preamble,
                        access_code=access_code,
                        pad_for_usrp=True,
        		do_whitening=True,
        		add_crc=True
                ),
        	source_queue=myqueue_in
        	)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.cc1111_cc1111_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))    
        self.connect((self.digital_gmsk_mod_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.digital_gmsk_mod_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.digital_gmsk_mod_0, 0), (self.wxgui_waterfallsink2_0_1, 0))    

    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_myqueue_in(self):
        return self.myqueue_in

    def set_myqueue_in(self, myqueue_in):
        self.myqueue_in = myqueue_in

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_sink_0.set_center_freq(self.frequency, 0)
        self.wxgui_waterfallsink2_0_1.set_baseband_freq(self.frequency)
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency)

    def get_bit_per_sym(self):
        return self.bit_per_sym

    def set_bit_per_sym(self, bit_per_sym):
        self.bit_per_sym = bit_per_sym

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code


def main(top_block_cls=grc_cc1111_hackrf_sender, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
