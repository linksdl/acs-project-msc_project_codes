# Towards Robot Skill Learning by Exploiting Imitation Learning
>  This repository is for my MSc Project.

## Table of Contents
- **[1, Installation](#installation)**
- **[2, Contents of Project](#project)**
  - Datasets
  - Designs of Experiment
  - Implementations of Experiment
  - Evaluation Results
  - Conclusions
- **[3, Acknowledgements](#3)**

## 1, Installation And Usage <a name="installation"></a>
This code is based on [PyTorch](https://pytorch.org/). To install and setup this code in local machine, running the following commands.
- **1: Clone the repository and cd into it** 
  ``` 
  # clone this reposotry to local dir
  git clone https://github.com/linksdl/acs-project-msc_project_codes.git
  
  # cd in this directory
  cd acs-project-msc_project_codes
  
  # create virtual env using conda
  conda create --name env_msc_project_py38 python=3.8
  conda acvtivate env_msc_project_py38
  
  # installing environments
  pip3 install -r requirements.txt
  # or try
  conda env create -f environments.yaml
  ```
  
- **2: Train the models on Datasets**
  ```
  # train the DNN-DMP model
  train_encoder_decoder.py
  
  # train the CNN-DMP model
  train_cnn_encoder_decoder.py
  
  # train the DNN-NDP model
  dnn_ndp_train.py
  
  # train the DNN-NDP model
  train_dnn_ndp.py
  
  # train the SCNN-NDP model
  train_scnn_ndp.py
  
  # train the CNN-NDP model
  train_cnn_ndp.py
  ```

## 2, Contents of Project <a name="project"></a>

### 2.1 Datasets
In this project, we use five types of datasets to train, test and evaluate our models. they are show as following:
- MNIST dataset: http://yann.lecun.com/exdb/mnist/
- Noisy MNIST (n-MNIST) dataset: https://csc.lsu.edu/~saikat/n-mnist/
- Synthetic MNIST (s-MNIST) dataset: https://portal.ijs.si/nextcloud/s/mnp2DD7qCYzyPd5
- Multi-digit MNIST (m-MNIST) dataset: https://github.com/shaohua0116/MultiDigitMNIST
- EMNIST (e-MNIST) dataset: https://www.nist.gov/itl/products-and-services/emnist-dataset
### 2.2 Designs of Experiment

**The network architecture of the DNN-DMP model**
![](architectures/DNN-DMP.png)

**The network architecture of the CNN-DMP model**
![](architectures/CNN-DMP.png)

**The network architecture of the DNN-NDP model**
![](architectures/DNN-NDP.png)

**The network architecture of the SCNN-NDP model**
![](architectures/SCNN-NDP.png)

**The network architecture of the CNN-NDP model**
![](architectures/CNN-NDP.png)

### 2.3 Implementations of Experiment

#### E

#### Experiment on Robot Arm
![](robot/digits/digit-0/digit-0.gif)![](robot/digits/digit-1/digit-1.gif)
<center class="half">
    <img src="robot/digits/digit-0/digit-0.gif" width="200"/>
    <img src="robot/digits/digit-0/digit-0.gif" width="200"/>
    <img src="robot/digits/digit-0/digit-0.gif" width="200"/> 
    <img src="robot/digits/digit-0/digit-0.gif" width="200"/>
</center>


### 2.4 Evaluation Results

### 2.5 Conclusions

## 3, Acknowledgements <a name="3"></a>
In this project, we use some open souce code. The source code of NDPs approach (Neural Dynamic Policies for End-to-End Sensorimotor Learning) is from: https://github.com/shikharbahl/neural-dynamic-policies/. We also use source code of the Deep Encoder-Decoder Networks approach, which comes from: https://github.com/abr-ijs/imednet. Also, some third-party source code comes from: https://github.com/abr-ijs/digit_generator.
