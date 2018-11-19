# gosa-sieve-vacancies

Gosa Sieve Vacancies

Simple python script used to create vacation rules for sieve out of 
ldap settings. It is meant to run repeatedly by cron job. 
The script pulls data that is managed by gosa but should be easy 
to adjust config files to use any other scheme.

## How it works

…

## Install & Setup: 

Make sure sieve and the sieve vacation plugin is installed and working 

Installing the debian package. 

    wget https://github.com/upsource/gosa-sieve-vacancies/blob/master/bin/gosa-sieve-vacancies_0.1.10_amd64.deb
    dpkg -i gosa-sieve-vacancies_0.1.10_amd64.deb

    # setup your ldap settings & sieve user directories
    /etc/gosa-sieve-vacancies/sync-vacancies.conf.json
    
    # setup the template file that is used to generate sieve vacation rules
    /etc/gosa-sieve-vacancies/sieve-template.tpl
    
    # review the integration in dovecot
    /etc/dovecot/conf.d/91-vacation-sieve.conf 

## Testing and Debuging 


Invoke the skript manually in dry-run mode to see what would be done

    python /opt/bin/sync-vacancies.py -d
    
Use the verbose and extra-verbose mode to get info what is happening  

    python /opt/bin/sync-vacancies.py -v 
    python /opt/bin/sync-vacancies.py -ev
    
This can also be used in conjunction with dry-run flag


## Files 

#### `/etc/gosa-sieve-vacancies/sync-vacancies.conf.json`

Holds the configuration for the ldpa client


#### `/etc/gosa-sieve-vacancies/sieve-template.tpl`

The sieve template that will be used to generate the sieve vacation script
on a per user base. The system uses pythons format() syntax as template base. Thus one must use double 
{ to get them escaped properly.
Within the template it is possible to access the LDAP User result. 
By simply adressing configured attributes like `{gosaVacationStart}`
To get dates in proper format the script provides
`gosaVacationStartDate` and `gosaVacationStopDate` property which contains the timestamp formated as YYYY-MM-DD

Invoke the script with -ev option to see the available information. 

e.g.
       
    # escaped braclets
    ${{1}} 
    # will result in 
    ${1}
