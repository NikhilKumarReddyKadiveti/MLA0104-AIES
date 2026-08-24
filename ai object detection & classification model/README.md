# AI Object Detection and Classification Model

This folder contains an image classification pipeline built with TensorFlow and MobileNetV3Large. The script scans loose images in `custom_dataset/images`, predicts ImageNet labels, assigns a broad category, draws a confidence-based bounding box, and moves the processed image into its category folder.

## Contents

- `my_object_detector.py` - main classification and sorting script
- `custom_dataset/` - labels and image dataset
- `tf_env/` - bundled Python environment files from the development machine

## Requirements

The included `tf_env` directory was created on Windows. For a clean setup on another machine, create a new virtual environment and install the required packages instead of relying on the copied environment:

```powershell
python -m venv tf_env
.\tf_env\Scripts\Activate.ps1
python -m pip install tensorflow opencv-python numpy
```

## Run

Run this command from this folder:

```powershell
python my_object_detector.py
```

The script reads images from `custom_dataset/images`. It creates category directories such as `animals`, `buildings`, `characters_and_art`, `vehicles`, and `others`, saves the annotated images there, and removes the original loose files.

## Notes

- The first TensorFlow run may download MobileNetV3 ImageNet weights.
- Keep a backup of the original images before running the sorter because processed loose images are moved into category folders.
- The bundled `tf_env` is platform-specific and is included for project reference; virtual environments are normally recreated per machine.
