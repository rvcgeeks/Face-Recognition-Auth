# Rvc Face Recognition authorisation

An OpenCV based Local Binary Pattern Histogram (LBPH) face Recognition
authorisation system with arduino support for door locks.

## Features

1) Supports on Raspberry Pi as well as webcam on PC
2) Can connect arduino for servo control for door lock or barrier boom
3) Fast and live Recognition of trained Face
4) Multiple faces via Ids supported

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This application was tested on Kali Linux 2019.3

1) opencv_contrib_python (for camera interface and face Recognition)
2) if arduino support, pyfirmata library and arduino board with atleast 2 LEDs

## Deployment

The following steps will guide you setting up the libraries and launching the Id generator.

1) Face Registration

to register a face into the system, we have two steps. I.e. dataset creation and second training and creating a model
In dataset preparation, face is captured by opencv using a pretrained default [haar cascade](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) 
these images are then trained using LPBH and the model is saved to model.yml aside.

1.1) Dataset preparation

To create a dataset for face id '1' run, 
```
python face_recognition.py g 1
```
note that face id can only be an integer. After this the webcam starts capturing images of your face and
its frames are stored in datasets/(face id)/(sample no).jpg
At this time, one registers multiple faces with ids 2,3,4,... 

1.2) Training

To train the model run,
```
python face_recognition.py t
```
after this model.yml is created. Donot rename this file. If done modify code accordingly.

2) Face Recognition

If arduino board is connected with the computer, it will perform the actions according to the code written if 
face is recognized in a separate thread to prevent delay of video capture. If not connected it wont cause any error
other than a warning message of absence of arduino. To start video run
```
python face_recognition r
```
If the confidence if detection > 50% then that face is considered to be 'recognized' and the gate connected to arduino opens.

## Author

* **Rajas Chavadekar** 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

