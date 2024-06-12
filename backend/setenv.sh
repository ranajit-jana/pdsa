#!/bin/bash

# Prompt the user for input
read -p "Enter Database User: " DATABASE_USER
read -sp "Enter Database Password: " DATABASE_PASSWORD
echo
read -p "Enter Database Host: " DATABASE_HOST
read -p "Enter Database Name: " DATABASE_NAME

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    touch .env
fi

# Update or add variables in the .env file
sed -i "/^DATABASE_USER=/d" .env
sed -i "/^DATABASE_PASSWORD=/d" .env
sed -i "/^DATABASE_HOST=/d" .env
sed -i "/^DATABASE_NAME=/d" .env

echo "DATABASE_USER=$DATABASE_USER" >> .env
echo "DATABASE_PASSWORD=$DATABASE_PASSWORD" >> .env
echo "DATABASE_HOST=$DATABASE_HOST" >> .env
echo "DATABASE_NAME=$DATABASE_NAME" >> .env

echo ".env file updated successfully."