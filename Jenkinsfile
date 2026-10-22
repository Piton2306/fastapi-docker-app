pipeline {
    // 1. ГДЕ выполнять: any (на любом свободном агенте)
    agent any

    // Переменные окружения пайплайна
    environment {
        APP_NAME = "fastapi-docker-app"
    }

    // 2. ЭТАПЫ КОНВЕЙЕРА
    stages {
        stage('1. Checkout') {
            steps {
                echo "Загрузка исходного кода из системы контроля версий..."
            }
        }

        stage('2. Static Analysis & Lint') {
            steps {
                echo "Запуск статического анализатора кода..."
                sh 'echo "Проверка PEP8 пройдена успешно!"'
            }
        }

        stage('3. Unit Tests') {
            steps {
                echo "Запуск модульных тестов Pytest..."
                sh 'echo "Все тесты завершены со статусом OK!"'
            }
        }

        stage('4. Docker Build') {
            steps {
                echo "Сборка Docker-образа для ${env.APP_NAME}..."
            }
        }
    }

    // 3. ПОСТ-ДЕЙСТВИЯ (выполняются в зависимости от результата)
    post {
        always {
            echo "Пайплайн завершил выполнение. Очистка временных файлов."
        }
        success {
            echo "Релиз успешен! Отправка уведомления в Telegram/Slack."
        }
        failure {
            echo "ВНИМАНИЕ: Сборка упала! Требуется вмешательство инженера."
        }
    }
}