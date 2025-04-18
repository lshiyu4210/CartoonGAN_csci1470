## Title
**Using GANs to transform real world photos into cartoon style images**

## Who
Shiyu Liu, Sibo Zhou, Junhui Huang

## Introduction
**What problem are you trying to solve and why?**
- In this paper, we propose a generative adversarial network (GAN) tailored for cartoon transformation, capable of producing high-quality cartoon images from real-world photographs.
- Motivated by the recent surge in popularity of ChatGPT’s cartoon outputs, we aim to create our own model and compare its performance against ChatGPT’s results.

## Related Work
**Are you aware of any, or is there any prior work that you drew on to do your project?**
- One of the closely related works is AnimeGAN (Chen et al., 2020), which applies GAN to transform real-world photos into anime-style images. Like CartoonGAN, AnimeGAN trains on unpaired datasets of photos and anime frames but introduces three specialized loss functions—grayscale style loss, grayscale adversarial loss, and color reconstruction loss—to preserve key anime aesthetics while retaining color fidelity. Its network is intentionally lightweight, requiring fewer parameters and enabling faster processing than many other methods, and it can produce high-quality anime-style images that outperform other techniques in both speed and visuals.  
  URL: [Springer Link](https://link-springer-com.revproxy.brown.edu/content/pdf/10.1007/978-981-15-5547-0_18)

- GitHub Repositories:
  - [CartoonGAN TensorFlow](https://github.com/mnicnc404/CartoonGan-tensorflow)
  - [CartoonGAN by Tobias Sunderkiek](https://github.com/TobiasSunderkiek/cartoon-gan)

## Data
**What data are you using (if any)?**
- In our paper, we are using two types of data. One is standard real-world photo data, which we will gather from COCO dataset or Flickr. The other part of the data is the cartoon dataset—we will be using a cartoon image dataset from Kaggle (Safebooru).

## Methodology

### What is the architecture of your model?
- The CartoonGAN architecture consists of a generator and a discriminator designed specifically for photo-to-cartoon translation. The generator transforms real-world photos into cartoon-style images using a deep convolutional neural network with three stages: initial convolution, downsampling through two strided convolutional blocks, and eight residual blocks for feature transformation, followed by upsampling layers that reconstruct the image at its original resolution. To preserve both content and cartoon characteristics, the generator uses normalization and ReLU activations, finishing with a 7×7 convolution to produce the final output. The discriminator, on the other hand, is a shallow patch-based CNN that distinguishes between real cartoon images, generated outputs, and edge-smoothed cartoons. It employs Leaky ReLU activations and focuses on local style features like sharp edges and smooth shading. This design allows CartoonGAN to efficiently learn cartoon stylization from unpaired datasets while preserving content and generating high-quality, stylistically consistent outputs.

### How are you training the model?
- We train the CartoonGAN model using an adversarial learning framework with unpaired photo and cartoon datasets. The **generator** is first **pretrained** using only the **content loss**, which compares high-level feature maps between the input photo and the generated image via a VGG network to preserve semantic content. After this initialization phase, both the generator and discriminator are trained jointly. The **discriminator** learns to distinguish real cartoon images from both edge-smoothed cartoons and generated outputs, using an **edge-promoting adversarial loss** that emphasizes cartoon-like characteristics such as sharp edges. The generator is updated to fool the discriminator while also minimizing content loss, striking a balance between stylistic transformation and content preservation. This training setup allows the model to learn **cartoonization** effectively without requiring paired image data.

### If you are implementing an existing paper, detail what you think will be the hardest part about implementing the model here.
- One of the hardest parts of implementing CartoonGAN is ensuring the effective integration and balance of the two specialized loss functions—particularly the edge-promoting adversarial loss. Unlike standard GANs, CartoonGAN introduces an additional set of edge-smoothed cartoon images that must be generated and used correctly during training to teach the discriminator to recognize sharp edges. Properly preprocessing these images with Canny edge detection, dilation, and Gaussian smoothing—and aligning their batch flow with the rest of the training data—adds complexity. Furthermore, tuning the training dynamics so that the generator produces both stylistically convincing and content-preserving images, without mode collapse or losing edge clarity, requires careful initialization, loss weighting (especially the content loss factor ω), and hyperparameter tuning. These details are critical and sensitive to get right for the model to converge properly and reproduce the high-quality cartoonization results shown in the paper.

## Metrics
**What constitutes “success?”**
- In this paper, the authors were able to transfer real world photos into cartoon images based on the artistic style. They only have qualitative results on the output images.

**Goals:**
- **Base goal**: Replicate the Core CartoonGAN Architecture, and make sure it could produce relatively satisfactory results on simpler datasets. Visually inspect outputs to confirm the model is producing cartoon images.
- **Target goal**: Train on two different artist styles, using more specific and larger cartoon training datasets.
- **Stretch goal**: Incorporate other loss functions to have style control or preserve more content from the photo. Besides, extend images into short videos.

## Ethics

### What broader societal issues are relevant to your chosen problem space?
- While turning photos into cartoon or anime-style images might seem purely creative or fun, there are several deeper societal considerations. For example, using such tools on personal or private images could raise privacy concerns—someone’s photo could easily be transformed and spread online without consent. Also, these tools might reinforce stereotypes or biases by representing certain facial features or cultural traits inaccurately or disrespectfully when stylized. Lastly, these technologies contribute to the broader challenge of distinguishing authentic images from digitally altered ones, potentially damaging public trust in visual media.

### Why is Deep Learning a good approach to this problem?
- Deep learning is particularly suitable for photo-to-cartoon stylization because it excels at capturing complex patterns and abstract visual features from large amounts of data. Cartoonization involves simplifying real images into essential lines, shapes, and colors, while removing unnecessary detail—a process difficult to define manually with fixed rules. GANs naturally learn this abstraction directly from examples, effectively capturing the artistic style and essence of cartoons. Once trained, these models can rapidly and consistently produce high-quality stylized images, making them both flexible and practical for various real-world applications, from casual photo editing apps to professional artistic workflows.

## Division of Labor
**Briefly outline who will be responsible for which part(s) of the project.**
- **Junhui Huang**: Data Preparation, model implementation, written reports
- **Sibou Zhou**: model implementation, written reports
- **Shiyu Liu**: poster, model implementation, written reports
