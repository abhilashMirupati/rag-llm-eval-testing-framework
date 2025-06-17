pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        VIRTUAL_ENV = "${WORKSPACE}/venv"
        PATH = "${VIRTUAL_ENV}/bin:${env.PATH}"
    }
    
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 . --output-file=flake8-report.txt
                    pylint --output-format=parseable **/*.py > pylint-report.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml --cov=. --cov-report=html
                '''
            }
        }
    }
    
    post {
        always {
            junit '**/test-results.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            archiveArtifacts artifacts: 'flake8-report.txt'
            archiveArtifacts artifacts: 'pylint-report.txt'
        }
    }
} 