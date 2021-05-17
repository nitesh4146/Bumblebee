# <center>Bumblebee <img src="images/bee.png" alt="alt text" width="48" height="48"></center>

## Team Members & Contributors
1. [Nitish Gupta](https://github.com/nitesh4146)
2. [Kameron Ted Bielawski](https://github.com/kambielawski)
3. [Xiangyu Chen](https://github.com/xiangyu8)
4. [Yiju Yang](https://github.com/YijuYang)
5. [Saharsh Gupta](https://github.com/saharshgupta)

## Prerequisites
* SVL Simulator - [Instructions here](https://www.svlsimulator.com/docs/installation-guide/installing-simulator/)
* Data Link - [Download from Drive](https://drive.google.com/file/d/1rL90epx_HgIjThv9ABoYMDS5SetPue1_/view?usp=sharing)  into maps folder
* Data Directory Structures - `./bumblebee/maps/Map1/data1/`


## Table of Contents
1. [Abstract](#abstract)
2. [Implementation](#implementation)
3. [Evaluation](#cvaluation)
4. [Conclusion](#conclusion)
5. [References](#references)


### Abstract
End-to-end learning for self-driving cars shows great potential since it removes some modules like path planning and optimization compared with traditional sefl-driving cars. However, data collection and model testing have been a bottleneck for algorithm verification. Thankfully, a relatively realistic simulator, SVL, was released in 2019, allowing us explore end-to-end algorithms conveniently. To this end, we collect data, design and also test exsting models, then simulate on the SVL simulator to compare the performance of some steering estimation algorithms. 

### Implementation
#### 1) End-to-end architecture
<p align="center">
<img src = "images/archeture.png"  alt="alt text" width=700" height="400">
</p>
                                                                         
#### 2) Data Acquisition
* Maps: 4 different maps: San Francisco, BorgesAve, Circular Path and Lan-less road
* Data: a. Camera feeds (left/right/center), b. corresponding steering angle values.
* Drive Speed: constant speed
* Time: 10+ hours of driving
* Data: to download our collected data, please refer to Prerequisites part above.

#### 3) Data Preprocessing
* Data Augmentation
  * Data addition: flipping images and negating corresponding steering angles.
  * Histogram balanceing: randomly resampling to the mean to remove bias as below.
<p align="center">
<img src = "images/balancing.png"  alt="alt text" width=1000" height="400">
</p>
  * Cropping: removal irrelevant information (sky, hood, etc.)
<p align="center">
<img src = "images/cropping.png"  alt="alt text" width=1000" height="400">
</p>
  * Scaling: reducing resulution 
* Batching: to make the algorithms run within limited memory.
<p align="center">
<img src = "images/batchingv2.png"  alt="alt text" width="500" height="350">
 </p>

#### 4) Training 
* setting:
  * backbone: convnet from NVIDIA, 5 conv layers+ 4 dense layers.
  * GPU: GTX 1080 8GB
  * Optimizer: Adam
  * Learning rate: 10^-4
  * Epochs: 10
  * Batch size: 32 or 128
  * Callbacks: Early stopping
  * Number of parameters: 250k
  * Framework: Tensorflow==1.15, keras==2.3.1
  * CUDA: 10.1

* result of convenet backbone:
  * inference time: 10 ms
  * FPS: 100 FPS
  * Successfully completed laps on all maps.

#### 5) Network Exploration
To make networks adjusted to more complicated road conditions, we explored more backbones to compare (results can be found in next part.):
* Baseline: convnet from NVIDIA (from previous part)
* convnet v2: another version of convnet with more FC layers and less conv layer, thus more parameters.
* Simple Resnet: our own simplified resnet to make online inference possible.
* RNN: inspired by [Training a neural network with an image sequence — example with a video as input](https://medium.com/smileinnovation/training-neural-network-with-image-sequence-an-example-with-video-as-input-c3407f7a0b0f), implement a sliding window based LSTM network to consider long-time dependencies. In our implementation, we set the length of sequence to 5.
* Shufflenet v1: a classicial efficient feature extractor for mobile devices with channel shuffle module.
* Shufflenet v2: an improved version of Shufflenet v1.
* Resnet 10: widely used smaller Resnet.
* Resnet 18: the smallest resnet proposed by Kaiming He. 

### Evaluation
* **Results**:
<img src = "images/result.png">

* **Demonstrations** (simulation on SVL simulator)
  * drive in different weather condition with convnet backbone. [video](https://www.youtube.com/watch?v=cOHSH2WEXE8)
  * Comparison of different backbones driving on Circular Path map. [video](https://www.youtube.com/watch?v=QknvHtCnNVk)
  * Comparison of different backbones driving on San Francisco map. [video](https://www.youtube.com/watch?v=MhFzb6Eb2CQ)
 
### Conclusion 
* RNN based backbone can finish all maps we tried, showing it's promising to consider long dependencies of sequence based tasks like steering estimation in autonomous driving.
* There is a trade-off between the number of parameters and security in autonomous driving. However, once the inference time can meet the minimum requirement of online inference, we only need to consider security then.
* Good feature extractors in typical tasks like image classification, cannot always work in steering estimation. Specially designed models are needed for such a time-sensitive and accuracy-sensitive task, like our sliding window based RNN model.

### References 
1. Bojarski, M.,Testa, D., Dworakowski, D., Firner, B., Flepp, B., Goyal, P., Jackel,
L., Monfort, M., Muller, U., Zhang, J., Zhang, X., Zhao, J., & Zieba, K. (2016). End to End Learning for Self-Driving Cars. ArXiv, abs/1604.07316.
2. [SVL simulator](www.svlsimulator.com)
3. [ROS](www.ros.org)
4. J. Zhou, X. Hong, F. Su and G. Zhao, "Recurrent Convolutional Neural Network Regression for Continuous Pain Intensity Estimation in Video," 2016 IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2016, pp. 1535-1543, doi: 10.1109/CVPRW.2016.191.
5. Eraqi, H.M., Moustafa, M.N., & Honer, J. (2017). End-to-End Deep Learning for Steering Autonomous Vehicles Considering Temporal Dependencies. ArXiv, abs/1710.03804.
