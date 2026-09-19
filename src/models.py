"""
models.py - Definição de MLP e CNN para diagnóstico de doenças em plantas
"""

import torch
import torch.nn as nn
import torchvision.models as models


class MLPBaseline(nn.Module):
    """
    MLP Baseline para classificação de doenças em plantas
    
    Entrada: Imagens 64x64 achatadas (4096 features)
    Saída: Probabilidades para cada classe
    """
    
    def __init__(self, input_size=64*64, hidden_size=256, num_classes=10):
        super(MLPBaseline, self).__init__()
        
        self.flatten = nn.Flatten()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(hidden_size // 2, num_classes)
        )
    
    def forward(self, x):
        x = self.flatten(x)
        return self.network(x)


class CNNTransferLearning(nn.Module):
    """
    CNN com Transfer Learning usando MobileNetV2
    
    Entrada: Imagens 224x224 (RGB)
    Saída: Probabilidades para cada classe
    """
    
    def __init__(self, num_classes=10, pretrained=True, freeze_backbone=True):
        super(CNNTransferLearning, self).__init__()
        
        # Carregar MobileNetV2 pré-treinado
        self.backbone = models.mobilenet_v2(pretrained=pretrained)
        
        # Congelar pesos da backbone se solicitado
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # Substituir camada de classificação final
        num_features = self.backbone.classifier[1].in_features
        
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)
    
    def unfreeze_backbone(self):
        """Descongelar pesos da backbone para fine-tuning"""
        for param in self.backbone.features.parameters():
            param.requires_grad = True


class CNNResNet18(nn.Module):
    """
    CNN com Transfer Learning usando ResNet18 (alternativa)
    
    Entrada: Imagens 224x224 (RGB)
    Saída: Probabilidades para cada classe
    """
    
    def __init__(self, num_classes=10, pretrained=True, freeze_backbone=True):
        super(CNNResNet18, self).__init__()
        
        # Carregar ResNet18 pré-treinado
        self.backbone = models.resnet18(pretrained=pretrained)
        
        # Congelar pesos da backbone se solicitado
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # Substituir camada de classificação final
        num_features = self.backbone.fc.in_features
        
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)
    
    def unfreeze_backbone(self):
        """Descongelar pesos da backbone para fine-tuning"""
        for param in self.backbone.parameters():
            param.requires_grad = True


def get_model(model_name, num_classes=10, device="cpu"):
    """
    Factory function para obter modelos
    
    Args:
        model_name: "mlp" | "mobilenetv2" | "resnet18"
        num_classes: Número de classes
        device: "cpu" ou "cuda"
    
    Returns:
        Modelo instantiado e movido para o device
    """
    
    if model_name == "mlp":
        model = MLPBaseline(input_size=64*64, num_classes=num_classes)
    elif model_name == "mobilenetv2":
        model = CNNTransferLearning(num_classes=num_classes, pretrained=True, freeze_backbone=True)
    elif model_name == "resnet18":
        model = CNNResNet18(num_classes=num_classes, pretrained=True, freeze_backbone=True)
    else:
        raise ValueError(f"Modelo desconhecido: {model_name}")
    
    return model.to(device)
