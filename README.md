# Tests out the performance characteristics of the google load balancers

* Dockerfile - builds a locust master/worker image
* kubernetes - configuration of masters/workers
* licenses - license files from various dependencies
* locust-tasks - locust scripts
* test-endpoints - contains test endpoints (echo servers) to respond to worker requests

## Basic Information
We'll be generating load in a BACKEND cluster using http://locust.io. We will
servicing the load using 3 load balancer configurations.
1. Kubernetes Service Type of LoadBalancer
1. Kubernetes Service Type of LoadBalancer with an NGINX side car for TLS termination
1. Kubernetes Ingress with a GCP HTTPS loadbalancer.

## Get started
1. git clone https://github.com/pbrumblay/lb-test

## Set up the FRONTEND GKE cluster

1. cd lb-test/test-endpoints
1. Connect to and authenticate with the FRONTEND GKE cluster. We'll set up
our nodes and "echo" endpoints here.
1. ./makesecret.sh
1. kubectl apply -f loadbalancertest.yaml
1. kubectl get svc  
Make note of the external IP addresses assigned to echoserver-https-httpsloadbalancer and echoserver-https-httpsloadbalancer
1. kubectl get ingress  
Make note of the ingress IP used in the HTTP load balancer.
1. kubectl get pods  
Ensure that the pods come up without error.

## Set up the BACKEND GKE cluster
1. Return to the root of where you cloned lb-test. (i.e. "cd .."")
1. cd lb-test/kubernetes
1. Connect to and authenticate with the BACKEND GKE cluster. We'll set up our locust
load generators here.
1. Modify locust-master-deployment.yaml and locust-worker-deployment.yaml. Change these environment variables according to the IPs you noted when you set up the FRONTEND cluster:

    ```
    - name: NOSSLURL
      value: http://<IP OF NLB WITHOUT SSL ENDPOINT>/ssl/nosslno
    - name: SIDECARURL
      value: https://<IP OF NLB WITH SSL SIDECAR>/ssl/sidecar
    - name: HTTPSLBURL
      value: https://<IP OF HTTPSLB ENDPOINT (FROM INGRESS)>/ssl/httpslb
    ```
    Note that 2 of the URLs use HTTPS, and one uses HTTP.
1. Create the load generator endpoints.
    1. kubectl apply -f locust-master-deployment.yaml
    1. kubectl apply -f locust-worker-deployment.yaml
    1. kubectl apply -f locust-master-service.yaml
1. kubectl get svc  
Make note of the ip for the service locust-master-lbtest
1. kubectl get pods  
Make sure that the pods come up without error.

## Run a load test to generate load
1. Connect to the master endpoint at http://`<`IP from backend locust-master-lbtest service`>`:8089
1. Generate load using 50 slaves with a hatch rate of 5 per second.
1. Let it run and observe the statistics. If you wait long enough, you'll see spikes with the load balancer style endpoints.
