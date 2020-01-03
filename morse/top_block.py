#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Jan  3 19:22:34 2020
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

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
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
        self.volume = volume = 0.2
        self.variable_sample_rate_0 = variable_sample_rate_0 = 2.048E6
        self.transition = transition = 1e6
        self.samp_rate = samp_rate = int(32e3)
        self.quadrature = quadrature = 500e3
        self.hackRF_samp_rate = hackRF_samp_rate = 32e3
        self.cutoff = cutoff = 100e3
        self.audio_dec = audio_dec = 10
        self.FM_freq = FM_freq = 107.9e6

        ##################################################
        # Blocks
        ##################################################
        self._variable_sample_rate_0_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.variable_sample_rate_0,
        	callback=self.set_variable_sample_rate_0,
        	label="Sample Rate: 1.024M, 1.4M, 1.8M, 1.92M, 2.048M, 2.4M & 2. 56M",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._variable_sample_rate_0_text_box, 7, 0, 1, 5)
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label="Volume",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0.2,
        	maximum=1,
        	num_steps=4,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(variable_sample_rate_0/quadrature),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=int(quadrature/1e3/audio_dec),
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, variable_sample_rate_0, cutoff, transition, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink("/home/bkbilly/Desktop/morse.wav", 1, samp_rate, 8)
        self.audio_sink_0_0 = audio.sink(samp_rate, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quadrature,
        	audio_decimation=audio_dec,
        )
        self.RTL820T = osmosdr.source( args="numchan=" + str(1) + " " + "hackrf=1" )
        self.RTL820T.set_sample_rate(samp_rate)
        self.RTL820T.set_center_freq(FM_freq, 0)
        self.RTL820T.set_freq_corr(0, 0)
        self.RTL820T.set_dc_offset_mode(0, 0)
        self.RTL820T.set_iq_balance_mode(0, 0)
        self.RTL820T.set_gain_mode(False, 0)
        self.RTL820T.set_gain(30, 0)
        self.RTL820T.set_if_gain(20, 0)
        self.RTL820T.set_bb_gain(20, 0)
        self.RTL820T.set_antenna("", 0)
        self.RTL820T.set_bandwidth(0, 0)
          

        ##################################################
        # Connections
        ##################################################
        self.connect((self.RTL820T, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_wavfile_sink_0_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_0, 0))    

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)

    def get_variable_sample_rate_0(self):
        return self.variable_sample_rate_0

    def set_variable_sample_rate_0(self, variable_sample_rate_0):
        self.variable_sample_rate_0 = variable_sample_rate_0
        self._variable_sample_rate_0_text_box.set_value(self.variable_sample_rate_0)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.variable_sample_rate_0, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

    def get_transition(self):
        return self.transition

    def set_transition(self, transition):
        self.transition = transition
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.variable_sample_rate_0, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.RTL820T.set_sample_rate(self.samp_rate)

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature

    def get_hackRF_samp_rate(self):
        return self.hackRF_samp_rate

    def set_hackRF_samp_rate(self, hackRF_samp_rate):
        self.hackRF_samp_rate = hackRF_samp_rate

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.variable_sample_rate_0, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

    def get_audio_dec(self):
        return self.audio_dec

    def set_audio_dec(self, audio_dec):
        self.audio_dec = audio_dec

    def get_FM_freq(self):
        return self.FM_freq

    def set_FM_freq(self, FM_freq):
        self.FM_freq = FM_freq
        self.RTL820T.set_center_freq(self.FM_freq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
