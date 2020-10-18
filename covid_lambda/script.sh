#!/bin/bash

# S3 bucket name for SAM to store the packaged output template.
BUCKET=covid-project-testing

# Directory to store the build artifacts
rm -rf build
mkdir build

# Generate cloudformation template out of SAM template.
aws cloudformation package                        \
	--template-file template.yaml             \
        --output-template-file build/output.yaml  \
        --s3-bucket $BUCKET

# Deploy the output cloudformation template
aws cloudformation deploy                         \
	--template-file ./build/output.yaml       \
	--stack-name  Covid-project	          \
        --capabilities CAPABILITY_NAMED_IAM 
