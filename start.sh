#!/bin/bash

mkdir -p /app/output
mkdir -p /app/voices

uvicorn main:app --host 0.0.0.0 --port 8000