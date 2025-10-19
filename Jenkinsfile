pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')  
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-id')  
        DOCKER_IMAGE = "jay16nair/blue-green-demo"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Get current live version (blue or green)
                    def color = bat(script: 'kubectl get svc myapp-service -o jsonpath="{.spec.selector.version}" || echo blue', returnStdout: true).trim()
                    def newColor = color == "blue" ? "green" : "blue"
                    env.NEW_COLOR = newColor

                    // Build Docker image
                    bat "docker build -t ${DOCKER_IMAGE}:${newColor} --build-arg APP_COLOR=${newColor} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                // Login and push to Docker Hub
                bat """
                    docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}
                    docker push ${DOCKER_IMAGE}:${NEW_COLOR}
                """
            }
        }

        stage('Deploy New Version') {
            steps {
                script {
                    bat "kubectl apply -f k8s-${NEW_COLOR}.yaml"
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    bat "kubectl patch service myapp-service -p \"{\\\"spec\\\":{\\\"selector\\\":{\\\"app\\\":\\\"myapp\\\",\\\"version\\\":\\\"${NEW_COLOR}\\\"}}}\""
                }
            }
        }

        stage('Clean Up Old Deployment') {
            steps {
                script {
                    def oldColor = env.NEW_COLOR == "blue" ? "green" : "blue"
                    bat "kubectl delete deployment ${oldColor}-deployment --ignore-not-found=true"
                }
            }
        }
    }
}
