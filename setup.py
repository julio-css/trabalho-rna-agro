from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trabalho-rna-agro",
    version="0.1.0",
    author="Grupo de Redes Neurais Artificiais - UEL",
    description="MLP e CNN para diagnóstico de doenças em culturas (soja, milho, café)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julio-css/trabalho-rna-agro",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.11",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pytorch-lightning>=2.0.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "jupyter>=1.0.0",
        "tqdm>=4.66.0",
        "albumentations>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            # Adicionar scripts executáveis aqui se necessário
        ],
    },
)
