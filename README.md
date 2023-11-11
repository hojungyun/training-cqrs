# Overview

This repository contains a simple and illustrative codebase showcasing the implementation of Command Query Responsibility Segregation (CQRS) with Event Sourcing.

# Getting Started

#### 1. Download the codebase and install packages
```
git clone https://github.com/hojungyun/training-cqrs.git
cd training-cqrs
poetry install
```

#### 2. Start NOSQL and MQ containers from terminal 1
```
cd training-cqrs
docker-compose up --build
```

#### 3. Start app for command from terminal 2
```
cd training-cqrs
poetry shell
uvicorn app_command.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Start app for query from terminal 3
```
cd training-cqrs
poetry shell
uvicorn app_query.main:app --reload --host 0.0.0.0 --port 8001
```

#### 5. Start listener to create product in NOSQL from terminal 4
```
cd training-cqrs
poetry shell
python event_bus/listener.py
```

# Test

#### 1. Create product from:
http://localhost:8000/docs

#### 2. Verify the product created by worker from:
http://localhost:8001/docs
