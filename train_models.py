# -*- coding: utf-8 -*-
"""Script para treinar MLP e CNN"""
import sys
sys.path.insert(0, '.')
import torch, json, numpy as np
import matplotlib
matplotlib.use('Agg')
from pathlib import Path
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.models import MLPBaseline, CNNTransferLearning
from src.data_loader import PlantDiseaseDataset
from src.training import Trainer
from src.utils import set_seed, get_device, plot_training_history, plot_confusion_matrix, print_classification_report

def train_mlp(epochs=20):
    set_seed(42)
    device = get_device()
    img_size = 64
    train_transform = transforms.Compose([transforms.Resize((img_size, img_size)), transforms.RandomHorizontalFlip(p=0.5), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    val_transform = transforms.Compose([transforms.Resize((img_size, img_size)), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    train_dataset = PlantDiseaseDataset('data/train', img_size=img_size, transform=train_transform)
    val_dataset = PlantDiseaseDataset('data/val', img_size=img_size, transform=val_transform)
    test_dataset = PlantDiseaseDataset('data/test', img_size=img_size, transform=val_transform)
    num_classes = len(train_dataset.classes)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    model = MLPBaseline(input_size=img_size*img_size*3, hidden_size=256, num_classes=num_classes)
    trainer = Trainer(model=model, device=device, lr=0.001, optimizer_name='adam')
    history = trainer.fit(train_loader, val_loader, epochs=epochs, save_best=True, save_dir='results/mlp')
    best_model = MLPBaseline(input_size=img_size*img_size, hidden_size=256, num_classes=num_classes)
    best_model.load_state_dict(torch.load('results/mlp/best_model.pth', map_location=device))
    best_model = best_model.to(device)
    trainer.model = best_model
    y_pred, y_conf, y_true = trainer.predict(test_loader)
    test_acc = (y_pred == y_true).mean()
    results = {"model": "MLP", "epochs": epochs, "best_val_acc": float(max(history['val_acc'])), "test_acc": float(test_acc), "params": sum(p.numel() for p in model.parameters())}
    with open('results/mlp/metrics.json', 'w') as f: json.dump(results, f, indent=2)
    print_classification_report(y_true, y_pred, class_names=train_dataset.classes)
    plot_training_history(history, save_path='results/plots/02_mlp_training_history.png')
    plot_confusion_matrix(y_true, y_pred, class_names=train_dataset.classes, save_path='results/confusion_matrices/02_mlp_confusion_matrix.png')
    return results

def train_cnn(epochs_phase1=15, epochs_phase2=10):
    set_seed(42)
    device = get_device()
    img_size = 224
    train_transform = transforms.Compose([transforms.Resize((img_size, img_size)), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomRotation(15), transforms.ColorJitter(brightness=0.2, contrast=0.2), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    val_transform = transforms.Compose([transforms.Resize((img_size, img_size)), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    train_dataset = PlantDiseaseDataset('data/train', img_size=img_size, transform=train_transform)
    val_dataset = PlantDiseaseDataset('data/val', img_size=img_size, transform=val_transform)
    test_dataset = PlantDiseaseDataset('data/test', img_size=img_size, transform=val_transform)
    num_classes = len(train_dataset.classes)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    model = CNNTransferLearning(num_classes=num_classes, pretrained=True, freeze_backbone=True)
    trainer = Trainer(model=model, device=device, lr=0.001, optimizer_name='adam')
    history1 = trainer.fit(train_loader, val_loader, epochs=epochs_phase1, save_best=True, save_dir='results/cnn')
    model.load_state_dict(torch.load('results/cnn/best_model.pth', map_location=device))
    model.unfreeze_backbone()
    trainer = Trainer(model=model, device=device, lr=0.0001, optimizer_name='adam')
    history2 = trainer.fit(train_loader, val_loader, epochs=epochs_phase2, save_best=True, save_dir='results/cnn')
    history = {'train_loss': history1['train_loss'] + history2['train_loss'], 'val_loss': history1['val_loss'] + history2['val_loss'], 'train_acc': history1['train_acc'] + history2['train_acc'], 'val_acc': history1['val_acc'] + history2['val_acc']}
    best_model = CNNTransferLearning(num_classes=num_classes, pretrained=True, freeze_backbone=False)
    best_model.load_state_dict(torch.load('results/cnn/best_model.pth', map_location=device))
    best_model = best_model.to(device)
    trainer.model = best_model
    y_pred, y_conf, y_true = trainer.predict(test_loader)
    test_acc = (y_pred == y_true).mean()
    results = {"model": "CNN_MobileNetV2", "epochs": epochs_phase1 + epochs_phase2, "best_val_acc": float(max(history['val_acc'])), "test_acc": float(test_acc), "params": sum(p.numel() for p in model.parameters())}
    with open('results/cnn/metrics.json', 'w') as f: json.dump(results, f, indent=2)
    print_classification_report(y_true, y_pred, class_names=train_dataset.classes)
    plot_training_history(history, save_path='results/plots/03_cnn_training_history.png')
    plot_confusion_matrix(y_true, y_pred, class_names=train_dataset.classes, save_path='results/confusion_matrices/03_cnn_confusion_matrix.png')
    return results

if __name__ == "__main__":
    Path("results/mlp").mkdir(parents=True, exist_ok=True)
    Path("results/cnn").mkdir(parents=True, exist_ok=True)
    mlp_results = train_mlp(epochs=20)
    cnn_results = train_cnn(epochs_phase1=15, epochs_phase2=10)
    print(f"\nMLP: test_acc={mlp_results['test_acc']:.4f}, CNN: test_acc={cnn_results['test_acc']:.4f}")
    with open('results/metrics.json', 'w') as f: json.dump({"mlp": mlp_results, "cnn": cnn_results}, f, indent=2)
