# MobileNet_Web_Application
Use Flask framework and fine-tuning MobileNet weights from Keras to build a simple AI web application.

## Environment
keras                     2.0.8  
tensorflow                1.2.1  
flask                     0.12.2  
python                    3.5.2

## Run the app
1. git clone this repo
2. set up the virtual environment
3. 
```
set FLASK_APP=path
set FLASK_ENV=development
flask run
``` 
where the `path` is the absolute path of app.py
Note: Use `export` instead of `set` on Linux OS. There should be no space around `=`！

## Functions
The app allows users to upload jpg or png images of cats or dogs and returns the classification and probability. It allows the user to provide feedback about the classification and use it to update the weights of MobileNet.
