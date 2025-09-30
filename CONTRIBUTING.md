# Contributing to Zoka API

First off, thank you for considering contributing to Zoka API! 

It's people like you that make Zoka API such a great tool. We welcome contributions from everyone, whether you're fixing a typo, adding documentation, reporting a bug, or implementing a new feature.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [INSERT EMAIL].

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)
- Git

### First Contribution?

If this is your first time contributing to open source, welcome! Here are some resources to help you get started:

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Timers Only](https://www.firsttimersonly.com/)
- [GitHub's Guide to Contributing](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)

Look for issues labeled `good-first-issue` or `help-wanted` to get started!

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the [existing issues](https://github.com/garboko/zoka-api/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs what actually happened
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Docker version)
- **Relevant logs** or error messages

Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

### Suggesting Features

We love feature suggestions! Before submitting:

- Check if the feature has already been suggested
- Make sure it aligns with the project's goals
- Provide a clear use case and rationale

Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

### Improving Documentation

Documentation improvements are always welcome! This includes:

- Fixing typos or grammar
- Adding examples
- Clarifying confusing sections
- Writing tutorials or guides
- Improving API documentation

### Writing Code

Ready to write some code? Great! Here's how:

1. **Find or create an issue** describing what you want to work on
2. **Comment on the issue** to let others know you're working on it
3. **Fork the repository** and create a branch
4. **Write your code** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Setup

### Using Docker (Recommended)
```bash
# 1. Clone your fork
git clone https://github.com/garboko/zoka-api.git
cd zoka-api

# 2. Copy environment variables
cp .env.example .env

# 3. Start services
docker-compose -f docker-compose.dev.yml up

# 4. API will be available at http://localhost:8000
# 5. API docs at http://localhost:8000/docs