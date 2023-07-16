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
Recently, we have witnessed a surge in television reportages highlighting serious crimes, with the criminals frequently having their faces obscured. As an editor working on such footage, one can imagine the immense amount of time and effort required to manually blur an individual's face. To address this challenge and streamline the process, I have developed an application that simplifies the task. By simply uploading the clip featuring the person whose face needs to be blurred, the app will automatically apply the necessary blurring effect, saving valuable time and effort in the editing process.

## Installing and running  
Download this repository, installing all the requirement packages by pip and then run the main.py file.  

## Technology
### To detect people's face  
I use a dnn caffemodel that opencv introduce cause it have the best performance on video. Models can be found in /models.  
For a deeper reason why I use this model, please visit [here](https://towardsdatascience.com/face-detection-models-which-to-use-and-why-d263e82c302c). 

### Blur algorithm  
In order to achieve the most realistic and effective blurring effect, I have implemented a pixelation algorithm in the application. The algorithm works by detecting the face in the uploaded clip and dividing it into multiple square regions of size h by h. Using OpenCV's mean blur technique, each square is blurred individually. Finally, these squares are concatenated to produce the final result. This approach ensures that the blurring effect is both accurate and visually appealing, providing a lively and professional output for the edited clip.

### Bad/Good guy classification  
In this case, we will judge a book just by its cover. We will mark a person is good or bad just by their face. To do this, I build a model that I fine-tuning from the the pretrained model EfficientNetV2B0 of TensorFlow.  

## Some results
### Model results
_ In the caffemodel, i just use the weight they give in the .caffemodel file.  
_ With EfficientNetV2B0, i freeze 70% layers of pretrain model and save the new weight in .h5 file, i implement simply by using model.load_weight(). Here are some results of this model.  
![image](https://github.com/lqkhanh195/BlurBadGuyFaces4Video/assets/131540429/2e5327e4-7c50-4bd5-8eec-a415bb29830a)
Loss and accuracy on training set and test set  
![image](https://github.com/lqkhanh195/BlurBadGuyFaces4Video/assets/131540429/62da98ce-fb3b-4c87-ba55-d953effc398f)
Confusion matrix  
_ The presented confusion matrix indicates positive outcomes as it effectively avoids misclassifying individuals with criminal intent as innocent individuals, thereby preventing their faces from being inadvertently blurred. It demonstrates the accuracy and reliability of the face-blurring process, ensuring that the appropriate individuals are identified and their privacy is protected while maintaining the overall integrity of the footage.  
### Demo  
[Demo Video] (https://drive.google.com/file/d/18Co4M58ikqoAde51lT6ahUxKEp_whpb1/view?usp=sharing)

## Downside
Doesnt have a good speed and bad multiprocessing handling.     
30fps is default for ouput.  
I encountered issues while attempting to use the .pyw file extension for the main.py file, as well as exporting the entire application to an .exe file, maybe because of bad path handling.  
Have some bias in dataset like: emotion, glass, hair, beard.  

## More infomation
You can have more infomation in the .docx report file, but this file is written by Vietnamese.
