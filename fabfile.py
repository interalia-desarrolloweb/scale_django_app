from fabric.api import *
PATH ="/export/web/scaledjago.stg.interalia.net/scale_django_app/"

@task
@hosts("andres.vargas@10.0.0.2")
def deploy():
    with cd(PATH):
        run("git pull && git reset --hard HEAD ")
        run("make html")
        
