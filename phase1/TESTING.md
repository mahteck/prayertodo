# Phase I Testing Documentation

**Project**: SalaatFlow - Prayer & Spiritual Task Manager
**Phase**: I - In-Memory Python Console Application
**Date**: 2025-12-27

---

## Test Execution Instructions

All tests should be executed by running the application:
```bash
python3 phase1/main.py
```

Then follow the test scenarios below.

---

## Test Session 1: Basic CRUD Operations

**Reference**: Spec Section 5.1

### Test Steps

1. Start the application
2. Add Task 1:
   - Command: `add`
   - Title: `Attend Fajr at Masjid Al-Huda`
   - Description: `Wake up 30 minutes early`
   - Category: `1` (Farz)
   - Masjid: `Masjid Al-Huda`
   - Area: `DHA Phase 5`
   - Due: `2025-12-28 05:30`
   - Expected: "Task added successfully! (ID: 1)"

3. Add Task 2:
   - Command: `add`
   - Title: `Read Surah Yaseen after Fajr`
   - Description: (press Enter)
   - Category: `2` (Sunnah)
   - Masjid: (press Enter)
   - Area: (press Enter)
   - Due: (press Enter)
   - Expected: "Task added successfully! (ID: 2)"

4. Add Task 3:
   - Command: `add`
   - Title: `Give charity today`
   - Description: `Donate to local food bank`
   - Category: `4` (Deed)
   - Masjid: (press Enter)
   - Area: (press Enter)
   - Due: (press Enter)
   - Expected: "Task added successfully! (ID: 3)"

5. List all tasks:
   - Command: `list`
   - Expected: Table showing 3 tasks, all with [ ] status
   - Expected: "Total: 3 tasks (0 completed, 3 pending)"

6. Complete task 1:
   - Command: `complete 1`
   - Expected: "Task ID 1 marked as completed!"

7. List all tasks again:
   - Command: `list`
   - Expected: Task 1 shows [✓] status
   - Expected: "Total: 3 tasks (1 completed, 2 pending)"

8. Delete task 2:
   - Command: `delete 2`
   - Confirmation prompt shows ID 2 and title
   - Enter: `y`
   - Expected: "Task deleted successfully!"

9. List all tasks:
   - Command: `list`
   - Expected: Only tasks 1 and 3 shown
   - Expected: "Total: 2 tasks (1 completed, 1 pending)"

### Expected Result
✅ All operations succeed, task list reflects changes correctly

### Actual Result
_To be filled during testing_

### Status
- [ ] PASS
- [ ] FAIL

### Notes
_Any issues or deviations_

---

## Test Session 2: Filtering Tasks

**Reference**: Spec Section 5.2

### Test Steps
_(Continuing from Session 1 state)_

1. List pending tasks:
   - Command: `list pending`
   - Expected: Only task 3 shown
   - Expected: "Total: 1 task (0 completed, 1 pending)"

2. List completed tasks:
   - Command: `list completed`
   - Expected: Only task 1 shown
   - Expected: "Total: 1 task (1 completed, 0 pending)"

3. List all tasks:
   - Command: `list all`
   - Expected: Both tasks 1 and 3 shown
   - Expected: "Total: 2 tasks (1 completed, 1 pending)"

4. Try invalid filter:
   - Command: `list invalid_filter`
   - Expected: "Error: Invalid filter. Use: all, pending, or completed"

### Expected Result
✅ Filters correctly show only matching tasks

### Actual Result
_To be filled during testing_

### Status
- [ ] PASS
- [ ] FAIL

---

## Test Session 3: Update Task

**Reference**: Spec Section 5.3

### Test Steps
_(Continuing from Session 2 state)_

1. View task 3 in detail:
   - Command: `view 3`
   - Note the `created_at` and `updated_at` timestamps

2. Update task 3:
   - Command: `update 3`
   - Title: (press Enter to keep)
   - Description: `Donate $50 to Masjid Al-Noor`
   - Category: (press Enter to keep)
   - Masjid: `Masjid Al-Noor`
   - Area: `Gulshan-e-Iqbal`
   - Due: `2025-12-27 18:00`
   - Expected: "Task updated successfully!"

