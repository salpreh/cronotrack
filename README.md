# CLI App for tracking time
[![PyPI version](https://badge.fury.io/py/cronotrack.svg)](https://badge.fury.io/py/cronotrack)
[![PyPI version](https://img.shields.io/github/license/salpreh/cronotrack.svg)](https://img.shields.io/github/license/salpreh/cronotrack.svg)

---
Basic CLI application for tracking time writen in python (stdlib only)

### Installation and usage
You can install the package thrugh `pip`:
```sh
> pip install cronotrack
```
Run the app as an executable module:
```sh
> python -m cronotrack
```
To exit from the app press `q` (or `ctrl+c`)

### Overview
When started the first chrono will be started. From there you can:
- `n`: Finish current chrono and start a new one. A prompt to name the finished task will appear.
- `p`: Pause and resume the current chrono
- `q`: Exit the app

Thats all, pretty simple. At the end of the execution a summary with chrono execution details will be printed.

### App samples
<img src="https://raw.githubusercontent.com/salpreh/cronotrack/master/assets/crtk_1.png" alt="App sample">
<img src="https://raw.githubusercontent.com/salpreh/cronotrack/master/assets/crtk_name.png" alt="App sample (naming chrono)">
<img src="https://raw.githubusercontent.com/salpreh/cronotrack/master/assets/crtk_summ.png" alt="App summary sample">
