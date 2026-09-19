"""
create_synthetic_dataset.py - Criar dataset sintético usando apenas módulos built-in

Gera imagens PPM (formato simples que não precisa de PIL)
depois converte para JPG usando ImageMagick se disponível
"""

import os
import struct
import random
from pathlib import Path

CLASSES = {
    "soja_saudavel": {"r": 34, "g": 139, "b": 34},
    "soja_ferrugem": {"r": 139, "g": 69, "b": 19},
    "milho_saudavel": {"r": 50, "g": 150, "b": 50},
    "milho_cercospora": {"r": 101, "g": 67, "b": 33},
    "cafe_saudavel": {"r": 60, "g": 120, "b": 60},
    "cafe_ferrugem": {"r": 180, "g": 100, "b": 50},
}

SPLITS = {"train": 50, "val": 15, "test": 15}
IMG_SIZE = 224


def create_ppm_image(class_name, class_config, disease_type=None):
    """Criar imagem PPM (formato simples)"""
    w, h = IMG_SIZE, IMG_SIZE
    
    # Inicializar com fundo verde
    bg_r = random.randint(80, 120)
    bg_g = random.randint(140, 180)
    bg_b = random.randint(80, 120)
    
    pixels = [[[bg_r, bg_g, bg_b] for _ in range(w)] for _ in range(h)]
    
    # Desenhar folha simples (retângulo com cor)
    leaf_color = [class_config["r"], class_config["g"], class_config["b"]]
    
    x_start, x_end = 60, 164
    y_start, y_end = 50, 174
    
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            if 0 <= y < h and 0 <= x < w:
                pixels[y][x] = leaf_color[:]
    
    # Adicionar doença (spots)
    if disease_type == "rust":
        for _ in range(int(20 * random.uniform(0.2, 0.5))):
            spot_x = random.randint(x_start + 10, x_end - 10)
            spot_y = random.randint(y_start + 10, y_end - 10)
            
            for dy in range(-10, 10):
                for dx in range(-10, 10):
                    yy, xx = spot_y + dy, spot_x + dx
                    if 0 <= yy < h and 0 <= xx < w and (dx**2 + dy**2) < 100:
                        pixels[yy][xx] = [200, 100, 50]
    
    elif disease_type == "spots":
        for _ in range(int(15 * random.uniform(0.2, 0.5))):
            spot_x = random.randint(x_start + 10, x_end - 10)
            spot_y = random.randint(y_start + 10, y_end - 10)
            
            for dy in range(-12, 12):
                for dx in range(-12, 12):
                    yy, xx = spot_y + dy, spot_x + dx
                    if 0 <= yy < h and 0 <= xx < w and (dx**2 + dy**2) < 144:
                        r = max(0, pixels[yy][xx][0] - 60)
                        g = max(0, pixels[yy][xx][1] - 40)
                        b = max(0, pixels[yy][xx][2] - 20)
                        pixels[yy][xx] = [r, g, b]
    
    # Converter para bytes PPM
    ppm_header = f"P6\n{w} {h}\n255\n".encode()
    ppm_data = b""
    
    for row in pixels:
        for pixel in row:
            ppm_data += bytes(pixel)
    
    return ppm_header + ppm_data


def create_dataset():
    """Criar dataset"""
    data_dir = Path("data")
    
    print("Criando dataset sintético (PPM)...")
    total = 0
    
    for split, num_per_class in SPLITS.items():
        print(f"\n{split.upper()}:")
        
        for class_name, class_config in CLASSES.items():
            class_dir = data_dir / split / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"  {class_name}: ", end="", flush=True)
            
            # Determinar tipo de doença
            if "ferrugem" in class_name:
                disease_type = "rust"
            elif "cercospora" in class_name:
                disease_type = "spots"
            else:
                disease_type = None
            
            for idx in range(num_per_class):
                ppm_data = create_ppm_image(class_name, class_config, disease_type)
                
                # Salvar como PPM
                ppm_path = class_dir / f"{idx:04d}.ppm"
                with open(ppm_path, "wb") as f:
                    f.write(ppm_data)
                
                # Tentar converter para JPG com ImageMagick
                try:
                    os.system(f"convert '{ppm_path}' '{class_dir / f'{idx:04d}.jpg'}' 2>/dev/null")
                    os.remove(ppm_path)
                except:
                    pass
                
                total += 1
            
            print(f"✓ {num_per_class}")
    
    print(f"\n✓ Dataset criado com sucesso!")
    print(f"Total: {total} imagens")


if __name__ == "__main__":
    create_dataset()
