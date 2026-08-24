# AI Object Detection and Classification Model

This folder contains a real object-detection pipeline built with Ultralytics YOLO. The pretrained YOLO model finds one or more objects, returns a learned bounding box and confidence for each detection, annotates the image, assigns a broad category, and moves the processed image into its category folder.

## Model Details

### Framework/library

- Ultralytics YOLO
- PyTorch is used by Ultralytics as the deep-learning backend
- OpenCV is used to read and save images
- The model script also uses Python's standard library (`pathlib` and `collections`)

### Dataset

The project contains custom images in `custom_dataset/images`, including animal, building, character/art, vehicle, and other image folders. These images are used as test/input images and are not used to train or fine-tune the detector.

The detector uses the pretrained YOLO11n weights trained on the COCO dataset. Therefore, its learned object classes are COCO classes, not custom classes created from the folder names. The custom folder names are only used for the project's broad category routing.

### Model architecture

This is a pretrained, single-stage YOLO object detector. YOLO11n predicts object classes, confidence scores, and bounding-box coordinates in one inference pass. The script uses the learned YOLO boxes returned by the model; the boxes are not manually generated rectangles.

### Primary groups

The script can output these primary folders:

- `vehicles`
- `animals`
- `characters_and_art`
- `others`

The `buildings` folder is present in the custom dataset, but `buildings` is not currently a reachable output group because the COCO label-to-group mapping contains no building labels. Building detection would require custom training or an open-vocabulary detector.

### Performance

No custom evaluation has been completed yet. Accuracy, precision, recall, F1-score, and mAP are therefore **not yet evaluated** for this project. The confidence value printed by YOLO is a detection confidence, not the accuracy of the model on this custom image collection.

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
