## Task Anatomy

Every task has four required fields:

**<files>:** Exact file paths created or modified.

- Good: `src/app/api/auth/login/route.ts`, `prisma/schema.prisma`
- Bad: "the auth files", "relevant components"

**<action>:** Specific implementation instructions, including what to avoid and WHY.

- Good: "Create POST endpoint accepting {email, password}, validates using bcrypt against User table, returns JWT in httpOnly cookie with 15-min expiry. Use jose library (not jsonwebtoken - CommonJS issues with Edge runtime)."
- Bad: "Add authentication", "Make login work"

**<verify>:** How to prove the task is complete.

- Good: `npm test` passes, `curl -X POST /api/auth/login` returns 200 with Set-Cookie header
- Bad: "It works", "Looks good"

**<done>:** Acceptance criteria - measurable state of completion.

- Good: "Valid credentials return 200 + JWT cookie, invalid credentials return 401"
- Bad: "Authentication is complete"

## Task Types

| Type                      | Use For                                | Autonomy         |
| ------------------------- | -------------------------------------- | ---------------- |
| `auto`                    | Everything Claude can do independently | Fully autonomous |
| `checkpoint:human-verify` | Visual/functional verification         | Pauses for user  |
| `checkpoint:decision`     | Implementation choices                 | Pauses for user  |
| `checkpoint:human-action` | Truly unavoidable manual steps (rare)  | Pauses for user  |

**Automation-first rule:** If Claude CAN do it via CLI/API, Claude MUST do it. Checkpoints verify AFTER automation, not replace it.

## Task Sizing

Each task: **15-60 minutes** Claude execution time.

| Duration  | Action                                |
| --------- | ------------------------------------- |
| < 15 min  | Too small — combine with related task |
| 15-60 min | Right size                            |
| > 60 min  | Too large — split                     |

**Too large signals:** Touches >3-5 files, multiple distinct chunks, action section >1 paragraph.

**Combine signals:** One task sets up for the next, separate tasks touch same file, neither meaningful alone.

## Specificity Examples

| TOO VAGUE             | JUST RIGHT                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| "Add authentication"  | "Add JWT auth with refresh rotation using jose library, store in httpOnly cookie, 15min access / 7day refresh"                        |
| "Create the API"      | "Create POST /api/projects endpoint accepting {name, description}, validates name length 3-50 chars, returns 201 with project object" |
| "Style the dashboard" | "Add Tailwind classes to Dashboard.tsx: grid layout (3 cols on lg, 1 on mobile), card shadows, hover states on action buttons"        |
| "Handle errors"       | "Wrap API calls in try/catch, return {error: string} on 4xx/5xx, show toast via sonner on client"                                     |

**Test:** Could a different Claude instance execute without asking clarifying questions? If not, add specificity.
