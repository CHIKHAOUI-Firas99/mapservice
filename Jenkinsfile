pipeline {
  agent any 
  stages {

      
stage('Build new image') {
	steps{
        //withDockerServer([uri: 'unix:///var/run/docker.sock']) {
	sh "docker build -t firaschikhaoui/test-back2:latest ."    	         
            }
         }

stage('Push new image') {
	steps{
	withDockerRegistry([credentialsId: "docker-credentials", url: ""]) {
  	sh "docker push firaschikhaoui/test-back2:latest"
	}
	}
	}
      
  
  }
      
  }
