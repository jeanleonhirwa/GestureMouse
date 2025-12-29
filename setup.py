"""
Setup script for GestureMouse
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gesturemouse",
    version="1.0.0",
    author="GestureMouse Team",
    description="Webcam-based gesture control for mouse operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gesturemouse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video :: Capture",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mediapipe>=0.10.9",
        "opencv-python>=4.8.0",
        "PyQt6>=6.6.0",
        "pyautogui>=0.9.54",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gesturemouse=src.main:main",
        ],
    },
)
