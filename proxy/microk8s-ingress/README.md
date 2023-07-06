# microk8s-ingress-example

Steps
1. Install MicroK8s
Microk8s quickstart link

sudo snap install microk8s --classic
microk8s.start

2. Install Ingress Dependent Resources
microk8s.kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml

3. Enable Ingress Addon
microk8s.enable ingress

4. Run a local Docker Registry
You can skip this step if you wanna host your image on a public/private repository.

docker run -p 5000:5000 registry

5. Clone Example Repository And Build Docker Image
git clone https://github.com/kendricktan/microk8s-ingress-example
cd microk8s-ingress-example

docker build . -t my-microk8s-app
docker tag my-microk8s-app localhost:5000/my-microk8s-app
docker push localhost:5000/my-microk8s-app

6. Run Applications And Ingress
microk8s.kubectl apply -f bar-deployment.yml
microk8s.kubectl apply -f foo-deployment.yml
microk8s.kubectl apply -f ingress.yml

7. Expose Deployments to Ingress
If you skip this step you'll get a 503 service unavailable

microk8s.kubectl expose deployment foo-app --type=LoadBalancer --port=8080
microk8s.kubectl expose deployment bar-app --type=LoadBalancer --port=8080

8. Testing Endpoint Out
curl -kL https://127.0.0.1/bar
curl -kL https://127.0.0.1/foo
