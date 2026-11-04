# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import torch, json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.models import MLPBaseline, CNNTransferLearning
from src.data_loader import PlantDiseaseDataset
from src.training import Trainer
from src.utils import set_seed, get_device
from src.noise_injection import flip_labels

Path("results/noise_experiments").mkdir(parents=True, exist_ok=True)
device = get_device()
img_size = 224
num_classes = 6

try:
    model = CNNTransferLearning(num_classes=num_classes, pretrained=False, freeze_backbone=False)
    model.load_state_dict(torch.load('results/cnn/best_model.pth', map_location=device))
    model_name = "CNN"
    print("Usando CNN")
except:
    model = MLPBaseline(input_size=64*64*3, hidden_size=256, num_classes=num_classes)
    model.load_state_dict(torch.load('results/mlp/best_model.pth', map_location=device))
    model_name = "MLP"
    img_size = 64
    print("Usando MLP")

model = model.to(device)
set_seed(42)
val_transform = transforms.Compose([transforms.Resize((img_size, img_size)), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
test_dataset = PlantDiseaseDataset('data/test', img_size=img_size, transform=val_transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)

print("\nBASELINE (sem ruido)")
trainer = Trainer(model=model, device=device, lr=0.001)
y_pred_clean, _, y_true = trainer.predict(test_loader)
acc_clean = (y_pred_clean == y_true).mean()
print(f"Acuracia: {acc_clean:.4f}")

print("\nEXPERIMENTO: RUIDO NOS LABELS")
noise_levels = [0.0, 0.05, 0.10, 0.20, 0.30]
results = []

for noise_ratio in noise_levels:
    noisy_labels, _ = flip_labels(test_dataset.labels, flip_ratio=noise_ratio, num_classes=num_classes)
    original = test_dataset.labels.copy()
    test_dataset.labels = list(noisy_labels)
    noisy_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    y_pred, _, _ = trainer.predict(noisy_loader)
    test_dataset.labels = list(original)
    true_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    _, _, y_true_final = trainer.predict(true_loader)
    acc = (y_pred == y_true_final).mean()
    results.append({"noise_ratio": noise_ratio, "accuracy": float(acc)})
    print(f"{noise_ratio*100:.0f}% ruido: {acc:.4f}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([r["noise_ratio"]*100 for r in results], [r["accuracy"]*100 for r in results], 'o-', linewidth=2, markersize=8)
ax.axhline(y=acc_clean*100, color='r', linestyle='--', label='Baseline')
ax.set_xlabel('% Labels Trocados', fontsize=12)
ax.set_ylabel('Acuracia (%)', fontsize=12)
ax.set_title(f'Robustez a Ruido ({model_name})', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('results/noise_experiments/label_noise.png', dpi=150)

with open('results/noise_experiments/metrics.json', 'w') as f:
    json.dump({"model": model_name, "baseline": float(acc_clean), "experiments": results}, f, indent=2)

print("\nFASE 3 CONCLUIDA!")
