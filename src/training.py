"""
training.py - Loop de treinamento e validação
"""

import torch
import torch.nn as nn
from torch.optim import Adam, SGD
import numpy as np
from tqdm import tqdm
import json
from pathlib import Path


class Trainer:
    """
    Classe para treinar e validar modelos de classificação
    """
    
    def __init__(self, model, device="cpu", lr=0.001, optimizer_name="adam"):
        """
        Args:
            model: Modelo PyTorch
            device: "cpu" ou "cuda"
            lr: Learning rate
            optimizer_name: "adam" ou "sgd"
        """
        self.model = model.to(device)
        self.device = device
        self.lr = lr
        
        # Otimizador
        if optimizer_name.lower() == "adam":
            self.optimizer = Adam(self.model.parameters(), lr=lr)
        elif optimizer_name.lower() == "sgd":
            self.optimizer = SGD(self.model.parameters(), lr=lr, momentum=0.9)
        else:
            raise ValueError(f"Otimizador desconhecido: {optimizer_name}")
        
        # Função de perda
        self.criterion = nn.CrossEntropyLoss()
        
        # Histórico
        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": []
        }
    
    def train_epoch(self, train_loader):
        """Treinar uma época"""
        self.model.train()
        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        
        pbar = tqdm(train_loader, desc="Treinando", leave=False)
        
        for images, labels in pbar:
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            # Forward
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Estatísticas
            total_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total_correct += (predicted == labels).sum().item()
            total_samples += labels.size(0)
            
            pbar.set_postfix({"loss": loss.item():.4f})
        
        avg_loss = total_loss / total_samples
        avg_acc = total_correct / total_samples
        
        return avg_loss, avg_acc
    
    def validate(self, val_loader):
        """Validar modelo"""
        self.model.eval()
        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        
        with torch.no_grad():
            pbar = tqdm(val_loader, desc="Validando", leave=False)
            
            for images, labels in pbar:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                # Forward
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                # Estatísticas
                total_loss += loss.item() * images.size(0)
                _, predicted = torch.max(outputs, 1)
                total_correct += (predicted == labels).sum().item()
                total_samples += labels.size(0)
                
                pbar.set_postfix({"loss": loss.item():.4f})
        
        avg_loss = total_loss / total_samples
        avg_acc = total_correct / total_samples
        
        return avg_loss, avg_acc
    
    def fit(self, train_loader, val_loader, epochs=50, save_best=True, 
            save_dir="results"):
        """
        Treinar modelo por múltiplas épocas
        
        Args:
            train_loader: DataLoader de treino
            val_loader: DataLoader de validação
            epochs: Número de épocas
            save_best: Salvar modelo com melhor validação
            save_dir: Diretório para salvar checkpoints
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        best_val_acc = 0.0
        best_epoch = 0
        
        print(f"\n{'='*70}")
        print(f"Treinando por {epochs} épocas")
        print(f"Device: {self.device}")
        print(f"Learning rate: {self.lr}")
        print(f"{'='*70}\n")
        
        for epoch in range(1, epochs + 1):
            # Treinar
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # Validar
            val_loss, val_acc = self.validate(val_loader)
            
            # Registrar histórico
            self.history["train_loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_acc"].append(val_acc)
            
            # Print
            print(f"Epoch {epoch:3d}/{epochs} | "
                  f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
                  f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")
            
            # Salvar melhor modelo
            if save_best and val_acc > best_val_acc:
                best_val_acc = val_acc
                best_epoch = epoch
                checkpoint_path = save_dir / "best_model.pth"
                torch.save(self.model.state_dict(), checkpoint_path)
                print(f"  → Melhor modelo salvo (Acurácia: {val_acc:.4f})")
        
        print(f"\n{'='*70}")
        print(f"Treinamento concluído!")
        print(f"Melhor época: {best_epoch} (Acurácia: {best_val_acc:.4f})")
        print(f"{'='*70}\n")
        
        # Salvar histórico
        history_path = save_dir / "training_history.json"
        with open(history_path, "w") as f:
            json.dump(self.history, f, indent=2)
        
        return self.history
    
    def predict(self, test_loader):
        """
        Fazer predições no conjunto de teste
        
        Returns:
            predictions: Array com labels preditos
            confidences: Array com confiança das predições
            all_labels: Array com labels verdadeiros
        """
        self.model.eval()
        predictions = []
        confidences = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in tqdm(test_loader, desc="Predizendo"):
                images = images.to(self.device)
                
                outputs = self.model(images)
                probs = torch.softmax(outputs, dim=1)
                
                _, predicted = torch.max(outputs, 1)
                
                predictions.extend(predicted.cpu().numpy())
                confidences.extend(probs.max(dim=1)[0].cpu().numpy())
                all_labels.extend(labels.numpy())
        
        return np.array(predictions), np.array(confidences), np.array(all_labels)
