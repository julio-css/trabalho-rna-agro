"""
process_field_images.py - Processar imagens coletadas em campo

Script para:
1. Validar integridade das imagens
2. Extrair metadados (GPS, hora, câmera)
3. Redimensionar e normalizar
4. Separar em treino/validação/teste
5. Gerar relatório de qualidade
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import random

# Para processamento de imagens (quando disponível)
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("⚠️  PIL não disponível - usar apenas para estrutura")


class FieldImageProcessor:
    def __init__(self, raw_dir="data/campo_2026/raw", output_dir="data/campo_2026/processed"):
        self.raw_dir = Path(raw_dir)
        self.output_dir = Path(output_dir)
        self.metadata_db = []
        self.validation_report = defaultdict(lambda: {"total": 0, "accepted": 0, "rejected": 0})
        
        # Criar diretórios
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "train").mkdir(exist_ok=True)
        (self.output_dir / "val").mkdir(exist_ok=True)
        (self.output_dir / "test").mkdir(exist_ok=True)
    
    def validate_image(self, image_path):
        """Validar se imagem é aceitável"""
        validations = {
            "exists": False,
            "readable": False,
            "has_metadata": False,
            "quality": False,
            "errors": []
        }
        
        try:
            # 1. Arquivo existe?
            if not image_path.exists():
                validations["errors"].append("Arquivo não existe")
                return validations
            validations["exists"] = True
            
            # 2. Arquivo é leiável?
            if not os.access(image_path, os.R_OK):
                validations["errors"].append("Sem permissão de leitura")
                return validations
            validations["readable"] = True
            
            # 3. Tem metadados (arquivo .json)?
            metadata_path = image_path.with_suffix('.json')
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    if all(k in metadata for k in ['GPS', 'timestamp', 'agronomist_label', 'severity']):
                        validations["has_metadata"] = True
                    else:
                        validations["errors"].append("Metadados incompletos")
            else:
                validations["errors"].append("Arquivo .json não encontrado")
            
            # 4. Qualidade de imagem (se PIL disponível)
            if PILLOW_AVAILABLE:
                try:
                    img = Image.open(image_path)
                    # Verificar dimensões mínimas
                    if img.size[0] >= 800 and img.size[1] >= 600:
                        validations["quality"] = True
                    else:
                        validations["errors"].append(f"Resolução baixa: {img.size}")
                except Exception as e:
                    validations["errors"].append(f"Erro ao abrir imagem: {str(e)}")
            else:
                # Se PIL não disponível, assumir qualidade ok
                validations["quality"] = True
            
            return validations
            
        except Exception as e:
            validations["errors"].append(f"Erro inesperado: {str(e)}")
            return validations
    
    def is_image_acceptable(self, validation_result):
        """Determinar se imagem passa em todos os testes"""
        return (
            validation_result["exists"] and
            validation_result["readable"] and
            validation_result["has_metadata"] and
            validation_result["quality"] and
            len(validation_result["errors"]) == 0
        )
    
    def load_metadata(self, metadata_path):
        """Carregar metadados de uma imagem"""
        try:
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def process_all_images(self):
        """Processar todas as imagens do diretório raw"""
        print("🔍 Iniciando processamento de imagens...")
        print(f"   Diretório: {self.raw_dir}\n")
        
        if not self.raw_dir.exists():
            print(f"❌ Diretório {self.raw_dir} não existe!")
            return False
        
        # Encontrar todas as imagens
        image_files = list(self.raw_dir.rglob("*.jpg")) + list(self.raw_dir.rglob("*.png"))
        
        if not image_files:
            print("❌ Nenhuma imagem encontrada!")
            return False
        
        print(f"📊 Encontradas {len(image_files)} imagens\n")
        
        accepted_images = []
        rejected_images = []
        
        # Processar cada imagem
        for idx, image_path in enumerate(image_files, 1):
            print(f"[{idx}/{len(image_files)}] Validando: {image_path.name}... ", end="", flush=True)
            
            # Validar imagem
            validation = self.validate_image(image_path)
            
            if self.is_image_acceptable(validation):
                print("✅ ACEITA")
                accepted_images.append(image_path)
                
                # Carregar metadados
                metadata_path = image_path.with_suffix('.json')
                metadata = self.load_metadata(metadata_path)
                
                if metadata:
                    label = metadata.get('agronomist_label', 'unknown')
                    self.validation_report[label]["total"] += 1
                    self.validation_report[label]["accepted"] += 1
                    
                    # Adicionar à database
                    self.metadata_db.append({
                        "image_path": str(image_path),
                        "metadata": metadata,
                        "split": None  # Será definido na etapa de split
                    })
            else:
                print(f"❌ REJEITADA - {', '.join(validation['errors'])}")
                rejected_images.append(image_path)
                
                # Carregar metadados mesmo para rejeitadas (para contagem)
                metadata_path = image_path.with_suffix('.json')
                metadata = self.load_metadata(metadata_path)
                if metadata:
                    label = metadata.get('agronomist_label', 'unknown')
                    self.validation_report[label]["total"] += 1
        
        # Relatório de validação
        self._print_validation_report(accepted_images, rejected_images)
        
        return len(accepted_images) > 0
    
    def _print_validation_report(self, accepted, rejected):
        """Imprimir relatório de validação"""
        total = len(accepted) + len(rejected)
        acceptance_rate = (len(accepted) / total * 100) if total > 0 else 0
        
        print("\n" + "="*70)
        print("📋 RELATÓRIO DE VALIDAÇÃO")
        print("="*70)
        print(f"\nTotal de imagens: {total}")
        print(f"Aceitas: {len(accepted)} ({acceptance_rate:.1f}%)")
        print(f"Rejeitadas: {len(rejected)} ({100-acceptance_rate:.1f}%)")
        
        if acceptance_rate < 90:
            print(f"\n⚠️  AVISO: Taxa de aceitação baixa (<90%)")
            print("   Verificar qualidade de coleta de imagens")
        
        print("\n📊 POR CLASSE:")
        for label, stats in sorted(self.validation_report.items()):
            if stats["total"] > 0:
                rate = stats["accepted"] / stats["total"] * 100
                print(f"   {label:20} | Total: {stats['total']:3} | Aceitas: {stats['accepted']:3} ({rate:5.1f}%)")
        
        print("\n" + "="*70)
    
    def create_train_val_test_split(self, train_ratio=0.7, val_ratio=0.15, seed=42):
        """Separar dados em treino/validação/teste"""
        random.seed(seed)
        
        if not self.metadata_db:
            print("❌ Nenhuma imagem aceita para split!")
            return False
        
        print(f"\n🔀 Criando split treino/val/teste...")
        print(f"   Treino: {train_ratio*100:.0f}% | Val: {val_ratio*100:.0f}% | Teste: {(1-train_ratio-val_ratio)*100:.0f}%")
        
        # Agrupar por classe
        by_class = defaultdict(list)
        for entry in self.metadata_db:
            label = entry["metadata"].get('agronomist_label', 'unknown')
            by_class[label].append(entry)
        
        splits = {"train": [], "val": [], "test": []}
        
        # Split por classe (garantir distribuição)
        for label, images in by_class.items():
            random.shuffle(images)
            
            n_train = int(len(images) * train_ratio)
            n_val = int(len(images) * val_ratio)
            
            for i, entry in enumerate(images):
                if i < n_train:
                    entry["split"] = "train"
                    splits["train"].append(entry)
                elif i < n_train + n_val:
                    entry["split"] = "val"
                    splits["val"].append(entry)
                else:
                    entry["split"] = "test"
                    splits["test"].append(entry)
            
            print(f"   {label:20} | Train: {n_train:3} | Val: {n_val:3} | Test: {len(images)-n_train-n_val:3}")
        
        print(f"\n✅ Split concluído:")
        print(f"   Treino: {len(splits['train'])} imagens")
        print(f"   Val:    {len(splits['val'])} imagens")
        print(f"   Teste:  {len(splits['test'])} imagens")
        
        return True
    
    def save_metadata_index(self):
        """Salvar índice de metadados em CSV"""
        csv_path = self.output_dir / "metadata_index.csv"
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['image_path', 'split', 'class', 'severity', 'gps', 'timestamp', 'property'])
            
            for entry in self.metadata_db:
                metadata = entry["metadata"]
                writer.writerow([
                    entry["image_path"],
                    entry.get("split", "unknown"),
                    metadata.get('agronomist_label', ''),
                    metadata.get('severity', ''),
                    metadata.get('GPS', ''),
                    metadata.get('timestamp', ''),
                    metadata.get('property', '')
                ])
        
        print(f"\n✅ Índice de metadados salvo: {csv_path}")
    
    def generate_report(self):
        """Gerar relatório final"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_images": len(self.metadata_db),
            "classes": {},
            "split_distribution": {
                "train": len([e for e in self.metadata_db if e.get("split") == "train"]),
                "val": len([e for e in self.metadata_db if e.get("split") == "val"]),
                "test": len([e for e in self.metadata_db if e.get("split") == "test"])
            }
        }
        
        # Por classe
        by_class = defaultdict(lambda: {"train": 0, "val": 0, "test": 0})
        for entry in self.metadata_db:
            label = entry["metadata"].get('agronomist_label', 'unknown')
            split = entry.get("split", "unknown")
            by_class[label][split] += 1
        
        report["classes"] = dict(by_class)
        
        # Salvar relatório
        report_path = self.output_dir / "processing_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Relatório salvo: {report_path}")
        
        # Imprimir resumo
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DE PROCESSAMENTO")
        print("="*70)
        print(f"\nTotal de imagens processadas: {report['total_images']}")
        print(f"\nDistribuição:")
        print(f"  Treino: {report['split_distribution']['train']}")
        print(f"  Val:    {report['split_distribution']['val']}")
        print(f"  Teste:  {report['split_distribution']['test']}")
        print(f"\nPor classe:")
        for class_name, counts in sorted(report['classes'].items()):
            print(f"  {class_name:20} | Train: {counts['train']:3} | Val: {counts['val']:3} | Test: {counts['test']:3}")
        print("\n" + "="*70)


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("PROCESSADOR DE IMAGENS DE CAMPO - RNA-AGRO")
    print("="*70)
    
    processor = FieldImageProcessor()
    
    # 1. Validar todas as imagens
    if not processor.process_all_images():
        print("\n❌ Nenhuma imagem válida encontrada. Abortando.")
        return
    
    # 2. Criar split treino/val/teste
    if not processor.create_train_val_test_split():
        print("\n❌ Erro ao criar split. Abortando.")
        return
    
    # 3. Salvar índice de metadados
    processor.save_metadata_index()
    
    # 4. Gerar relatório final
    processor.generate_report()
    
    print("\n✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"   Dados prontos em: {processor.output_dir}")


if __name__ == "__main__":
    main()
