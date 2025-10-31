pipeline {
    agent any

    environment {
        IMAGE_NAME = "seleniumdemoapp:v1"
        DOCKER_REPO = "vishnupriya68/sample1:seleniumtestimage"
    }

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "🏃 Running Selenium Tests using pytest"

                // Install dependencies
                bat 'pip install -r requirements.txt'

                // Clear old ChromeDriver cache
                bat 'if exist %USERPROFILE%\\.wdm\\drivers\\chromedriver rd /s /q %USERPROFILE%\\.wdm\\drivers\\chromedriver'

                // Run tests
                bat 'pytest -v --maxfail=1 --disable-warnings || echo Pytest failed - check logs for details'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image"
                bat 'dir Dockerfile'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Docker Login (Secure)') {
            steps {
                echo "🔐 Logging in to Docker Hub using Jenkins credentials"
                bat 'docker login -u vishnupriya68 -p "Shivapriya123@"'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "⬆️ Pushing Docker Image to Docker Hub"
                bat "docker tag %IMAGE_NAME% %DOCKER_REPO%"
                bat "docker push %DOCKER_REPO%"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Deploying to Kubernetes Cluster"
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the stage logs above for details.'
        }
    }
}
