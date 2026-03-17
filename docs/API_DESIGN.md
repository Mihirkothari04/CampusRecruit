# API Design

Production API mappings for a frontend-backend split.

```
POST /drives                          → create drive
POST /drives/:id/upload               → bulk upload
POST /drives/:id/parse                → trigger parsing (async)
POST /drives/:id/screen               → trigger screening (async)
GET  /drives/:id/shortlist            → current shortlist
PATCH /shortlist/:id                  → override tier
POST /drives/:id/shortlist/approve    → bulk approve
POST /drives/:id/briefs/generate      → trigger briefs
POST /drives/:id/communications       → generate drafts
```
