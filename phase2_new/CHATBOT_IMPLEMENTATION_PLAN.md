# SalaatFlow Chatbot - Complete Implementation Plan

## Executive Summary
Yeh document clearly define karta hai ke SalaatFlow chatbot ko kis tarah implement karna hai, with exact specifications aur step-by-step guide.

---

## Current Status (2025-12-30)

### ✅ Completed
1. **Google Gemini API Integration** - FREE API working
2. **Backend Server** - Running on port 8000
3. **Database** - Seeded with sample data
4. **Basic Intent Detection** - Regex-based pattern matching
5. **Task Creation** - via natural language
6. **Task Listing** - formatted output
7. **Masjid Search** - by area name

### ⏳ In Progress
1. Task update functionality
2. Task deletion
3. Better error handling

### ❌ Pending
1. Hadith integration
2. Context/conversation memory
3. Natural language improvements
4. Analytics & logging

---

## Chatbot Architecture

```
User Message
     ↓
[Language Detection] → Urdu/English
     ↓
[Intent Detection] → create_task | list_tasks | search_masjid | conversation
     ↓
[Parameter Extraction] → title, prayer, priority, time, area
     ↓
[Tool Execution] → Direct API calls
     ↓
[Response Formatting] → Pretty output with emojis
     ↓
User Response
```

---

## Detailed Feature Specifications

### 1. Task Creation

#### Input Examples:
```
"Fajr ki namaz ka task bana do"
"Kal Tahajjud 4 baje"
"Urgent task Quran padhne ka"
"Create task for Asr prayer"
```

#### Intent Patterns (Regex):
```regex
- task\s+(create|bana|add|new)
- (bana|create|add)\s+.*task
- namaz.*task
- (fajr|dhuhr|asr|maghrib|isha).*task
```

#### Parameter Extraction:
1. **Title**: User message se trigger words remove karke
   - Remove: "task", "bana", "create", "do", "kr", "ka", "ki"
   - Example: "Fajr ki namaz ka task bana do" → "Fajr namaz"

2. **Linked Prayer**:
   - Search for: fajr, dhuhr, asr, maghrib, isha
   - Case-insensitive matching
   - Default: None

3. **Priority**:
   - urgent/zaruri/important → high
   - low/kam → low
   - Default → medium

4. **Time**:
   - Regex: `(\d{1,2}):(\d{2})`
   - Example: "4:30" → extract time

#### API Call:
```python
execute_tool(
    "create_task",
    user_id=user_id,
    title=extracted_title,
    description=user_message,
    priority=extracted_priority,
    linked_prayer=extracted_prayer
)
```

#### Response Format:
```
✅ Task created successfully!

Title: Fajr namaz
Priority: medium
Linked Prayer: Fajr
```

---

### 2. Task Listing

#### Input Examples:
```
"Mujhe aaj ke tasks dikhao"
"Show my tasks"
"Mere pending tasks"
"Konse tasks hain"
```

#### Intent Patterns:
```regex
- (show|display|list|dikhao).*task
- task.*list
- mery\s+task
- konse\s+task
```

#### API Call:
```python
execute_tool("list_tasks", user_id=user_id)
```

#### Response Format:
```
📋 Your Tasks (3 total):

1. ⏳ Fajr namaz (Fajr)
   Priority: high

2. ✅ Quran reading
   Priority: medium

3. ⏳ Tahajjud reminder (None)
   Priority: low
```

---

### 3. Task Update

#### Input Examples:
```
"Quran task ko urgent mark karo"
"Task #1 complete kar do"
"Fajr task ka priority high karo"
```

#### Intent Patterns:
```regex
- task\s+(update|edit|change|modify)
- (complete|done|finish).*task
- urgent.*task
- task.*urgent
```

#### Parameters to Extract:
1. **Task Identifier**: Task number, title keywords
2. **Update Type**: complete, priority change, time change
3. **New Value**: new priority, new time, etc.

#### Implementation:
```python
# First, get user's tasks
tasks = execute_tool("list_tasks", user_id)

# Match task by number or title keywords
matched_task = find_matching_task(tasks, user_message)

# Update based on intent
if "complete" in user_message.lower():
    execute_tool("update_task", user_id, task_id=matched_task.id, completed=True)
elif "urgent" in user_message.lower():
    execute_tool("update_task", user_id, task_id=matched_task.id, priority="high")
```

---

### 4. Task Deletion

#### Input Examples:
```
"Quran task delete kar do"
"Remove task #2"
"Task 1 cancel karo"
```

#### Intent Patterns:
```regex
- task\s+(delete|remove|cancel)
- (delete|remove|cancel).*task
```

#### Implementation:
```python
# Get tasks
tasks = execute_tool("list_tasks", user_id)

# Find matching task
matched_task = find_matching_task(tasks, user_message)

# Delete
execute_tool("delete_task", user_id, task_id=matched_task.id)
```

---

### 5. Masjid Search

#### Input Examples:
```
"North Nazimabad mein konsi masjid hai"
"DHA area ka masjid"
"Nearest masjid"
```

#### Intent Patterns:
```regex
- masjid.*search
- konsi\s+masjid
- masjid.*area
- namaz.*kahan
```

#### Area Extraction:
```regex
(North Nazimabad|DHA|Clifton|Gulshan|Malir)
```

#### Response Format:
```
🕌 Found 2 masjid(s) in North Nazimabad:

1. Masjid Al-Huda
   Area: North Nazimabad, Karachi
   Fajr: 05:25 | Dhuhr: 12:55

2. Masjid Al-Noor
   Area: North Nazimabad, Karachi
   Fajr: 05:30 | Dhuhr: 13:00
```

