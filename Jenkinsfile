pipeline {
  agent {
    node {
      label 'python'
    }
  }
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
      stage('Deploy Uploader JSON') {
        when {
          branch 'master'
          not {
            changeRequest()
          }
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./uploader* sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/core/'
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./uploader* sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/'
        }
      }
      stage('Deploy Egg') {
        when {
          branch 'master'
          not {
            changeRequest()
          }
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./insights-core.egg* sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/core/'
       }
     }
   }
 }
