# Zoka API

<div align="center">

![Zoka Logo](https://via.placeholder.com/200x200?text=Zoka)

**Open-source data collection platform API**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Project Status](https://img.shields.io/badge/status-early%20development-yellow.svg)]()

[About](#about) • [Features](#features) • [Get Involved](#get-involved) • [Roadmap](#roadmap) • [Community](#community)

</div>

---

## About

**Zoka API** is the backend REST API for the Zoka ecosystem - a modern, open-source data collection platform designed for field surveys, research projects, and data gathering operations.

> **Project Status**: This project is in **early development**. We're currently building the foundation and would love your help! Check out our [roadmap](#roadmap) and [contribution guide](CONTRIBUTING.md) to get involved.

### The Zoka Ecosystem

- **Zoka API** (this repo) - RESTful API backend (In development)
- **Zoka Collect** (coming soon) - Mobile data collection app
- **Zoka Toolbox** (coming soon) - Web-based management platform

### Why Zoka?

- **Open Source**: Fully transparent, community-driven
- **Offline-first**: Collect data anywhere, sync when online
- **Secure**: Built with security best practices from day one
- **Flexible**: Adaptable to various data collection needs
- **Modern Stack**: Built with FastAPI, PostgreSQL, and cutting-edge tools

## Planned Features

### Authentication & Authorization
- [ ] JWT-based authentication with refresh tokens
- [ ] Role-based access control (RBAC)
- [ ] Organization-level isolation
- [ ] Fine-grained permissions

### Data Collection
- [ ] Dynamic form builder with XLSForm support
- [ ] Offline data collection support
- [ ] GPS coordinates capture
- [ ] Media attachments (photos, audio, video)
- [ ] Form versioning and history

### Multi-tenancy
- [ ] Organization management
- [ ] Project-based workflows
- [ ] User assignments and quotas
- [ ] Team collaboration tools

### Synchronization
- [ ] Offline-first architecture
- [ ] Conflict resolution
- [ ] Device sync status tracking
- [ ] Bulk data upload

### Data Management
- [ ] Submission validation workflows
- [ ] Comments and collaboration
- [ ] Audit logging
- [ ] Data export (CSV, XLSX, JSON, SPSS)

### Notifications
- [ ] Real-time alerts
- [ ] Email notifications
- [ ] In-app notifications
- [ ] Customizable triggers

## Get Involved

We're looking for contributors! Whether you're a developer, designer, technical writer, or just passionate about open-source data collection tools, there's a place for you here.

### Ways to Contribute

- **Code**: Help build features (check [good first issues](https://github.com/garboko/zoka-api/labels/good-first-issue))
- **Documentation**: Write guides, improve docs, add examples
- **Testing**: Find bugs, write tests, improve quality
- **Ideas**: Share feature suggestions and use cases
- **Design**: Help with UX/UI for future web/mobile apps
- **Support**: Star the repo, share with others

### Getting Started

Ready to contribute? Here's how:

1. **Read** our [Contributing Guide](CONTRIBUTING.md)
2. **Check** the [Roadmap](#roadmap) to see what we're working on
3. **Look** for [good first issues](https://github.com/garboko/zoka-api/labels/good-first-issue)
4. **Join** the discussion in [GitHub Discussions](https://github.com/garboko/zoka-api/discussions)
5. **Fork** the repo and start coding!

## Tech Stack

### Backend
- **Framework**: FastAPI - Modern, fast web framework
- **Database**: PostgreSQL 15+ - Reliable relational database
- **Cache**: Redis 7+ - For sessions and caching
- **ORM**: SQLAlchemy 2.0 - Powerful Python SQL toolkit
- **Validation**: Pydantic v2 - Data validation using Python type hints
- **Migrations**: Alembic - Database migration tool

### DevOps & Tools
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest - Testing framework
- **Code Quality**: Ruff (linting & formatting), mypy (type checking)
- **CI/CD**: GitHub Actions
- **Task Queue**: Celery (planned)

## Project Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure and setup
- [x] Documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- [x] GitHub templates and workflows
- [ ] Database schema implementation
- [ ] Docker development environment
- [ ] Basic FastAPI setup
- [ ] Database migrations with Alembic

### Phase 2: Core Authentication
- [ ] User model and registration
- [ ] JWT authentication
- [ ] Password hashing and security
- [ ] Login/logout endpoints
- [ ] Refresh token mechanism
- [ ] Basic authorization

### Phase 3: Multi-tenancy & Projects
- [ ] Organization management
- [ ] Project CRUD operations
- [ ] User-project assignments
- [ ] Role-based permissions
- [ ] API documentation (OpenAPI)

### Phase 4: Forms & Data Collection
- [ ] Form builder (XLSForm support)
- [ ] Form versioning
- [ ] Submission endpoints
- [ ] File upload handling
- [ ] GPS data capture

### Phase 5: Advanced Features
- [ ] Offline sync logic
- [ ] Notifications system
- [ ] Comments and collaboration
- [ ] Data export functionality
- [ ] Audit logging

### Phase 6: Mobile Integration
- [ ] Mobile app API optimization
- [ ] Real-time sync improvements
- [ ] Media handling optimization
- [ ] Performance tuning

### Phase 7: Production Ready
- [ ] Comprehensive testing (>80% coverage)
- [ ] Security audit
- [ ] Performance optimization
- [ ] Production deployment guide
- [ ] v1.0 Release

See our [detailed roadmap](https://github.com/garboko/zoka-api/projects) for more information.

## Development Status

### Current Focus
We're currently in **Phase 1: Foundation**. Here's what we're working on:

- Project structure
- Documentation
- Database schema
- Development environment
- API design

### Next Steps
1. Complete database models
2. Setup Docker development environment
3. Implement authentication system
4. Build first API endpoints

## Documentation

### For Contributors
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines
- [Project Structure](docs/ARCHITECTURE.md) - (Coming soon)
- [Database Schema](docs/DATABASE.md) - (Coming soon)

### For Users
- [API Documentation](docs/API.md) - (Coming soon)
- [Installation Guide](docs/INSTALLATION.md) - (Coming soon)
- [Deployment Guide](docs/DEPLOYMENT.md) - (Coming soon)

## Community

### Get in Touch

- **GitHub Issues**: [Report bugs or request features](https://github.com/garboko/zoka-api/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/garboko/zoka-api/discussions)
- **Email**: [contact@zokatoolbox.org](mailto:contact@zokatoolbox.org) (Coming soon)

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

## Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/garboko/zoka-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/garboko/zoka-api?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/garboko/zoka-api?style=social)

</div>

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### Why Apache 2.0?

We chose Apache 2.0 because it:
- Allows commercial use
- Permits modification and distribution
- Provides patent protection
- Requires attribution
- Is widely recognized and trusted

## Acknowledgments

This project is inspired by existing data collection tools and built with modern technologies:

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Powerful ORM
- [ODK](https://getodk.org/) - Open Data Kit inspiration
- [KoBoToolbox](https://www.kobotoolbox.org/) - Data collection inspiration

## Support the Project

If you find Zoka useful, please consider:

- Starring the repository
- Reporting bugs
- Suggesting features
- Sharing with others
- Contributing code
- Improving documentation

## Vision

Our vision is to create a **free, open-source alternative** to commercial data collection platforms that:

- Empowers researchers and organizations in low-resource settings
- Provides enterprise-grade features without the enterprise price tag
- Prioritizes user privacy and data sovereignty
- Supports offline-first workflows for field work
- Builds a strong, supportive community

## Quick Links

- [Report a Bug](https://github.com/garboko/zoka-api/issues/new?template=bug_report.md)
- [Request a Feature](https://github.com/garboko/zoka-api/issues/new?template=feature_request.md)
- [Ask a Question](https://github.com/garboko/zoka-api/issues/new?template=question.md)
- [View Roadmap](https://github.com/garboko/zoka-api/projects)
- [Join Discussion](https://github.com/garboko/zoka-api/discussions)

---

<div align="center">

**[Back to top](#zoka-api)**

Made with by the Zoka community

*Let's build something amazing together!*

</div>