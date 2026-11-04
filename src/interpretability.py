"""
interpretability.py - Técnicas de interpretabilidade para CNNs
"""
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate_cam(self, image, target_class=None):
        self.model.eval()
        image.requires_grad = True
        output = self.model(image)
        pred_class = output.argmax(dim=1).item()
        if target_class is None:
            target_class = pred_class
        self.model.zero_grad()
        one_hot = torch.zeros_like(output)
        one_hot[0, target_class] = 1
        output.backward(gradient=one_hot, retain_graph=True)
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = cam.squeeze().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam, pred_class

def saliency_map(model, image, target_class=None):
    model.eval()
    image.requires_grad = True
    output = model(image)
    pred_class = output.argmax(dim=1).item()
    if target_class is None:
        target_class = pred_class
    model.zero_grad()
    output[0, target_class].backward()
    saliency = image.grad.abs().max(dim=1)[0].squeeze().cpu().numpy()
    return saliency, pred_class

def occlusion_sensitivity(model, image, target_class=None, patch_size=32, stride=16):
    model.eval()
    with torch.no_grad():
        original_output = model(image)
        pred_class = original_output.argmax(dim=1).item()
        if target_class is None:
            target_class = pred_class
        original_prob = F.softmax(original_output, dim=1)[0, target_class].item()
    _, _, h, w = image.shape
    sensitivity_map = np.zeros((h, w))
    for i in range(0, h - patch_size + 1, stride):
        for j in range(0, w - patch_size + 1, stride):
            occluded = image.clone()
            occluded[:, :, i:i+patch_size, j:j+patch_size] = 0.5
            with torch.no_grad():
                output = model(occluded)
                prob = F.softmax(output, dim=1)[0, target_class].item()
            sensitivity = original_prob - prob
            sensitivity_map[i:i+patch_size, j:j+patch_size] += sensitivity
    sensitivity_map = (sensitivity_map - sensitivity_map.min()) / (sensitivity_map.max() - sensitivity_map.min() + 1e-8)
    return sensitivity_map, pred_class

def visualize_interpretability(image_tensor, cam, saliency, occlusion, original_image, pred_class, true_class, class_names, save_path=None):
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes[0, 0].imshow(original_image)
    axes[0, 0].set_title(f"Original\nVerdadeiro: {class_names[true_class]}\nPredito: {class_names[pred_class]}", fontsize=10, fontweight='bold')
    axes[0, 0].axis('off')
    axes[0, 1].imshow(original_image)
    axes[0, 1].imshow(cam, cmap='jet', alpha=0.5)
    axes[0, 1].set_title("Grad-CAM", fontsize=10, fontweight='bold')
    axes[0, 1].axis('off')
    axes[1, 0].imshow(saliency, cmap='hot')
    axes[1, 0].set_title("Saliency Map", fontsize=10, fontweight='bold')
    axes[1, 0].axis('off')
    axes[1, 1].imshow(occlusion, cmap='Reds')
    axes[1, 1].set_title("Occlusion Sensitivity", fontsize=10, fontweight='bold')
    axes[1, 1].axis('off')
    plt.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig
