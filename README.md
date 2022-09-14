# ``Unfold for ZED Stereo Camera``
A Python project for **measuring distance between two ships** with **ZED Stereo Camera**.

Taken from [previous repo without ZED](https://github.com/dandygardad/unfold).

## Requirements
- Python 3.8 or newer
- PyTorch 1.7 or newer
- [ZED SDK](https://www.stereolabs.com/developers/) and its dependencies ([CUDA](https://developer.nvidia.com/cuda-downloads), [OpenCV](https://github.com/opencv/opencv/releases))
- [ZED Python API](https://github.com/stereolabs/zed-python-api)

## Install
```
git clone https://github.com/dandygardad/unfold.git

cd unfold

pip install -r requirements.txt
```

Rename `config.yaml.example` into `config.yaml` and edit the camera & detection config.

```
python main.py
```

## Features
- Live/Video source input
- Detect with YOLOv5 (Mini-version) & Template Matching
- Distance Measurement
- Root Mean Squared Error

---

🌸 from **Dandy Garda**
