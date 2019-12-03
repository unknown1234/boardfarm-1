def extra_args = env.extra_args ?: ''
def email_results = env.email_results ?: ''
def GERRIT_BRANCH = env.GERRIT_BRANCH ?: 'master'
def GERRIT_PROJECT = env.GERRIT_PROJECT ?: ''
def GERRIT_REFSPEC = env.GERRIT_REFSPEC ?: ''

def meta = env.meta ?: ''
if (meta != '') {
    meta_args = " -m " + meta
} else {
    meta_args = ""
}

def sync_code () {
    sshagent ( [ ssh_auth ] ) {
        script {
            sh "rm -rf *"
            sh "repo init -u " + manifest + " && repo sync --force-remove-dirty"
            sh "repo forall -c 'git checkout gerrit/$GERRIT_BRANCH'"
            if (GERRIT_REFSPEC != '') {
                sh "repo forall -r ^$GERRIT_PROJECT\$ -c 'pwd && git fetch gerrit $GERRIT_REFSPEC && git checkout FETCH_HEAD && git rebase gerrit/$GERRIT_BRANCH'"
            }
            sh "repo manifest -r"
        }
    }
}

def run_lint () {
    sh '''
    set +e
    pwd
    ls
    rm -f errors.txt
    touch errors.txt
    repo forall -c 'git diff --name-only HEAD m/master | sed s,^,$REPO_PATH/,g' > files_changed.txt
    echo "Running pyflakes on py files and ignoring init files:"
    files_changed=`cat files_changed.txt | grep .py | grep -v __init`
    if [ -z "$files_changed" ]; then
      exit 0
    fi
    # Check pyflakes errors
    python2 -m pyflakes ${files_changed} > flakes.txt 2>&1
    cat flakes.txt | grep -v 'devices\\.' | grep -v 'No such file' > errors.txt
    # Check print errors
    grep -n -E '^\\s+print\\s' ${files_changed} | awk '{print $1" print should be function: print()"}' >> errors.txt
    # Check indentation errors
    flake8 --select=E111 ${files_changed} >> errors.txt
    '''
}

def run_test () {
    ansiColor('xterm') {
        sh '''
        pwd
        ls
        rm -rf venv
        virtualenv venv
        . venv/bin/activate
        repo forall -c '[ -e "requirements.txt" ] && { pip install -r requirements.txt || echo failed; } || true '
        repo forall -c '[ -e "setup.py" ] && { pip install -e . || echo failed; } || true '
        python --version
        bft --version
        export BFT_CONFIG=''' + config + '''
        ${WORKSPACE}/boardfarm/scripts/whatchanged.py --debug m/master HEAD
        export changes_args="`${WORKSPACE}/boardfarm/scripts/whatchanged.py m/master HEAD`"
        if [ "$BFT_DEBUG" != "y" ]; then unset BFT_DEBUG; fi
        cd boardfarm
        yes | ./bft -b ''' + board + ''' -x ''' + testsuite + ''' ${changes_args}''' + extra_args + meta_args

        sh 'grep tests_fail...0, boardfarm/results/test_results.json'
    }
}

pipeline {
    agent { label 'boardfarm && ' + location }


    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('checkout gerrit change') {

            steps {
                sync_code()
            }
        }

        stage('run linting') {
            steps {
                run_lint()
            }
        }

        stage('run bft test') {
            steps {
                run_test()
            }
        }
        stage('post results to gerrit') {
            steps {
                sh '''#!/bin/bash
                cat boardfarm/results/test_results.json | jq '.test_results[] | [ .grade, .name, .message, .elapsed_time ] | @tsv' | \
                sed -e 's/"//g' -e 's/\\t/    /g' | \
                while read -r line; do
                echo $line >> message
                done
                '''
            }
        }
    }
    post {
        always {
            emailext body: '''${FILE, path="boardfarm/results/results.html"}''',
                 mimeType: 'text/html',
                 subject: "[Jenkins] ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                 recipientProviders: [[$class: 'RequesterRecipientProvider']],
                 to: email_results
            archiveArtifacts artifacts: '*.txt,boardfarm/results/*'
            sh 'rm -rf boardfarm/results'
            sh '''
            set +xe
            echo "Killing spawned processes..."
            PID_SELF=$$
            for PID in $(ps -eo pid,command -u ${USER} | grep -v grep | tail -n+2 | awk '{print $1}' | grep -v ${PID_SELF} | grep -v ${PPID}); do
                echo "Checking pid ${PID}"
                if xargs -0 -L1 -a /proc/${PID}/environ 2>/dev/null | grep "BUILD_ID=${BUILD_ID}$"; then
                    echo "Killing $(ps -p ${PID} | tail -1 | awk '{print $1}')"
                    sed -z 's/$/ /' /proc/$PID/cmdline; echo
                    kill ${PID}
                    echo killed ${PID}
                fi
            done || true
            '''
        }
    }
}
