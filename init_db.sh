#!/bin/bash
/usr/bin/mysqld_safe --skip-grant-tables &
sleep 5
mysql -u root -e "CREATE DATABASE BrainTrain"
mysql -u root BrainTrain < /tmp/BrainTrain_Border.sql
mysql -u root BrainTrain < /tmp/BrainTrain_Champion.sql

