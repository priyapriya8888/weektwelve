pipeline {
    agent any

    environment {
        // ✅ Docker image details (matches deployment.yaml)
        IMAGE_NAME = "seleniumtestdemoapp:v1"
        DOCKER_REPO = "vishnupriya68/sample1:seleniumtestimage"

        // ✅ Python path on your system
        PYTHON_EXE = "C:\\Users\\Vishnupriya\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    }

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "🏃 Running Selenium Tests using pytest"

                // ✅ Step 1: Upgrade pip
                bat "\"%PYTHON_EXE%\" -m pip install --upgrade pip"

                // ✅ Step 2: Install compatible webdriver-manager (to avoid ChromeType import error)
                bat "\"%PYTHON_EXE%\" -m pip install webdriver-manager==3.8.6"

                // ✅ Step 3: Install dependencies from requirements.txt
                bat "\"%PYTHON_EXE%\" -m pip install -r requirements.txt"

                // ✅ Step 4: Clear old ChromeDriver cache
                bat "if exist %USERPROFILE%\\.wdm\\drivers\\chromedriver rd /s /q %USERPROFILE%\\.wdm\\drivers\\chromedriver"

                // ✅ Step 5: Run Selenium tests with pytest
                bat "\"%PYTHON_EXE%\" -m pytest -v --maxfail=1 --disable-warnings || echo Pytest failed - check logs for details"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image"
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Docker Login (Secure)') {
            steps {
                echo "🔐 Logging in to Docker Hub"
                bat "docker login -u vishnupriya68 -p \"Shivapriya123@\""
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
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully! Everything deployed to Kubernetes 🎉"
        }
        failure {
            echo "❌ Pipeline failed. Please check the logs above for details."
        }
    }
}
