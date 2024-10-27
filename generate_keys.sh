#!/bin/bash
openssl ecparam -genkey -name secp384r1 -out ec.key
chmod 600 ec.key
openssl ec -in ec.key -pubout -out ec-pub.key