---

### 6. General Conversation

#### Input Examples:
```
"Assalam o Alaikum"
"Tum kya kar sakte ho?"
"Help me"
```

#### Handling:
- Falls back to Google Gemini
- Uses SYSTEM_PROMPT for Islamic context
- Maintains conversation history

#### Response:
Natural language response from Gemini with Islamic context

---

## Implementation Steps

### Step 1: Enhanced Intent Detection
**File**: `chatbot/agent/agent.py`

```python
def detect_intent(user_message: str) -> Dict:
    """Enhanced intent detection with better patterns"""

    msg_lower = user_message.lower()

    # More comprehensive patterns
    intents = {
        "create_task": [
            r'task\s+(create|bana|add|new|banao)',
            r'(bana|create|add|set)\s+.*task',
            r'(fajr|dhuhr|asr|maghrib|isha).*task',
            r'task.*reminder',
        ],
        "list_tasks": [
            r'(show|display|list|dikhao|batao).*task',
            r'task.*list',
            r'(mery|mere|aapne)\s+task',
        ],
        # ... more intents
    }

    for intent, patterns in intents.items():
        for pattern in patterns:
            if re.search(pattern, msg_lower):
                return {"intent": intent, "message": user_message}

    return {"intent": "conversation", "message": user_message}
```

### Step 2: Task Matching Helper
**New Function**: `chatbot/agent/helpers.py`

```python
def find_matching_task(tasks: List[Dict], user_message: str) -> Optional[Dict]:
    """
    Find task from list based on:
    - Task number (#1, task 1, etc.)
    - Title keywords
    """

    # Check for task number
    task_num_match = re.search(r'(?:task\s*#?|#)(\d+)', user_message.lower())
    if task_num_match:
        task_num = int(task_num_match.group(1))
        if task_num <= len(tasks):
            return tasks[task_num - 1]

    # Check for title keywords
    for task in tasks:
        title_keywords = task['title'].lower().split()
        message_words = user_message.lower().split()

        # If 2+ keywords match, this is probably the task
        matches = sum(1 for kw in title_keywords if kw in message_words)
        if matches >= 2:
            return task

    return None
```

### Step 3: Update/Delete Implementation
**File**: `chatbot/agent/agent.py`

```python
elif intent == "update_task":
    # Get all tasks first
    tasks_result = execute_tool("list_tasks", user_id)

    if not tasks_result.get('success'):
        return "Could not fetch your tasks."

    tasks = tasks_result.get('tasks', [])
    matched_task = find_matching_task(tasks, user_message)

    if not matched_task:
        return "Task not found. Please specify task number or title."

    # Determine what to update
    updates = {}
    if any(word in user_message.lower() for word in ['complete', 'done', 'finish']):
        updates['completed'] = True

    if any(word in user_message.lower() for word in ['urgent', 'zaruri', 'important']):
        updates['priority'] = 'high'

    # Execute update
    result = execute_tool(
        "update_task",
        user_id,
        task_id=matched_task['id'],
        **updates
    )

    if result.get('success'):
        return f"✅ Task '{matched_task['title']}' updated successfully!"
    else:
        return f"❌ Failed to update task: {result.get('error')}"
```

---

## Error Handling Strategy

### 1. API Errors
```python
try:
    result = execute_tool(...)
except Exception as e:
    logger.error(f"Tool execution failed: {e}")
    if language == "ur":
        return "Maaf kijiye, ek error aaya. Dobara try karein."
    else:
        return "Sorry, an error occurred. Please try again."
```

### 2. Invalid Input
```python
if not matched_task:
    if language == "ur":
        return "Task nahi mila. Task number ya title specify karein."
    else:
        return "Task not found. Please specify task number or title."
```

### 3. Empty Results
```python
if not tasks:
    if language == "ur":
        return "Aapke koi tasks nahi hain. Naya task banana chahein?"
    else:
        return "You don't have any tasks. Would you like to create one?"
```

---

## Testing Plan

### Test Cases

#### 1. Task Creation
```
Input: "Fajr ka task bana do"
Expected: Task created with title containing "Fajr", linked_prayer="Fajr"

Input: "Urgent Quran reading reminder"
Expected: Task created with priority="high", title="Quran reading reminder"
```

#### 2. Task Listing
```
Input: "Mujhe tasks dikhao"
Expected: List of all tasks with proper formatting

Input: "Show my pending tasks"
Expected: List of incomplete tasks only
```

#### 3. Task Update
```
Input: "Task #1 complete kar do"
Expected: Task 1 marked as completed

Input: "Quran task urgent karo"
Expected: Quran task priority changed to high
```

#### 4. Error Scenarios
```
Input: "Delete task #999"
Expected: "Task not found" error

Input: Invalid/gibberish
Expected: Helpful fallback message
```

---

## Deployment Checklist

- [ ] All tests passing
- [ ] Error handling in place
- [ ] Logging configured
- [ ] Documentation updated
- [ ] Frontend integrated
- [ ] User testing completed
- [ ] Performance acceptable (<2s response)
- [ ] Urdu support verified

---

## Performance Targets

- **Response Time**: < 2 seconds
- **Success Rate**: > 95%
- **Intent Accuracy**: > 90%
- **Uptime**: 99%

---

## Future Enhancements

1. **Context Memory**: Remember previous conversation
2. **Multi-turn Dialogues**: "Tell me more about that"
3. **Voice Input**: Speech-to-text
4. **Personalization**: Learn user preferences
5. **Analytics**: Track usage patterns

---

**Document Version**: 1.0
**Last Updated**: 2025-12-30
**Author**: AI Development Team
**Status**: ACTIVE - Implementation in Progress
