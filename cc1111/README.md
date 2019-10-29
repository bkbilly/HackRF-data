Documentation
=============
- Some more explanations can be found here: http://funoverip.net/2014/07/gnu-radio-cc1111-packets-encoderdecoder-blocks/

Installation
============

```bash
sudo apt install swig
git clone https://github.com/funoverip/gr-cc1111.git
cd gr-cc1111/src/gr-cc1111/
mkdir build
cd build
cmake ../
make
sudo make install
```

Fix
============
Remove the `._hr` on line 139:
```bash
sudo vi /usr/local/lib/python2.7/dist-packages/cc1111/cc1111_packet.py
```