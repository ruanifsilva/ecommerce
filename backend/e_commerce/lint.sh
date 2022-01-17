#!/bin/bash

echo "organizando os imports"
isort .

echo "organizando o código"
black .