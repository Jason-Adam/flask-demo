# ResNet-50 Model Deployed to API Endpoint  
This repo contains everything needed to deploy a pre-trained ResNet-50 CNN as an API endpoint utilizing Flask, Gunicorn, Nginx, and Docker.  

## ResNet-50
ResNet-50 refers to a 50 layer residual neural network that is commonly used to classify images. ResNet-50 was trained on more than a million images from the ImageNet databaseand can classify images into 1000 object categories. The use of a wide array of images resulted in rich feature representations that can be applied to very broadly.  

## Deploy the API  
The API can be deployed locally using `docker-compose`. The following commands will launch the flask API on your localhost.  

```bash  
docker-compose build  
docker-compose up
```  

Once you've deployed the model (it takes a few seconds for the ResNet-50 model to load), you can send image requests to it with the following command:  

```bash  
curl -X POST -F image=@imgs/husky.jpg "https://localhost:5000"
```  

You should receive a JSON response object with predictions for the image.
