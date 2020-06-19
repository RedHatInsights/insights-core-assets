pipeline {
  options {
    disableConcurrentBuilds()
  }
  agent {
    node {
      label 'python27'
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
             withCredentials(bindings: [sshUserPrivateKey(credentialsId: "cloud-netstorage",
                                                          keyFileVariable: "privateKeyFile")]) {
                  configFileProvider([configFile(fileId: "9f0c91bc-4feb-4076-9f3e-13da94ff3cef", variable: "AKAMAI_HOST_KEY")]) {
                          sh """
                            eval `ssh-agent`
                            ssh-add \"$privateKeyFile\"
                            cp $AKAMAI_HOST_KEY ~/.ssh/known_hosts
                            chmod 600 ~/.ssh/known_hosts
                            rsync -arv -e \"ssh -2\" ./uploader* sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/
                            """
                  }
             }
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
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./changelog.txt sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/core/'
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./insights-core.egg* sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/release/'
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./changelog.txt sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/release/'
             withCredentials(bindings: [sshUserPrivateKey(credentialsId: "cloud-netstorage",
                                                          keyFileVariable: "privateKeyFile")]) {
                  configFileProvider([configFile(fileId: "9f0c91bc-4feb-4076-9f3e-13da94ff3cef", variable: "AKAMAI_HOST_KEY")]) {
                          sh """
                            eval `ssh-agent`
                            ssh-add \"$privateKeyFile\"
                            cp $AKAMAI_HOST_KEY ~/.ssh/known_hosts
                            chmod 600 ~/.ssh/known_hosts
                            rsync -arv -e \"ssh -2\" ./insights-core.egg* sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/
                            rsync -arv -e \"ssh -2\" ./changelog.txt sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/
                            rsync -arv -e \"ssh -2\" ./insights-core.egg* sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/release/
                            rsync -arv -e \"ssh -2\" ./changelog.txt sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/release/
                            """
                  }
             }
        }
      }
      stage('Deploy Egg to Pre-Prod') {
        when {
          branch 'pre_prod'
          not {
            changeRequest()
          }
        }
        steps {
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./insights-core.egg* sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/testing/'
             sh 'rsync -arv -e "ssh -i /tmp/akamai-ssh -o StrictHostKeyChecking=no" ./changelog.txt sshacs@unprotected.upload.akamai.com:/114034/r/insights/v1/static/testing/'
             withCredentials(bindings: [sshUserPrivateKey(credentialsId: "cloud-netstorage",
                                                          keyFileVariable: "privateKeyFile")]) {
                  configFileProvider([configFile(fileId: "9f0c91bc-4feb-4076-9f3e-13da94ff3cef", variable: "AKAMAI_HOST_KEY")]) {
                          sh """
                            eval `ssh-agent`
                            ssh-add \"$privateKeyFile\"
                            mkdir ~/.ssh
                            chmod 700 ~/.ssh
                            cp $AKAMAI_HOST_KEY ~/.ssh/known_hosts
                            chmod 600 ~/.ssh/known_hosts
                            rsync -arv -e \"ssh -2\" ./insights-core.egg* sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/testing
                            rsync -arv -e \"ssh -2\" ./changelog.txt sshacs@cloud-unprotected.upload.akamai.com:/822386/api/v1/static/testing
                            """
                  }
             }
        }
      }
  }
}

