import os
import json
import shutil
import argparse
from tqdm import tqdm
import copy

def split_coco_dataset(coco_dir, target_dir, split, num_images, copy_val_as_train=False):
    """
    Save a specified number of images and their annotations from the COCO dataset.
    
    Args:
        coco_dir (str): Path to the COCO dataset
        target_dir (str): Path to save the results
        num_images (int): Number of images to select
        copy_val_as_train (bool): Whether to copy validation data as training data
    """
    
    source_split = split if copy_val_as_train == False else 'train'
    
    # Set paths
    images_dir = os.path.join(coco_dir, f'{source_split}2017')
    annotation_file = os.path.join(coco_dir, 'annotations', f'instances_{source_split}2017.json')
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Load annotation file
    with open(annotation_file, 'r') as f:
        coco_data = json.load(f)
    
    # Sort images by filename
    images = sorted(coco_data['images'], key=lambda x: x['file_name'])
    
    # Warning if requested number of images exceeds total
    if num_images > len(images):
        print(f"Requested number of images ({num_images}) exceeds the total number of images ({len(images)}).")
        print(f"Using all available images ({len(images)}).")
        selected_images = images
    else:
        # Select specified number of images
        selected_images = images[:num_images]
    
    # Create list of selected image IDs
    selected_image_ids = [img['id'] for img in selected_images]
    
    # Filter annotations for selected images
    selected_annotations = [ann for ann in coco_data['annotations'] 
                           if ann['image_id'] in selected_image_ids]
    
    # Create new COCO data
    new_coco_data = {
        'info': copy.deepcopy(coco_data['info']),
        'licenses': copy.deepcopy(coco_data['licenses']),
        'categories': copy.deepcopy(coco_data['categories']),
        'images': selected_images,
        'annotations': selected_annotations
    }
    
    # Create target directories
    target_images_dir = os.path.join(target_dir, f'{split}2017')
    target_annotations_dir = os.path.join(target_dir, 'annotations')

    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(target_images_dir, exist_ok=True)
    os.makedirs(target_annotations_dir, exist_ok=True)
    
    # Save annotation file
    annotation_path = os.path.join(target_annotations_dir, f'instances_{split}2017.json')
    with open(annotation_path, 'w') as f:
        json.dump(new_coco_data, f)
    
    # Copy image files
    print(f"Copying {len(selected_images)} selected images...")
    for img in tqdm(selected_images):
        src_path = os.path.join(images_dir, img['file_name'])
        dst_path = os.path.join(target_images_dir, img['file_name'])
        print(f"src_path: {src_path}, dst_path: {dst_path}")
        shutil.copy2(src_path, dst_path)
    
    print(f"Completed: {len(selected_images)} images, {len(selected_annotations)} annotations")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract a specified number of images from the COCO dataset.')
    parser.add_argument('--coco_dir', required=True, help='Path to the COCO dataset')
    parser.add_argument('--target_dir', required=True, help='Path to save the results')
    parser.add_argument('--num_images', type=int, required=True, help='Number of images to select')
    parser.add_argument('--copy_val_as_train', action='store_true', help='Copy validation data as training data')
    
    args = parser.parse_args()
    
    if os.path.exists(args.target_dir):
        shutil.rmtree(args.target_dir)
    
    for split in ['train', 'val']:
        split_coco_dataset(args.coco_dir, args.target_dir, split, args.num_images, args.copy_val_as_train)
    print("Processing complete!")
