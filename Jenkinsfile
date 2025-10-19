pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')  // Add in Jenkins
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-id')  // Optional if using Docker Desktop
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
                    def color = sh(script: "kubectl get svc myapp-service -o jsonpath='{.spec.selector.version}' || echo blue", returnStdout: true).trim()
                    def newColor = color == "blue" ? "green" : "blue"
                    env.NEW_COLOR = newColor

                    sh "docker build -t ${DOCKER_IMAGE}:${newColor} --build-arg APP_COLOR=${newColor} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker push ${DOCKER_IMAGE}:${NEW_COLOR}
                """
            }
        }

        stage('Deploy New Version') {
            steps {
                script {
                    sh "kubectl apply -f k8s-${NEW_COLOR}.yaml"
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    sh "kubectl patch service myapp-service -p '{\"spec\":{\"selector\":{\"app\":\"myapp\",\"version\":\"${NEW_COLOR}\"}}}'"
                }
            }
        }

        stage('Clean Up Old Deployment') {
            steps {
                script {
                    def oldColor = env.NEW_COLOR == "blue" ? "green" : "blue"
                    sh "kubectl delete deployment ${oldColor}-deployment --ignore-not-found=true"
                }
            }
        }
    }
}