3. View task 3 again:
   - Command: `view 3`
   - Verify description changed to "Donate $50 to Masjid Al-Noor"
   - Verify masjid changed to "Masjid Al-Noor"
   - Verify area changed to "Gulshan-e-Iqbal"
   - Verify due date/time changed to "2025-12-27 18:00"
   - Verify `updated_at` timestamp changed
   - Verify `created_at` timestamp unchanged

### Expected Result
✅ Task updated with new values, timestamps managed properly

### Actual Result
_To be filled during testing_

### Status
- [ ] PASS
- [ ] FAIL

---

## Test Session 4: Error Handling

**Reference**: Spec Section 5.4

### Test Steps

1. Invalid command:
   - Command: `invalid_command`
   - Expected: "Error: Unknown command 'invalid_command'. Type 'help' for available commands."

2. Delete without ID:
   - Command: `delete`
   - Expected: "Error: Command 'delete' requires argument(s). Usage: delete <id>"

3. Delete non-existent ID:
   - Command: `delete 999`
   - Expected: "Error: Task with ID 999 not found."

4. Complete with invalid ID format:
   - Command: `complete abc`
   - Expected: "Error: Invalid task ID. Please enter a number."

5. View non-existent ID:
   - Command: `view 999`
   - Expected: "Error: Task with ID 999 not found."

6. List with invalid filter:
   - Command: `list invalid_filter`
   - Expected: "Error: Invalid filter. Use: all, pending, or completed"

### Expected Result
✅ All errors handled gracefully, application continues running

### Actual Result
_To be filled during testing_

### Status
- [ ] PASS
- [ ] FAIL

---

## Test Session 5: Complete Workflow

**Reference**: Spec Section 5.5

### Test Steps

1. Add task 4:
   - Command: `add`
   - Title: `Pray Dhuhr at office`
   - Description: `Set reminder 10 min before`
   - Category: `1` (Farz)
   - Masjid: (press Enter)
   - Area: `Clifton`
   - Due: `2025-12-27 13:30`
   - Expected: "Task added successfully! (ID: 4)"

2. Add task 5:
   - Command: `add`
   - Title: `Recite Ayat-ul-Kursi before sleep`
   - Description: (press Enter)
   - Category: `2` (Sunnah)
   - Masjid: (press Enter)
   - Area: (press Enter)
   - Due: `2025-12-27 23:00`
   - Expected: "Task added successfully! (ID: 5)"

3. List pending tasks:
   - Command: `list pending`
   - Expected: At least 3 pending tasks shown (3, 4, 5)

4. Complete task 4:
   - Command: `complete 4`
   - Expected: "Task ID 4 marked as completed!"

5. Uncomplete task 1:
   - Command: `uncomplete 1`
   - Expected: "Task ID 1 marked as incomplete!"

6. List all tasks:
   - Command: `list`
   - Verify task 4 shows [✓]
   - Verify task 1 shows [ ]
   - Expected: "Total: 4 tasks (1 completed, 3 pending)"

7. Exit application:
   - Command: `exit`
   - Expected: "JazakAllah Khair for using SalaatFlow! May your deeds be accepted."

### Expected Result
✅ All operations work seamlessly in realistic usage

### Actual Result
_To be filled during testing_

### Status
- [ ] PASS
- [ ] FAIL

---

## Overall Test Summary

### Results
- Session 1 (Basic CRUD): ⬜ PASS / ⬜ FAIL
- Session 2 (Filtering): ⬜ PASS / ⬜ FAIL
- Session 3 (Update): ⬜ PASS / ⬜ FAIL
- Session 4 (Error Handling): ⬜ PASS / ⬜ FAIL
- Session 5 (Complete Workflow): ⬜ PASS / ⬜ FAIL

### Phase I Acceptance Testing
⬜ PASS / ⬜ FAIL

### Issues Found
_List any bugs or deviations from spec_

### Resolution
_Document how issues were resolved (spec refinement and code regeneration)_

---

## How to Run Manual Tests

1. **Start fresh for each major test session**:
   ```bash
   python3 phase1/main.py
   ```

2. **Follow test steps exactly** as documented

3. **Record actual output** in the "Actual Result" sections

4. **Mark PASS/FAIL** for each session

5. **Document any issues** in the Issues Found section

6. **If failures occur**:
   - Do NOT manually edit code
   - Refine spec or task descriptions
   - Regenerate code via Claude Code
   - Retest

---

**Testing Date**: _________________
**Tester**: _________________
**Python Version**: _________________
