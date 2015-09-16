Timeline Gallery in Openshift
======================

This is python web application running in Openshift by Redhat.

It's using flask as web framework, sqlalchemy as ORM to MySQL, jQuery and other javascript libraries.

Demo
======================

http://tintin.zfdang.com/


Deloy Instruction to OpenShift
======================

This git repository helps you get up and running quickly with a Timeline Gallery installation on OpenShift. The backend database is MySQL and the database name is the same as your application name (using $_ENV['OPENSHIFT_APP_NAME']).


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a python application (you can call your application whatever you want, 'gallery' here as an example)

    rhc app create -a gallery -t python-2.6

Add MySQL support to your application

    rhc cartridge add -a gallery -c mysql-5.1

Add this upstream "Timeline Gallery" repo

    cd gallery 
    git remote add upstream -m master git://github.com/zfdang/timeline-gallery-in-openshift.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now init your application at:

    http://gallery-$yournamespace.rhcloud.com/admin/init
    
Default Credentials
-------------------
<table>
<tr><td>Default Admin Username</td><td>admin</td></tr>
<tr><td>Default Admin Password</td><td>Password2012</td></tr>
</table>
