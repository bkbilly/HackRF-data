# HackRF-data

## Objective

The objective of this project is to transfer binary data from one HackRF One to another using a modulation for the transmitter and a demodulation on the receiver. 

There are 3 basic types of modulations:
  - Frequency Modulation
  - Amplitude Modulation
  - Phase Modulation


## Problems

  - We need to use Ubuntu 16.04 as this is the distro that everyone is using in the Robot Community.
  - In order to test the latest version of GNU Radio 3.8 which doesn't support this distro an installation of Ubuntu 18.04 is needed. The build of the newest version was successfully completed, but for the communication with the HackRF One an extra package had to be build from source `gr-osmosdr` which had build errors.
  - HackRF is not that strong and for real life applications it needs a Signal Booster.


## Projects

### FM
This contains a receiver that can graphically change frequency and a transmitter that gets a WAV audio file and sends it to a prespecified frequency. Created it so that we can check how each component of GNU-Radio works together.
#### RDS

### wifi
Checks the 2.4GHz WiFi signals. Created it so that we can check what kind of antena we need for a high frequency receiver.

### morse
Works only on older versions of GNU Radio and contains a python block that reads the input message and transmits it as a morse code. This was the first attempt to send/receive data, though this approch has many problems and mostly because of the timing interval that has to be synchronized. A way to run this is to save the raw data to a wav file and then have an external application decode the wav file. For noisy environments the morse code can be decoded with neural networks with this code: https://github.com/ag1le/LSTM_morse
http://ag1le.blogspot.com/2019/02/training-computer-to-listen-and-decode.html

### cc1111
Sends/Receives binary data from one HackRF to another. It needs compilation from source and the full documentation exists on the project README page.

### OFDM
A deferent approach on the receiver/transmitter problem which is using the official OFDM tx/rx examples. As a modulation it is using timeslots to send multiple signals at the same time.


## Installation

### Install HackRF libraries
```bash
sudo python -m easy_install --upgrade pyOpenSSL
sudo pip install bitstring
sudo apt install hackrf
sudo apt install rtl-sdr
sudo apt install gr-osmosdr
```

### Install GNU Radio 3.8 on Ubuntu 18.04
```bash
git clone --recursive https://github.com/gnuradio/gnuradio.git
cd gnuradio
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ../
make
make test
sudo make install
sudo ldconfig
```

