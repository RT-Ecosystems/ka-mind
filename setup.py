from setuptools import setup, find_packages
setup(
    name="ka-mind",
    version="3.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "semantic": ["sentence-transformers>=2.2.0"],
        "hd_image": ["diffusers", "torch"],
        "fast_search": ["faiss-cpu>=1.7.4"],
        "all": ["sentence-transformers>=2.2.0", "diffusers", "torch", "faiss-cpu>=1.7.4"],
    },
    author="RT-Ecosystems",
    description="KA-Mind: Zero-Hallucination Neuro-Symbolic AI Framework (No LLMs, No Transformers)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RT-Ecosystems/ka-mind",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
