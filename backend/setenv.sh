#!/bin/bash

# Prompt the user for input
read -p "Enter Database User: " DB_USERNAME
read -sp "Enter Database Password: " DB_PASSWORD
echo
read -p "Enter Database Host: " DB_HOSTNAME
read -p "Enter Database Name: " DB_NAME

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    touch .env
fi

# Update or add variables in the .env file
sed -i "/^DB_USERNAME=/d" .env
sed -i "/^DB_PASSWORD=/d" .env
sed -i "/^DB_HOSTNAME=/d" .env
sed -i "/^DB_NAME=/d" .env

echo "DB_USERNAME=$DB_USERNAME" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env
echo "DB_HOSTNAME=$DB_HOSTNAME" >> .env
echo "DB_NAME=$DB_NAME" >> .env

echo ".env file updated successfully."
