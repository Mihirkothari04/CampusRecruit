# Scaling Strategy

## Bottlenecks
1. **Resume Parsing Compute:** PyMuPDF running synchronously on hundreds of resumes blocks the event loop.
2. **LLM API Limits:** Deep evaluations are prone to hitting rate limits if parallelized unsafely.

## Resolution
1. **Event-driven Async Processing:** Move parsing and AI screening to backend workers (Celery/Redis or serverless functions like AWS Lambda).
2. **Optimistic Locking:** Shortlist adjustments from concurrent members (multiple HR users) must utilize versioning and optimistic locking to prevent overwriting.
3. **Caching & DB Pooling:** Use PgBouncer and Memcached for faster reads during interview day when panel members simultaneously fetch briefs.
