# SoftwareX
# CoCoStyle
CocoStyle is an AI based mixed initiative co-creative system that supports three creative fashion design process which is research, design, and improvement.


## Local server setup
### System requirments:
-   We tested in Python 3.8.5 and PyTorch 1.13.1 with CUDA 11.8 and RTX 4070ti.

### Frontend:
---

#### Environment installation
 1. Install ([NodeJS](https://nodejs.org/en/download/))
2. Install ([npm](https://www.npmjs.com/))
 3. Install a package through the -g flag will install the package in the system folder.
 
        npm install -g n
 4. Install the stable version through a plug-in that manages the Node.js version 
 
         n stable
 
5. Inside the `frontend` directory, install dependencies by running the following command in the terminal:
 
         n stable
 
6. Go to the  frontend directory `/src/QuQu/QuQu/`, build the application by running the following command in the terminal
 
         npm run build
 
 7. Launch the frontend application by running the following command in the terminal within the `/src/QuQu/QuQu/` directory: 
 
          npm start
 
 
 8. Access the frontend of the platform from React by visiting:  
		
 		127.0.0.1:3000 
 
 #### Enabling S3
To enable S3 for images, go to `src/QuQu/QuQu/src/ququ.config.js` and enter your AWS.

    149. ####INPUT S3 INFO
	149. ACCESS_KEY =  ''
	150. SECRET_ACCESS_KEY =  ""
	151. REGION =  ""
	152. S3_BUCKET =  ''
 


## Backend:



#### Environment installation

To work with this project on your own machine, you need to install the environment as follows:

```bash
conda env create -f environment.yml
conda activate CoCoStyle
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install nvidia-pyindex
pip install nvidia-tensorflow[horovod]
pip install nvidia-tensorboard==1.15
pip install paddleseg==2.5.0
pip install paddle
pip install paddlepaddle
pip install -U openmim
mim install mmcv-full==1.7.1
pip install mmdet==2.27.0
pip install cvlib=0.2.7
pip install einops
pip install pytorch_transformers==1.2.0
pip install extcolors
pip install wandb
```


#### Enabling S3
To enable S3 for images, go to QuQu-backend/ququ_backend/settings.py and enter your AWS.

    149. ####INPUT S3 INFO
	149. ACCESS_KEY_ID =  ''
	150. ACCESS_SECRET_KEY =  ""
	151. AWS_DEFAULT_REGION =  ""
	152. BUCKET_NAME =  ''
  
#### Input user name 

Enter the user name in QuQu-backend/ququ/views.py to distinguish between users when saving the log.

    38. ###INPUT USER INFO
    39. global_user_name =  ""

### Download the file

Go to https://drive.google.com/file/d/12vOtPhA6OcndJR5G0o-GUI30ob9SAhM3/view?usp=drive_link and move the downloaded database to src/QuQu-backend/

Go to https://drive.google.com/file/d/1lMDldYc12J1zw6AnXefpwNBUVHwpdR0W/view?usp=drive_link and move the downloaded HumanGAN file to src/QuQu-backend/ququ/apicode/
Go to 
https://drive.google.com/file/d/1nKUg2nqSgv4AvNlXKi-wMP5NJzUI9I0c/view?usp=drive_link and move the downloaded pth file to src/QuQu-backend/ququ/

#### Django
Construct Django environment.

```bash
pip3 install Django
pip install django-cors-headers
pip install djangorestframework
cd src/
python3 manage.py migrate
```

Run Django server.

```bash
python manage.py runserver
```



