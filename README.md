# CartoonGAN_csci1470

This repository contains our implementation of **CartoonGAN**, based on the CVPR 2018 paper [CartoonGAN: Generative Adversarial Networks for Photo Cartoonization](https://openaccess.thecvf.com/content_cvpr_2018/papers/Chen_CartoonGAN_Generative_Adversarial_CVPR_2018_paper.pdf) by Chen et al. The model transforms real-world photos into stylized cartoon images using an adversarial framework trained on unpaired photo/cartoon image datasets.

## Project Structure

This project was developed for the CSCI1470 Final Project and includes:

- Dataset download scripts
- Edge smoothing preprocessor
- GAN architecture with content and adversarial losses
- Jupyter notebook for training and evaluation
- Final poster and reflections documenting our work

## Getting Started

### 1. Install Requirements

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Download Training Images

Use the provided scripts to download both real-world photos and cartoon images:

```bash
python coco_downloader.py       # Downloads real-world photos from the COCO dataset
python cartoon_downloader.py    # Downloads cartoon-style images
```

This will create two folders with the following structure:

```
coco/                   # real-world photos
├── annotations/
├── photos/
├── coco.zip

safebooru/              # cartoon images
├── photos/
├── all_data.csv
├── safebooru.zip    
```

### 3. Generate Smoothed Cartoon Images

To compute the edge-smoothed versions of the cartoon images for use in the discriminator loss, run:

```bash
python edge_smoother.py
```

This will generate:

```
safebooru/
└── safebooru_smoothed/         # cartoon images with edge smoothing
└── safebooru_smoothed.zip      # zipped version of the smoothed images
```

### 4. Organize Your Files

Ensure that all image folders and files are in the same directory as the Jupyter notebook `CartoonGAN_1470.ipynb`. Your folder structure should look like this:

```
.
├── CartoonGAN_1470.ipynb
├── coco.zip
├── safebooru.zip
├── safebooru_smoothed.zip
├── coco/
│   ├── photos/
│   └── annotations/
├── safebooru/
│   ├── photos/
│   ├── safebooru_smoothed/
```


### 5. Train the Model

To train and test the model, follow this workflow inside CartoonGAN_1470.ipynb:

1. Preprocess the photos using torchvision.datasets.ImageFolder and appropriate transforms (e.g. center crop, resize, etc).
2. Load the Generator and Discriminator models.
3. Initialize loss functions: GeneratorLoss and DiscriminatorLoss.
4. Run the training loop, starting with a content-only warmup phase followed by full adversarial training.
5. Test and visualize outputs: compare generated cartoon images against the original input photos using matplotlib.

## Contributors

- **Shiyu Liu**
- **Sibo Zhou**
- **Junhui Huang**

