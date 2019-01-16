arecord -D plughw:1,0 -t raw | python3 fft_analyze.py
