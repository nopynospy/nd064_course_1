# nd064_C1
## Cloud Native Fundamentals Scholarship Program Nanodegree Program

**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji

**Student**: https://www.linkedin.com/in/kelvin-tan-2086011a3/

This is the final project for the programme that I enrolled in March 2023.

At the time of this writing, I work as a devops engineer in the mobile games industry. I felt a need to upskill myself and came across a Facebook ad about a devops programme sponsored by SWIFT.

### Project Steps

In this project, I forked the original repo from my instructor. The  changes made were:

<ol>
    <li> Best Practices For Application Deployment
    <li> Docker for Application Packaging
    <li> Continuous Integration with GitHub Actions
    <li> Kubernetes Declarative Manifests
    <li> Helm Charts
    <li> Continuous Delivery with ArgoCD
    <li> Standout Suggestions (Optional)
        <ol>
            <li>Dynamic Healthcheck endpoint
            <li>Push Docker images with custom tags
            <li>Helm chart conditionals
        </ol>
</ol>

### Challenges Faced

I encountered some additional challenges outside of the project steps.

<ol>
    <li><b>Vagrantfile private_network ip conflict</b><br>
        Somehow the original <code>192.168.50.4</code> has a conflict on my Linux Mint, so I modified it to <code>192.168.56.4</code> in order for vagrant to build the vm.
    <li><b>Github action pytest: "Error: Version X with arch x64 not found"</b><br>
        ![job failed text](https://github.com/nopynospy/nd064_course_1/blob/main/project/screenshots/ci-github-actions_pytest_failed.png)<br>
        My pytest kept failing in github action.<br>
        ![job failed detailed text](https://github.com/nopynospy/nd064_course_1/blob/main/project/screenshots/ci-github-actions_pytest_failed_python.png)<br>
        I fixed the issue by referring to [the list of available python versions in git action](https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json)<br>
        I found out the cause was in the dockerfile, ubuntu latest is used (which is <code>22.04</code>), so I replaced <code>python-version: [2.7, 3.5, 3.6, 3.7, 3.8]</code> with <code>ppython-version: ["2.7x", "3.7x", "3.8x"]</code> because there is no 3.5 and 3.6 for 22.04 and 'x' basically means let the git action use any compatible minor python version.<br>

</ol>

### Installation

```
# Clone this repo
git clone https://github.com/nopynospy/nd064_course_1.git

# cd into project directory
cd nd064_course_1/project

# Create vm
vagrant up

# Ssh into vm
vagrant ssh

# Install kubectl
curl -sfL https://get.k3s.io | sh -

# Wait for a few minutes for k3s to get started
sudo su
k3s kubectl get node

# Install argocd
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Set up argocd
curl -o argocd-server-nodeport.yaml https://github.com/udacity/nd064_course_1/blob/main/solutions/argocd/argocd-server-nodeport.yaml
kubectl apply -f argocd-techtrends-staging.yaml

# Get encoded password
kubectl get secret argocd-initial-admin-secret -n argocd -o yaml

# Get password and login at https://192.168.56.4:30008/
# Login id is admin
# Decrypt password with the command below and replace encoded_password
echo encoded_password | base64 --decode

# Set up staging and prod applications
curl -o argocd-techtrends-staging.yaml https://github.com/nopynospy/nd064_course_1/blob/main/project/argocd/argocd-techtrends-staging.yaml
kubectl apply -f argocd-techtrends-staging.yaml
curl -o argocd-techtrends-prod.yaml https://github.com/nopynospy/nd064_course_1/blob/main/project/argocd/argocd-techtrends-prod.yaml
kubectl apply -f argocd-techtrends-prod.yaml
```

### References

<ol>
<li>[How to structure, package, and release an application to a Kubernetes cluster, while using an automated CI/CD pipeline]
(https://medium.com/@nisalikularatne/how-to-structure-package-and-release-an-application-to-a-kubernetes-cluster-while-using-an-b1f597289e93)
</ol>