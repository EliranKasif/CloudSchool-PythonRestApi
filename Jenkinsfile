pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'echo "building the repo"'
          }
        }
      }
    }
  
    stage('Test') {
      steps {
        sh 'python3 test_app.py'
        //input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
      }
    }
  
    stage('updatesConsulKey')
    {
      steps {
          contents = env.GIT_COMMIT

        echo "updates consul key with new version"
        sh "curl \
    --request PUT \
    --data @${contents} \
    http://main.services:8500/v1/kv/app/version/APPLICATION_VERSION"
      }
    }
  }
  
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}