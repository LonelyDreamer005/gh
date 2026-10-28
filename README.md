
# Flask DevOps Project — Revision Notes

This project covers Flask API development, automated testing, Docker, Git/GitHub, GitHub Actions, Docker Hub, and Kubernetes using Minikube in Google Cloud Shell.

## 1. Overall Workflow

```text
Flask Application
      |
      v
API Testing with pytest
      |
      v
Docker and Docker Compose
      |
      v
Git and GitHub
      |
      v
GitHub Actions (CI)
      |
      v
Build and Publish Docker Image
      |
      v
Docker Hub
      |
      v
Kubernetes Deployment
      |
      v
Kubernetes Service
      |
      v
Test using port-forward
```

## 2. Run the Flask Application

### Commands

```bash
python --version
ls
python app.py
```

Test the API from another terminal:

```bash
curl http://localhost:5000/
```

### Purpose

- `python --version`: Checks the Python version.
- `ls`: Lists project files.
- `python app.py`: Starts the Flask application.
- `curl`: Sends an HTTP request to the API.

The Flask application uses port `5000`.

## 3. Docker and Docker Compose

### Commands

```bash
docker --version
docker compose up --build
```

Inspect images and containers:

```bash
docker images
docker ps
docker ps -a
```

View container logs:

```bash
docker logs container_v
```

Stop the application:

```bash
docker compose down
```

### Purpose

- **Dockerfile:** Defines how to build the application image.
- **compose.yaml:** Defines how to run the application's containers.
- **Docker image:** Packages the application and its dependencies.
- **Container:** A running instance of an image.
- `docker compose up --build`: Builds the image and starts the configured services.
- `docker ps`: Lists running containers.
- `docker ps -a`: Lists running and stopped containers.

## 4. Automated API Testing

Install pytest:

```bash
pip install pytest
```

Run tests:

```bash
python -m pytest -v
```

### Purpose

- `pytest` discovers and executes tests.
- `-v` displays detailed test results.
- Tests help detect errors before changes are published.

The test file used in this project is `app_test.py`.

## 5. Git and GitHub Setup

### Configure Git

```bash
git config --global user.name "YOUR_GITHUB_USERNAME"
git config --global user.email "YOUR_EMAIL"
```

### Authenticate using GitHub CLI

```bash
gh --version
gh auth login
gh auth status
```

### Check repository status

```bash
git status
git branch
git remote -v
```

### Initialize a repository if required

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Only add the remote if it does not already exist.

### Standard Git workflow

```bash
git status
git diff
git add .
git commit -m "Describe your changes"
git push -u origin main
```

After the upstream branch is configured, you can usually use:

```bash
git push
```

### Purpose

- `git add`: Stages changes.
- `git commit`: Saves a snapshot locally.
- `git push`: Uploads commits to GitHub.
- `git status`: Shows changed and staged files.
- `git diff`: Displays unstaged changes.

**Security:** Never commit passwords, access tokens, service-account keys, or private configuration files.

## 6. GitHub Actions — Continuous Integration

### Workflow directory

```text
.github/
└── workflows/
    ├── ci.yml
    └── cd.yml
```

Create the directory:

```bash
mkdir -p .github/workflows
```

### Commit the CI workflow

```bash
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI"
git push origin main
```

### What CI does

A typical CI workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies.
4. Runs automated tests.

For example:

```bash
python -m pytest -v
```

The exact behavior depends on the contents of `ci.yml`.

Check workflow results under **GitHub → Actions**.

## 7. Docker Image Publishing

### Docker Hub image

The image used in this project is:

```text
vinay1030/fl:latest
```

Pull the image:

```bash
docker pull vinay1030/fl:latest
```

Inspect local images:

```bash
docker images
```

### GitHub Actions secrets

The publishing workflow uses these repository secrets:

- `DOCKER_USERNAME`
- `DOCKER_TOKEN`

The workflow logs in to Docker Hub, builds the image, and pushes it to the repository.

### Commit the publishing workflow

```bash
git add .github/workflows/cd.yml
git commit -m "Configure Docker image publishing"
git push origin main
```

Check the result under **GitHub → Actions** and verify the image on Docker Hub.

**Important:** Publishing an image is not the same as deploying it to Kubernetes.

## 8. Start Kubernetes with Minikube

### Check the tools

```bash
kubectl version --client
minikube version
```

### Start the cluster

```bash
minikube start --driver=docker
```

Check the cluster:

```bash
minikube status
kubectl get nodes
```

### Purpose

- `kubectl`: Communicates with Kubernetes.
- `minikube`: Runs a local Kubernetes learning cluster.
- `kubectl get nodes`: Checks whether the cluster is available.

This project uses Minikube inside Google Cloud Shell, not Google Kubernetes Engine (GKE).

## 9. Create a Kubernetes Deployment

Run:

```bash
kubectl create deployment tstkub --image=vinay1030/fl:latest
```

