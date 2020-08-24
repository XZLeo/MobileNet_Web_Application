# MobileNet_Web_Application
Use Flask framework and fine-tuning MobileNet weights from Keras to build a simple AI web application.

**Core Function**: Classify the input image to dog or cat..yeah, pretty simple function.

## Why Flask, Keras and MobileNet?

Python is not the mainstream option for web development, however, it would be much easier to embed the machine learning script into a app developed with Python. And Flask is a light-weight framework for beginners. I don't know anything about JavaScript, but Jinja2 provides simple (but ugly) solution for the front end. Therefore, I chose Flask.

As for Keras, it offers pretrained weights for different calssic models, very easy to do transfer learning. Since it's only a local project without GPU server, Mobilenet is a good option to run on CPU. Actually there are more efficient models, like ShuffleNet.


## Environment
keras                     2.0.8  
tensorflow                1.2.1  
flask                     0.12.2  
python                    3.5.2

## Run the app
1. git clone this repo
2. set up the virtual environment
3. go to the path of python.exe
```
set FLASK_APP=path
set FLASK_ENV=development
flask run
``` 
where the `path` is the absolute path of app.py
Note: Use `export` instead of `set` on Linux OS. There should be no space around `=`！

## Functions
The app allows users to upload jpg or png images of cats or dogs and returns the classification and probability. It allows the user to provide feedback about the classification and use it to update the weights of MobileNet.

## Structure
│  app.py  
│  repredict.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;load weights to classify  
│  TryMobile.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Update weights  
├─static  
│  │  cats_dog_mobileNet.h5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;weights after transfer learning  
│  │  files_cat.npy  
│  │  files_dog.npy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;numpy array to save paths of newly labeled images  
│  │  style.css  
│  └─images  
│      │             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                 save unlabeled input images  
│      ├─Cat  
│      │             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                 save images labeled as 'Cat' for updating weights  
│      └─Dog  
├─templates  
│      show.html          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            the interface to upload images  
│      thanks.html  
│      upload.html        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            show the classification result and users can give feedbacks  
└─uploads                             


