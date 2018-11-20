
echo "setup access rights for cron"
chown root:root /etc/cron.d/gosa-sieve-vacancies
chmod 644 /etc/cron.d/gosa-sieve-vacancies

echo "setup access rights for config files"
chmod 600 /etc/gosa-sieve-vacancies/sync-vacancies.conf.json

