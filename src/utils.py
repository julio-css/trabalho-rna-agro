"""
utils.py - Funções utilitárias para visualização e métricas
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, f1_score
import seaborn as sns
from pathlib import Path


def plot_training_history(history, save_path=None):
    """
    Plotar curvas de treino vs validação
    
    Args:
        history: Dict com "train_loss", "val_loss", "train_acc", "val_acc"
        save_path: Caminho para salvar figura
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    
    # Loss
    axes[0].plot(history["train_loss"], label="Train Loss", linewidth=2)
    axes[0].plot(history["val_loss"], label="Val Loss", linewidth=2)
    axes[0].set_xlabel("Época", fontsize=11)
    axes[0].set_ylabel("Loss", fontsize=11)
    axes[0].set_title("Perda (CrossEntropy)", fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Acurácia
    axes[1].plot(history["train_acc"], label="Train Acc", linewidth=2)
    axes[1].plot(history["val_acc"], label="Val Acc", linewidth=2)
    axes[1].set_xlabel("Época", fontsize=11)
    axes[1].set_ylabel("Acurácia", fontsize=11)
    axes[1].set_title("Acurácia", fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_confusion_matrix(y_true, y_pred, class_names=None, save_path=None):
    """
    Plotar matriz de confusão
    
    Args:
        y_true: Labels verdadeiros
        y_pred: Labels preditos
        class_names: Nomes das classes
        save_path: Caminho para salvar figura
    """
    cm = confusion_matrix(y_true, y_pred)
    
    # Normalizar
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(cm_norm, annot=True, fmt='.2f', cmap='Blues', ax=ax,
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Taxa'})
    
    ax.set_ylabel('Verdadeiro', fontsize=11)
    ax.set_xlabel('Predição', fontsize=11)
    ax.set_title('Matriz de Confusão (Normalizada)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def print_classification_report(y_true, y_pred, class_names=None):
    """
    Imprimir relatório de classificação
    
    Args:
        y_true: Labels verdadeiros
        y_pred: Labels preditos
        class_names: Nomes das classes
    """
    print("\n" + "="*70)
    print("RELATÓRIO DE CLASSIFICAÇÃO")
    print("="*70 + "\n")
    
    report = classification_report(y_true, y_pred, target_names=class_names)
    print(report)
    
    # Métricas gerais
    overall_acc = (y_true == y_pred).mean()
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    weighted_f1 = f1_score(y_true, y_pred, average='weighted')
    
    print("\nMÉTRICAS GERAIS:")
    print(f"  Acurácia geral: {overall_acc:.4f}")
    print(f"  F1-Score (macro): {macro_f1:.4f}")
    print(f"  F1-Score (weighted): {weighted_f1:.4f}")
    print("="*70 + "\n")


def plot_sample_predictions(images, y_true, y_pred, y_conf, class_names=None, 
                           num_samples=12, save_path=None):
    """
    Plotar amostras de predições
    
    Args:
        images: Array de imagens (batch_size, 3, H, W)
        y_true: Labels verdadeiros
        y_pred: Labels preditos
        y_conf: Confiança das predições
        class_names: Nomes das classes
        num_samples: Número de amostras a plotar
        save_path: Caminho para salvar figura
    """
    num_samples = min(num_samples, len(images))
    cols = 4
    rows = (num_samples + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 3*rows))
    axes = axes.flatten()
    
    for i in range(num_samples):
        ax = axes[i]
        
        # Desnormalizar imagem
        img = images[i].numpy()
        img = np.transpose(img, (1, 2, 0))
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)
        
        ax.imshow(img)
        
        # Determinar cor
        is_correct = y_true[i] == y_pred[i]
        color = 'green' if is_correct else 'red'
        
        true_label = class_names[y_true[i]] if class_names else str(y_true[i])
        pred_label = class_names[y_pred[i]] if class_names else str(y_pred[i])
        
        title = f"Verdadeiro: {true_label}\n"
        title += f"Predição: {pred_label} ({y_conf[i]:.2f})"
        
        ax.set_title(title, fontsize=9, color=color, fontweight='bold')
        ax.axis('off')
    
    # Remover eixos vazios
    for i in range(num_samples, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def set_seed(seed=42):
    """
    Fixar seed para reprodutibilidade
    
    Args:
        seed: Valor do seed
    """
    import torch
    import random
    
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device():
    """Retornar device (cuda ou cpu)"""
    import torch
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
