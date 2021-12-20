properties([pipelineTriggers([githubPush()])])

pipeline {
    agent none
    stages {
        /* checkout repo */
        stage('Checkout SCM') {
            agent any
            steps {
                script{
                    def scmVars = checkout([
                     $class: 'GitSCM',
                     branches: [[name: 'main']],
                     userRemoteConfigs: [[
                        url: 'https://github.com/EliranKasif/CloudSchool-PythonRestApi',
                        credentialsId: '',
                     ]]
                    ])
                    env.GIT_COMMIT = scmVars.GIT_COMMIT
                }
            }
        }
    stage('Test') {
        agent any
      steps {
        sh 'apt-get update'
        sh 'apt install -y python3'
        sh 'python3 test_app.py'
        //input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
      }
    }
    stage('updatesConsulKey')
    {
    agent any
      steps {
        echo "updates consul key with new version"
        sh "curl \
    --request PUT \
    --data ${env.GIT_COMMIT} \
    main.services:8500/v1/kv/app/version/APPLICATION_VERSION"
      }
    }

    }
}