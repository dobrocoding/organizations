#!/bin/bash

# Create test buckets
awslocal s3 mb s3://test-bucket

# Setup test email
awslocal ses verify-email-identity --email-address sender@example.com --region us-east-1
