# HackRF-data

## Projects
### FM
This contains a receiver that can graphically change frequency and a transmitter that gets a WAV audio file and sends it to a prespecified frequency

### cc1111
Sends/Receives binary data from one HackRF to another.

### morse
Works only on older versions of GNU Radio and contains a python block that reads the input message and transmits it as a morse code.

### wifi
Checks the 2.4GHz WiFi signals. 

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

