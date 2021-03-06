#!/bin/bash

WAS_HOME=$1
REMOTE_HOST=$2
SOAP_PORT=$3
USERNAME=$4
PASSWORD=$5
MODE=$6
APPLICATION_PATH=$7
APPNAME=$8
PARAMS=$9

$WAS_HOME/bin/wsadmin.sh -lang jython -conntype SOAP \
-host $REMOTE_HOST -port $SOAP_PORT \
-username $USERNAME -password $PASSWORD \
-f ../scripts/deploy.py $MODE $APPLICATION_PATH $APPNAME $PARAMS