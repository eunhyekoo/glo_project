import groovy.json.JsonOutput
@Library('devops-library') _
def gitInfo = ""
def message = null

node { 
    try {
        stage('Clone devops & build repository') {
            sh 'echo "Current user: $(whoami)"'
            sh 'echo "Current directory: $(pwd)"'

            // Checkout Tool Repository
            script{
                gitInfo = checkout scm
            }
        }

        stage('Environment settings for build') {
			//set build number into deploy.yaml
			sh 'sed -i \'s/SET_BUILD_NUMBER/'+"${env.BUILD_NUMBER}"+'/g\' ./gloz-logstash/logstash.deploy.yaml'
        }

        stage('Build docker image & Push image') {
            dir('./gloz-logstash') {
                // DockerBuild Command
                sh 'docker-compose -f ./logstash.docker-compose.yaml build logstash'

                // Login AWS ECR
                sh 'aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 740016600163.dkr.ecr.ap-northeast-2.amazonaws.com'

                // Push Docker image
                sh 'docker-compose -f ./logstash.docker-compose.yaml push logstash'

                // Add build number to ECR
                sh 'aws ecr put-image --repository-name glocalize-dev/logstash --image-tag '+"${env.BUILD_NUMBER}"+' --image-manifest \"$(aws ecr batch-get-image --repository-name glocalize-dev/logstash --image-ids imageTag=latest --query \'images[].imageManifest\' --output text)"'
            }
        }

        stage('Deploy to EKS') {
            sh 'python3 ./kubeAPI/kubeDeleteDeployment.py ${CLUSTER} es gloz-logstash'
            sh 'python3 ./kubeAPI/kubeDeployDeployment.py ${CLUSTER} ./gloz-logstash/logstash.deploy.yaml'
        }

    } catch (Exception e) { 
        currentBuild.result = 'FAILURE'
        println("exception: "+e)
      
    } finally {
        cleanUpDocker()
        echo "Build Status : ${currentBuild.result}"

		if (currentBuild.result != 'FAILURE') {
			setElasticsearch(gitInfo)
		}
    }
}

def cleanUpDocker() {
    //Not Used. for Build Performance
    //sh 'echo "Cleaning up docker containers and images"'
    //sh 'docker image prune -a'
    sh 'echo "Remove exited containers"'
    sh 'docker ps --filter status=dead --filter status=exited -aq | xargs -r docker rm -v'
}
