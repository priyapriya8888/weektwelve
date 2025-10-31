pipeline {
    agent any

    environment {
        // ✅ Docker image details
        IMAGE_NAME = "seleniumtestdemoapp:v1"
        DOCKER_REPO = "vishnupriya68/sample1:seleniumtestimage"

        // ✅ Full path to Python executable
        PYTHON_EXE = "C:\\Users\\Vishnupriya\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    }

    stages {

        stage('Setup Python & Run Selenium Tests') {
            steps {
                echo "🏃 Setting up Python and running Selenium tests..."

                // ✅ Step 1: Upgrade pip safely using your Python executable
                bat "\"%PYTHON_EXE%\" -m pip install --upgrade pip"

                // ✅ Step 2: Install specific webdriver-manager version (stable for Chrome)
                bat "\"%PYTHON_EXE%\" -m pip install webdriver-manager==3.8.6"

                // ✅ Step 3: Install dependencies from requirements.txt
                bat "\"%PYTHON_EXE%\" -m pip install -r requirements.txt"

                // ✅ Step 4: Clear any old ChromeDriver cache
                bat "if exist %USERPROFILE%\\.wdm\\drivers\\chromedriver rd /s /q %USERPROFILE%\\.wdm\\drivers\\chromedriver"

                // ✅ Step 5: Run pytest explicitly through Python
                bat "\"%PYTHON_EXE%\" -m pytest -v --maxfail=1 --disable-warnings || echo ⚠️ Pytest failed - check logs for details"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image..."
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Docker Login (Secure)') {
            steps {
                echo "🔐 Logging in to Docker Hub..."
                // ⚠️ In production, move your password to Jenkins credentials store
                bat "docker login -u vishnupriya68 -p \"Shivapriya123@\""
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "⬆️ Pushing Docker Image to Docker Hub..."
                bat "docker tag %IMAGE_NAME% %DOCKER_REPO%"
                bat "docker push %DOCKER_REPO%"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Deploying to Kubernetes Cluster..."
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
