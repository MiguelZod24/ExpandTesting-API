pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub'
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                echo 'Instalando Python y dependencias'
                sh '''
                    apt-get update -q || true
                    apt-get install -y python3 python3-pip -q || true
                    pip3 install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('Ejecutar tests') {
            steps {
                echo 'Ejecutando tests con Pytest'
                sh 'python3 -m pytest --tb=short'
            }
        }

    }
}
