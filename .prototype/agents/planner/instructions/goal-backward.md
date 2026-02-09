## Goal-Backward Methodology

**Forward planning:** "What should we build?" → produces tasks.
**Goal-backward:** "What must be TRUE for the goal to be achieved?" → produces requirements tasks must satisfy.

## The Process

**Step 1: State the Goal**
Take phase goal from ROADMAP.md. Must be outcome-shaped, not task-shaped.

- Good: "Working chat interface" (outcome)
- Bad: "Build chat components" (task)

**Step 2: Derive Observable Truths**
"What must be TRUE for this goal to be achieved?" List 3-7 truths from USER's perspective.

For "working chat interface":

- User can see existing messages
- User can type a new message
- User can send the message
- Sent message appears in the list
- Messages persist across page refresh

**Test:** Each truth verifiable by a human using the application.

**Step 3: Derive Required Artifacts**
For each truth: "What must EXIST for this to be true?"

"User can see existing messages" requires:

- Message list component (renders Message[])
- Messages state (loaded from somewhere)
- API route or data source (provides messages)
- Message type definition (shapes the data)

**Test:** Each artifact = a specific file or database object.

**Step 4: Derive Required Wiring**
For each artifact: "What must be CONNECTED for this to function?"

Message list component wiring:

- Imports Message type (not using `any`)
- Receives messages prop or fetches from API
- Maps over messages to render (not hardcoded)
- Handles empty state (not just crashes)

**Step 5: Identify Key Links**
"Where is this most likely to break?" Key links = critical connections where breakage causes cascading failures.

For chat interface:

- Input onSubmit -> API call (if broken: typing works but sending doesn't)
- API save -> database (if broken: appears to send but doesn't persist)
- Component -> real data (if broken: shows placeholder, not messages)
