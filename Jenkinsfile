pipeline {
  agent {
    node {
      label 'python'
    }
  }
  if (env.CHANGE_ID == null) {
    stages {
      stage('Write SSH Key') {
        steps {
             writeFile file: "/tmp/akamai-ssh", text: "${env.AKAMAI_SSH_KEY}\n-----END RSA PRIVATE KEY-----"
             sh 'chmod 600 /tmp/akamai-ssh'
        }
      }    
      stage('Check GPG') {
        steps {
          sh """
             gpg --no-default-keyring --keyring ./redhattools.pub.gpg --verify uploader.v2.json.asc uploader.v2.json
             gpg --no-default-keyring --keyring ./redhattools.pub.gpg --verify uploader.json.asc uploader.json
             gpg --no-default-keyring --keyring ./redhattools.pub.gpg --verify insights-core.egg.asc insights-core.egg
          """
        }
      }
      stage('Deploy Insights') {
        when {
          branch 'master'
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh" * sshacs@unprotected.upload.akamai.com:/114034/insights/static/core/'
        }
      }
      stage('Deploy Insights Beta') {
        when {
          branch 'master'
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh" * sshacs@unprotected.upload.akamai.com:/114034/insightsbeta/static/core/'
        }
      }
      stage('Deploy Insights Alpha') {
        when {
          branch 'master'
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh" * sshacs@unprotected.upload.akamai.com:/114034/insightsalpha/static/core/' 
        }
      }
      stage('Deploy Legacy API') {
        when {
          branch 'master'
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh" * sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/core/'
        }
      }
    }
  }
}
