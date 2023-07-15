# BlurBadGuyFaces4Video
An app to let you automatically blur bad guy's faces in the video you upload. Mainly using keras, pygame, tkinter and opencv.  

# Foobar

Foobar is a Python library for dealing with word pluralization.

## Requirements

numpy==1.23.4  
opencv_contrib_python==4.6.0.66  
opencv_python==4.6.0.66  
pygame==2.1.2  
tensorflow==2.11.0  
tensorflow_intel==2.11.0  

## Getting Started  
### Introduciton  
Recently, we have seen a lot of reportages on TV about a serious crime, and the criminal often have their face blurred. Try to imagine where you are an editor to that movies, you will have to spend a tons of times to blur a man's face. So to save your time, I create this app that you only need to upload the clip where you have to blur the bad guy's face and it will automatically blur it for you.

## Installing and running  
Download this repository, installing all the requirement packages by pip and then run the main.py file.  

## Technology
### To detect people's face  
I use a dnn caffemodel that opencv introduce cause it have the best performance on video. Models can be found in /models.  
For a deeper reason why I use this model, please visit [here](https://towardsdatascience.com/face-detection-models-which-to-use-and-why-d263e82c302c).  

### Blur algorithm  
I use pixelate algorith to make it the most lively it can be. Basically I just divide the face I detected to several squares of hxh size and then use mean blur of opencv to blur that square. Finally, we concatenate those squares to have a final result  

### Bad/Good guy classification  
In this case, we will judge a book just by its cover. We will mark a person is good or bad just by their face. To do this, I build a model that I fine-tuning from the the pretrained model EfficientNetV2B0 of TensorFlow.

## Some results:  
### Model results:

