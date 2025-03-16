# COCO128

Small subsets of the COCO2017 dataset for CI/CD testing, debugging, and faster experiment

`train2017` and `val2017` have the same images.

## split_coco.py

A utility script for creating smaller subsets of the COCO (Common Objects in Context) dataset, useful for prototyping, testing, or working with limited computational resources.

### Overview

This script allows you to extract a specified number of images and their corresponding annotations from the COCO dataset, preserving the original format and structure. It handles both training and validation splits.

### Features

- Extract a configurable number of images from the COCO dataset
- Preserve all associated annotations for the selected images
- Maintain COCO's JSON format for annotations
- Support for both training and validation splits
- Option to copy validation data as training data when needed

### Requirements

- Python 3.6+
- Required packages:
  - `tqdm`: For progress display
  - Standard libraries: `os`, `json`, `shutil`, `argparse`, `copy`

### Installation

Clone this repository or download the script. Install the required packages:

```bash
pip install tqdm
```

### Usage

Basic usage:

```bash
python split_coco.py --coco_dir /path/to/coco --target_dir /path/to/output --num_images 1000
```

### Arguments

- `--coco_dir` (required): Path to the original COCO dataset
- `--target_dir` (required): Path where the subset should be saved
- `--num_images` (required): Number of images to select for each split (train/val)
- `--copy_val_as_train` (optional): Use training data for validation split 

Uploaded dataset is processed with `--num_images 128` and `--copy_val_as_train` options.

### Example

To create a subset with 500 images from each split:

```bash
python split_coco.py --coco_dir /datasets/coco --target_dir /datasets/coco_small --num_images 500
```

### Notes

- The script selects images in order after sorting by filename
- If the requested number of images exceeds the available images, all available images will be used
- The target directory will be cleared if it already exists
- Both image files and annotation files are copied to maintain the same structure as the original dataset

### Expected Directory Structure

Expected input COCO structure:
```
/path/to/coco/
├── train2017/
├── val2017/
└── annotations/
    ├── instances_train2017.json
    └── instances_val2017.json
```

Output structure will be the same but with fewer images and updated annotation files.

### License

Use this script according to the license terms of the COCO dataset.

## References
- https://github.com/giddyyupp/coco-minitrain
- https://github.com/chongruo/tiny-coco
- https://www.kaggle.com/datasets/ultralytics/coco128