Check the Deployment and Pods:

```bash
kubectl get deployments
kubectl get pods
```

### Purpose

A Deployment manages the application's Pods and ensures the desired number of replicas is running.

## 10. Expose the Application with a Service

Run:

```bash
kubectl expose deployment tstkub \
  --type=NodePort \
  --port=5000 \
  --target-port=5000
```

Check the Service:

```bash
kubectl get services
```

### Purpose

- `--type=NodePort`: Exposes the Service through a port on cluster nodes.
- `--port=5000`: Defines the Service port.
- `--target-port=5000`: Defines the application container port.

## 11. Access the Application

Run:

```bash
kubectl port-forward service/tstkub 5000:5000 --address 0.0.0.0
```

Keep the command running.

From another terminal, test the API:

```bash
curl http://localhost:5000/
```

Cloud Shell also supports **Web Preview → Preview on port 5000**.

Port forwarding is temporary and is intended for testing, not permanent public access.

## 12. Kubernetes YAML Configuration

### Directory structure

```text
k8s/
├── deployment.yaml
└── service.yaml
```

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tstkub
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-container
          image: vinay1030/fl:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5000
```

### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: tstkub
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080
```

### Important concepts

- `tstkub`: Deployment and Service name.
- `flask-container`: Container name.
- `flask-app`: Pod label used by the Service selector.
- `vinay1030/fl:latest`: Docker image reference.

The Service selector must match the Pod labels:

```yaml
selector:
  app: flask-app
```

### Apply the YAML files

From the project root:

```bash
kubectl apply -f k8s/
```

Verify the resources:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl rollout status deployment/tstkub
```

### Debugging commands

```bash
kubectl describe deployment tstkub
kubectl describe pods
kubectl logs deployment/tstkub
```

### Immutable selector issue

A Deployment's selector cannot be changed after creation. During development, a selector mismatch was resolved by deleting and recreating the Deployment:

```bash
kubectl delete deployment tstkub
kubectl apply -f k8s/
```

Only do this when necessary, because deleting a Deployment interrupts its Pods until it is recreated.

## 13. Commit Kubernetes Configuration

After adding or updating the YAML files:

```bash
git status
git diff
git add k8s/
git commit -m "Add Kubernetes Deployment and Service"
git push origin main
```

Kubernetes YAML should be tracked in Git. Credentials and private cluster configuration should not be committed.

## 14. Quick Command Reference

| Task | Command |
|---|---|
| Run Flask | `python app.py` |
| Run tests | `python -m pytest -v` |
| Start Docker Compose | `docker compose up --build` |
| Stop Docker Compose | `docker compose down` |
| List images | `docker images` |
| List containers | `docker ps -a` |
| Check Git changes | `git status` |
| Push changes | `git push` |
| Check Kubernetes nodes | `kubectl get nodes` |
| List Kubernetes resources | `kubectl get deployments,pods,services` |
| Apply Kubernetes YAML | `kubectl apply -f k8s/` |
| Check rollout | `kubectl rollout status deployment/tstkub` |
| View logs | `kubectl logs deployment/tstkub` |
| Forward port | `kubectl port-forward service/tstkub 5000:5000` |

## 15. Final Workflow to Remember

1. Write or modify the Flask application.
2. Run the automated tests.
3. Build and test the application using Docker.
4. Commit and push the code to GitHub.
5. GitHub Actions runs the configured CI workflow.
6. GitHub Actions builds and publishes the Docker image.
7. Kubernetes Deployment specifies which image to run.
8. Kubernetes Service provides network access to the Pods.
9. Verify the rollout and test the API.

```text
Source Code
    ↓
pytest
    ↓
Docker
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Docker Hub
    ↓
Kubernetes Deployment
    ↓
Kubernetes Service
    ↓
API Testing
```

## 16. What Still Needs Verification

The command history shows that these tools and steps were used, but it does not prove that every workflow is currently passing.

Verify separately:

- Whether the CI workflow passes.
- Whether the image-publishing workflow passes.
- Whether Docker Hub receives the latest image.
- Whether the Kubernetes Pods are running.
- Whether the Flask API is accessible through port forwarding.
- Whether GitHub Actions automatically deploys new images to Kubernetes.

The current Minikube cluster in Cloud Shell is useful for learning. GitHub-hosted Actions runners cannot automatically reach it without additional connectivity and authentication configuration.

### Core Concepts

- **Git:** Tracks source-code changes.
- **GitHub:** Hosts the repository.
- **GitHub Actions:** Automates workflows.
- **Docker:** Packages the application.
- **Docker Hub:** Stores container images.
- **Kubernetes:** Runs and manages containers.
- **Deployment:** Manages application Pods.
- **Service:** Provides a stable network endpoint for Pods.
- **CI:** Tests and validates changes.
- **CD:** Delivers or deploys changes to an environment.
