# Database Schema (Production Vision)

Production instances move away from Streamlit `session_state` and store complex relational data into isolated PostgreSQL clusters (like Supabase).

## Entities

1. **Users** (*roles: HR_ADMIN, INTERVIEWER, PLACEMENT_CELL*)
2. **Organizations** (*multi-tenant groupings for different recruitment agencies/companies*)
3. **Drives** (*instances pointing to specific colleges/events*)
4. **Roles** (*job descriptions and filtering configurations assigned to a Drive*)
5. **Candidates** (*structured parse outputs + normalized PIVs*)
6. **ScreeningResults** (*dimension scores tied to a candidate and role*)
7. **Shortlists** (*audit trails marking tier switches by Users*)
8. **Communications** (*generated textual logs of correspondence with the Candidate*)
9. **AuditLog** (*history events detailing modifications at each boundary state transition or interrupt resolution*)

The database implements flexible `JSONB` for storing nested lists like extracted arrays of Projects or Internships.
