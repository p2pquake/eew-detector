# eew-detector

Detect announcement of EEW(Earthquake Early Warning) using NHK Radio 1.

## Prerequisites

For pattern matching, two WAVE files are required.

- Chime sound
- Message voice of "Kinkyu-jishin-sokuho-desu （緊急地震速報です）"

## Usage

```bash
arecord -D plughw:1,0 -t raw | python3 fft_analyze.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

