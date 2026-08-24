# AI Object Detection and Classification Model

This folder contains a real object-detection pipeline built with Ultralytics YOLO. The pretrained YOLO model finds one or more objects, returns a learned bounding box and confidence for each detection, annotates the image, assigns a broad category, and moves the processed image into its category folder.

## Contents

- `my_object_detector.py` - YOLO object detection and sorting script
- `custom_dataset/` - labels and image dataset
- `tf_env/` - bundled Python environment files from the development machine
- `requirements.txt` - Python dependencies

## Requirements

The included `tf_env` directory was created on Windows. For a clean setup on another machine, create a new virtual environment and install the required packages instead of relying on the copied environment:

```powershell
python -m venv tf_env
.\tf_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

Run this command from this folder:

```powershell
python my_object_detector.py
```

The script reads loose images from `custom_dataset/images`. On its first run, Ultralytics downloads `yolo11n.pt`. It detects objects using the COCO-pretrained classes, draws the actual YOLO bounding boxes, creates category directories such as `animals`, `characters_and_art`, `vehicles`, and `others`, saves annotated images there, and removes the original loose files.

## Notes

- The first YOLO run downloads the pretrained `yolo11n.pt` weights.
- COCO does not contain a `building` class, so building-specific detection requires custom training or an open-vocabulary detector.
- The model is pretrained and has not been fine-tuned on this custom dataset; custom accuracy and mAP have not yet been evaluated.
- Keep a backup of the original images before running the sorter because processed loose images are moved into category folders.
- The bundled `tf_env` is platform-specific and is included for project reference; virtual environments are normally recreated per machine.
