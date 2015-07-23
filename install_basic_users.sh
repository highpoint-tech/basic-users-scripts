#!/bin/bash

echo ""
echo "Installing Basic User software"
echo ""

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -z "$BASIC_USERS_API_ID" ]
	then echo "Basic users API ID is not in environment variables."
	exit
fi

if [ -z "$BASIC_USERS_API_KEY" ]
	then echo "Basic users API key is not in environment variables."
	exit
fi

DESTINATION="/opt/basic-users"
BRANCH="master"


mkdir -p ${DESTINATION}
cd ${DESTINATION} && curl -L https://github.com/hp-mobile/basic-users-scripts/tarball/${BRANCH} -o ${BRANCH}.tar.gz
cd ${DESTINATION} && tar xzvf ${BRANCH}.tar.gz --strip-components=1
rm ${DESTINATION}/${BRANCH}.tar.gz


cat ${DESTINATION}/config.ini | sed -e "s/id =/id = ${BASIC_USERS_API_ID}/" > ${DESTINATION}/config_temp.ini
mv ${DESTINATION}/config_temp.ini ${DESTINATION}/config.ini

cat ${DESTINATION}/config.ini | sed -e "s/key =/key = ${BASIC_USERS_API_KEY}/" > ${DESTINATION}/config_temp.ini
mv ${DESTINATION}/config_temp.ini ${DESTINATION}/config.ini


mv ${DESTINATION}/basic-users-upstart.conf /etc/init/basic-users-upstart.conf
start basic-users-upstart


echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
