"""
data_loader.py - DataLoaders para os 3 datasets
"""

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from pathlib import Path
import numpy as np
from PIL import Image
import os


class PlantDiseaseDataset(Dataset):
    """
    Dataset genérico para imagens de plantas organizadas em pastas por classe
    
    Estrutura esperada:
        data/train/
            ├── classe_0/
            │   ├── img_0.jpg
            │   ├── img_1.jpg
            │   └── ...
            ├── classe_1/
            │   ├── img_0.jpg
            │   └── ...
            └── ...
    """
    
    def __init__(self, root_dir, split="train", img_size=224, transform=None):
        """
        Args:
            root_dir: Caminho raiz do dataset (ex: "data/train")
            split: "train", "val" ou "test"
            img_size: Tamanho das imagens (224 para CNN, 64 para MLP)
            transform: Transformações adicionais
        """
        self.root_dir = Path(root_dir)
        self.img_size = img_size
        
        # Transformações padrão
        if transform is None:
            self.transform = transforms.Compose([
                transforms.Resize((img_size, img_size)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
        else:
            self.transform = transform
        
        # Mapear classes
        self.classes = sorted([d.name for d in self.root_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        
        # Carregar lista de imagens
        self.images = []
        self.labels = []
        
        for class_name in self.classes:
            class_dir = self.root_dir / class_name
            for img_path in class_dir.glob("*.jpg"):
                self.images.append(img_path)
                self.labels.append(self.class_to_idx[class_name])
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Carregar imagem
        try:
            image = Image.open(img_path).convert("RGB")
        except Exception as e:
            print(f"Erro ao carregar {img_path}: {e}")
            # Retornar imagem preta se falhar
            image = Image.new("RGB", (self.img_size, self.img_size))
        
        # Aplicar transformações
        if self.transform:
            image = self.transform(image)
        
        return image, label


def get_dataloaders(data_root="data", batch_size=32, num_workers=4, img_size=224):
    """
    Criar DataLoaders para treino, validação e teste
    
    Args:
        data_root: Caminho raiz dos dados
        batch_size: Tamanho do batch
        num_workers: Número de workers para loading
        img_size: Tamanho das imagens
    
    Returns:
        (train_loader, val_loader, test_loader, num_classes)
    """
    
    # Transformações com augmentação para treino
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Transformações sem augmentação para val/test
    val_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Criar datasets
    train_dataset = PlantDiseaseDataset(
        f"{data_root}/train",
        split="train",
        img_size=img_size,
        transform=train_transform
    )
    
    val_dataset = PlantDiseaseDataset(
        f"{data_root}/val",
        split="val",
        img_size=img_size,
        transform=val_transform
    )
    
    test_dataset = PlantDiseaseDataset(
        f"{data_root}/test",
        split="test",
        img_size=img_size,
        transform=val_transform
    )
    
    # Criar dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    num_classes = len(train_dataset.classes)
    
    return train_loader, val_loader, test_loader, num_classes


# Para uso em Colab (sem num_workers)
def get_dataloaders_colab(data_root="data", batch_size=32, img_size=224):
    """Versão otimizada para Google Colab (sem multiprocessing)"""
    return get_dataloaders(
        data_root=data_root,
        batch_size=batch_size,
        num_workers=0,  # Colab não suporta bem multiprocessing
        img_size=img_size
    )
