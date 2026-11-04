# -*- coding: utf-8 -*-
"""
Fase 4: Interpretabilidade (P21)
Gera visualizacoes Grad-CAM, saliency e occlusion
"""
import sys
sys.path.insert(0, '.')
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import torchvision.transforms as transforms
from src.models import CNNTransferLearning
from src.data_loader import PlantDiseaseDataset
from src.interpretability import GradCAM, saliency_map, occlusion_sensitivity, visualize_interpretability
from src.utils import get_device, set_seed

Path("results/grad_cam").mkdir(parents=True, exist_ok=True)

set_seed(42)
device = get_device()
img_size = 224

# Carregar CNN
model = CNNTransferLearning(num_classes=6, pretrained=False, freeze_backbone=False)
model.load_state_dict(torch.load('results/cnn/best_model.pth', map_location=device))
model = model.to(device)
model.eval()

# Carregar dados de teste
val_transform = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
test_dataset = PlantDiseaseDataset('data/test', img_size=img_size, transform=val_transform)
class_names = test_dataset.classes

# GradCAM na última camada convolucional
target_layer = model.backbone.features[-1]
grad_cam = GradCAM(model, target_layer)

print("\n=== GERANDO VISUALIZACOES GRAD-CAM ===")

# Selecionar exemplos: 3 acertos e 3 erros (se existirem)
num_samples = min(6, len(test_dataset))
samples_to_viz = []

for idx in range(len(test_dataset)):
    image_tensor, true_label = test_dataset[idx]
    image_tensor_batch = image_tensor.unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image_tensor_batch)
        pred_label = output.argmax(dim=1).item()
    
    is_correct = (pred_label == true_label)
    samples_to_viz.append({
        'idx': idx,
        'true_label': true_label,
        'pred_label': pred_label,
        'is_correct': is_correct
    })
    
    if len(samples_to_viz) >= num_samples:
        break

# Gerar visualizações
for i, sample in enumerate(samples_to_viz):
    idx = sample['idx']
    true_label = sample['true_label']
    pred_label = sample['pred_label']
    
    print(f"\n[{i+1}/{len(samples_to_viz)}] Gerando visualizacao para imagem {idx}")
    print(f"  Verdadeiro: {class_names[true_label]}")
    print(f"  Predito: {class_names[pred_label]}")
    print(f"  {'ACERTO' if sample['is_correct'] else 'ERRO'}")
    
    # Carregar imagem
    image_tensor, _ = test_dataset[idx]
    image_tensor_batch = image_tensor.unsqueeze(0).to(device)
    
    # Grad-CAM
    cam, _ = grad_cam.generate_cam(image_tensor_batch, target_class=pred_label)
    cam_resized = np.array(Image.fromarray((cam * 255).astype(np.uint8)).resize((img_size, img_size)))
    cam_resized = cam_resized / 255.0
    
    # Saliency
    saliency, _ = saliency_map(model, image_tensor_batch, target_class=pred_label)
    saliency_resized = np.array(Image.fromarray((saliency * 255 / saliency.max()).astype(np.uint8)).resize((img_size, img_size)))
    saliency_resized = saliency_resized / 255.0
    
    # Occlusion (reduzido para ser mais rápido)
    occlusion, _ = occlusion_sensitivity(model, image_tensor_batch, target_class=pred_label, patch_size=32, stride=32)
    occlusion_resized = np.array(Image.fromarray((occlusion * 255).astype(np.uint8)).resize((img_size, img_size)))
    occlusion_resized = occlusion_resized / 255.0
    
    # Imagem original (desnormalizar)
    img_path = test_dataset.images[idx]
    original_image = Image.open(img_path).convert('RGB').resize((img_size, img_size))
    original_array = np.array(original_image)
    
    # Visualizar
    status = "acerto" if sample['is_correct'] else "erro"
    save_path = f"results/grad_cam/{i+1:02d}_{status}_{class_names[true_label]}.png"
    
    visualize_interpretability(
        image_tensor_batch,
        cam_resized,
        saliency_resized,
        occlusion_resized,
        original_array,
        pred_label,
        true_label,
        class_names,
        save_path=save_path
    )
    
    print(f"  Salvo: {save_path}")

print("\n=== FASE 4 CONCLUIDA ===")
print(f"Visualizacoes salvas em: results/grad_cam/")
print(f"Total: {len(samples_to_viz)} imagens")
print("\nP21 RESPONDIDA: As visualizacoes mostram onde o modelo olha para decidir!")
