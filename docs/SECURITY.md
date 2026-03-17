# Security Architecture

1. **Blind Screening**: Candidates' personally identifiable information (Name, Gender, Contact) should be masked during the LLM's Stage B processing to minimize subconscious bias and enforce merit-only evaluation based purely on extracted education/skills components.
2. **File Handling**: Uploaded PDFs/DOCXs are parsed in sandboxed environments without execution capabilities. Signed URLs with strict expiry dictating S3 accesses ensure placement data is volatile and secure.
3. **Data Protection**: Streamlit Secrets or secure Vaults must be rigorously used to store LLM keys and Database connection URLS.
