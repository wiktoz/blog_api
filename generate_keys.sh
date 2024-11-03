#!/bin/sh

openssl ecparam -genkey -name secp384r1 -out /blog_api/ec.key
chmod 600 /blog_api/ec.key
openssl ec -in /blog_api/ec.key -pubout -out /blog_api/ec-pub.key
