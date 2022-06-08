# Autoscaling Computer Vision Inference in the Cloud

## Overview

This repository consolidates the code used and results collected from experimenting with **autoscaling Computer Vision (CV) inference instances** in the cloud. Before we proceed further, a couple of terms will be explained in the following paragraphs.

What is a **CV inference instance**? Here, I define it as a **single** virtual machine (VM) or serverless application, running a CV AI model such as YOLO for object detection. For example, an instance receives an image of this cute Shiba Inu, and the CV model correctly infers that it is a "Dog", returning the predicted image with a superimposed bounding box and label.

<img src='images/shiba_inu_prediction.jpeg' width='500'><br>
*CV Inference on Dog*

What about **autoscaling**? It is a cloud computing feature that dynamically adjusts the number of compute resources (such as VMs) as the load varies. This has several advantages compared to a fixed machine - if the load decreases, scaling down reduces costs, while if the load increases, scaling out allows the demand to be met. There's [scaling out versus scaling up](https://packetpushers.net/scale-up-vs-scale-out/#:~:text=Scaling%20out%20%3D%20adding%20more%20components,it%20can%20handle%20more%20load.) - for the purposes of this project, we will solely focus on scaling out.

<img src='images/scaling_out.jpeg' width='300'><br>
*Scaling Out with AWS*

Combining what we now know, the following use cases will benefit from the ability to **autoscale CV inference instances**:
- An API where users submit images for inference - the ability to scale down will help to save costs
- A system where the load fluctuates depending on the number of CCTVs, detected instances etc - the ability to scale out will help to maintain a consistent FPS
- Splitting a video feed into frames which are inferred by multiple, cheap CPU instances instead of a single but more expensive GPU VM. This can theoretically be done for models without time aspect (so this excludes object tracking), as each video frame can be inferred independently of other video frames. Each frame has an associated time-stamp, so if there is a need to retrieve all the inferred result in sequence, they can be sorted in post-processing.

## Architecture

The architecture used for these experiments is shown below. It can be described in 3 parts:
1. **Client** - A load testing tool is used to create multiple clients. Each client encodes an image into [base64 format](https://www.geeksforgeeks.org/python-convert-image-to-string-and-vice-versa/), and makes a POST request to the server with the encoded message. This is used to simulate some of the use cases described previously.
2. **Server** - Hosted on the cloud. A load balancer allows all POST requests be made to a common URL, and increases or decreases the number of instances depending on the load.
3. **Storage** - Hosted on the cloud. Stores the inference results from each server instance in .jpeg format.

<img src='diagrams/architecture.drawio.svg'><br>
*Architecture Diagram*

## Tools Used

Google Cloud Platform (GCP) is the cloud computing service used here (AWS or Microsoft Azure are other options). While GCP has several services which support autoscaling, we will be focusing on these two:

| Service | Pros | Cons |
|---------------------------------------------------------|-------|-------|
| [Google App Engine](https://cloud.google.com/appengine) |  - Serverless and easy to deploy | - Least control over deployment <br> - Limited compute resource (max 2GB RAM) <br> - Does not support containers | 
| [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine) | - More compute power <br> - Supports containers <br> - More control over K8s clusters and VMs | - More effort to set up

App Engine and Kubernetes Engine were chosen because they are at the 2 extremes, but other possible services that are somewhat in-between are [Cloud Run](https://cloud.google.com/run) and [Compute Engine Managed Instance Groups (MIGs)](https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances).

Other key tools used in this study are:
- [Locust](https://locust.io/) - An open source load testing tool which will create multiple client instances to send POST requests to the load balancer on GCP
- [Google Cloud Storage](https://cloud.google.com/storage) - Object storage to store the resulting image files from CV inference
- [PeekingDuck](https://github.com/aimakerspace/PeekingDuck) - A CV inference framework. Each instance will be running it's own copy of PeekingDuck.
- [FastAPI](https://fastapi.tiangolo.com/) - A high performance web framework that will be used as the server for each instance. [Flask](https://flask.palletsprojects.com/en/2.1.x/) was used initially, but it did not perform as well as FastAPI as it is a development server.


## Google App Engine



Num users 1000
Spawn rate 100/sec

<img src='images/app_engine/1_inst_1000_users_100_spawn_rate.png' width='500'><br>
*Limited to 1 instance - 16% failure*

<img src='images/app_engine/unlimited_inst_1000_users_100_spawn_rate.png' width='500'><br>
*No limit to instances - 0% failure*


<img src='images/app_engine/app_engine_instances.png' width='500'><br>