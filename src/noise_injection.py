"""
noise_injection.py - Funções para injetar ruído em dados (P23)
"""
import torch
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import random

def flip_labels(labels, flip_ratio=0.1, num_classes=6, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    labels = np.array(labels)
    n_flip = int(len(labels) * flip_ratio)
    flip_indices = np.random.choice(len(labels), size=n_flip, replace=False)
    noisy_labels = labels.copy()
    for idx in flip_indices:
        original = labels[idx]
        wrong_classes = [c for c in range(num_classes) if c != original]
        noisy_labels[idx] = np.random.choice(wrong_classes)
    return noisy_labels, flip_indices

def add_gaussian_noise(image, std=0.1):
    img_array = np.array(image).astype(np.float32) / 255.0
    noise = np.random.normal(0, std, img_array.shape)
    noisy = np.clip(img_array + noise, 0, 1)
    return Image.fromarray((noisy * 255).astype(np.uint8))

def add_blur(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))

def adjust_brightness(image, factor=1.5):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def apply_image_noise(image, noise_type='gaussian', **kwargs):
    if noise_type == 'gaussian':
        return add_gaussian_noise(image, kwargs.get('std', 0.1))
    elif noise_type == 'blur':
        return add_blur(image, kwargs.get('radius', 2))
    elif noise_type == 'brightness':
        return adjust_brightness(image, kwargs.get('factor', 1.5))
    else:
        raise ValueError(f"Tipo de ruído desconhecido: {noise_type}")

def create_imbalanced_split(labels, imbalance_ratio=0.5, majority_classes=None):
    labels = np.array(labels)
    unique_classes = np.unique(labels)
    if majority_classes is None:
        majority_classes = np.random.choice(unique_classes, size=len(unique_classes)//2, replace=False)
    keep_indices = []
    for cls in unique_classes:
        cls_indices = np.where(labels == cls)[0]
        if cls in majority_classes:
            keep_indices.extend(cls_indices)
        else:
            n_keep = int(len(cls_indices) * imbalance_ratio)
            keep = np.random.choice(cls_indices, size=n_keep, replace=False)
            keep_indices.extend(keep)
    return np.sort(keep_indices)
