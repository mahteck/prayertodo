# SalaatFlow Constitution

## Project Identity

**SalaatFlow – Intelligent Prayer & Masjid Todo Assistant**

A 5-phase hackathon project that evolves a Todo system into a specialized Islamic prayer and spiritual task management platform, fully compliant with spec-driven development methodology.

---

## Core Principles

### 1. Spec-Driven Development (Non-Negotiable)
- **Every feature requires a Markdown specification before implementation**
- **No manual production code** – all code generated via Claude Code from specs
- **Spec → Plan → Tasks → Implementation** workflow is mandatory
- If code doesn't match behavior, **update specs and regenerate**, never patch manually

### 2. Domain-First Architecture
- The system is a **Todo evolution** applied to Islamic spiritual practices
- All "Evolution of Todo" requirements must be satisfied through the prayer/spiritual lens
- Clean separation: Domain → Infrastructure → Presentation

### 3. Progressive Evolution
- Each phase **builds upon** the previous, not replaces
- The core domain model evolves incrementally across all 5 phases
- No rewrites – only extensions and enhancements

---

## Domain Model Mapping

### Todo → Spiritual Task Transformation

| Generic Todo Concept | SalaatFlow Equivalent | Notes |
|---------------------|----------------------|-------|
| Task | Spiritual Task | Prayer obligations, good deeds, reminders |
| Priority | Farz/Sunnah/Nafl or High/Medium/Low | Religious significance or urgency |
| Category | Prayer/Quran/Charity/Deed/Dhikr | Islamic practice categories |
| Due Date | prayer_time or due_time | Tied to prayer times or custom deadlines |
| Recurrence | Daily prayers, Weekly Jummah, Custom | Islamic ritual repetition patterns |
| Tags | Masjid name, Area, Practice type | Location and context metadata |

### Core Entities

#### 1. Spiritual Task
```
Properties:
- id: unique identifier
- title: task name (e.g., "Attend Fajr at Masjid Al-Huda")
- description: optional details
- category: Farz | Sunnah | Nafl | Deed | Quran | Charity | Dhikr
- priority: High | Medium | Low (or Farz/Sunnah/Nafl mapping)
- masjid: optional masjid reference
- area: optional location/area
- prayer_time: optional prayer timing reference
- due_time: optional custom deadline
- completed: boolean
- recurrence: none | daily | weekly | custom pattern
- tags: array of strings
- created_at: timestamp
- updated_at: timestamp
```

#### 2. Masjid
```
Properties:
- id: unique identifier
- name: masjid name
- area: locality/neighborhood
- location: address or coordinates
- prayer_timetable: {Fajr, Dhuhr, Asr, Maghrib, Isha, Jummah}
```

#### 3. User
```
Properties:
- id: unique identifier
- name: user name
- preferences: settings object
- default_area: preferred locality
- preferred_masjid: default masjid reference
```

#### 4. Daily Hadith (Optional Enhancement)
```
Properties:
- id: unique identifier
- content: hadith text
- source: reference (e.g., Sahih Bukhari 123)
- date: display date
```

---

## Functional Requirements

### Phase I & II – Basic Operations
- ✅ Add spiritual tasks
- ✅ Delete spiritual tasks
- ✅ Update spiritual task details
- ✅ View all tasks or single task
- ✅ Mark tasks as complete

### Phase II+ – Intermediate Features
- ✅ Assign priorities (Farz/Sunnah/Nafl or High/Medium/Low)
- ✅ Tag tasks (Masjid names, areas, practice types)
- ✅ Search tasks by keyword
- ✅ Filter tasks by:
  - Completion status
  - Priority/Category
  - Masjid
  - Area
  - Date range
- ✅ Sort tasks by:
  - Created date
  - Due time/Prayer time
  - Priority
  - Completion status

### Phase III+ – Advanced Features
- ✅ Recurring tasks:
  - Daily prayers (Fajr, Dhuhr, Asr, Maghrib, Isha)
  - Weekly Jummah
  - Custom recurrence patterns
- ✅ Due dates and reminders:
  - Tied to prayer times from masjid timetables
  - Configurable offsets (e.g., 15 min before Adhan)
- ✅ Masjid & area management:
  - User selects area → sees masjids in that area
  - View prayer timetables per masjid
- ✅ AI Chatbot natural language interface:
  - Query: "Is area ki Masjid Al-Huda mein Fajr ka time kya hai?"
  - Command: "Kal se Fajr ke 20 minutes pehle mujhe remind karna"
  - Task creation: "Is Jummah se pehle sadqah dene ka ek task add karo"
  - Support Urdu/English mixed language

---

## Technical Stack by Phase

### Phase I: Python Console App
- **Language**: Python 3.11+
- **Storage**: In-memory (lists/dicts)
- **Interface**: CLI with input/menu system
- **Focus**: Core domain logic and CRUD operations

### Phase II: Full-Stack Web App
- **Frontend**: Next.js 14+ (App Router, React Server Components, TypeScript)
- **Backend**: FastAPI (Python)
- **Database**: Neon Postgres with SQLModel ORM
- **API**: RESTful endpoints
- **Focus**: Persistent storage, web UI, API contracts

### Phase III: AI Integration
- **Chatbot**: OpenAI ChatKit
- **Agent Framework**: OpenAI Agents SDK
- **Tools**: Official MCP SDK for tool integrations
- **NLP**: Natural language task management
- **Focus**: Conversational interface, intelligent parsing

### Phase IV: Local Kubernetes
- **Containers**: Docker
- **Orchestration**: Minikube
- **Package Manager**: Helm
- **AI Tooling**: kubectl-ai, kagent
- **Focus**: Container orchestration, local cloud-native deployment

### Phase V: Cloud Deployment
- **Message Broker**: Apache Kafka
- **Runtime**: Dapr (Distributed Application Runtime)
- **Cloud Provider**: DigitalOcean Kubernetes (DOKS)
- **Focus**: Production-grade distributed system

---

## Non-Functional Requirements

### Architecture
- **Modular design**: Clear separation of concerns
- **Domain isolation**: Spiritual task logic independent of infrastructure
- **API-first**: RESTful contracts documented before implementation
- **Extensible**: New prayer types, masjids, and features easily added

### Testing
- **Automated tests** for each phase (unit, integration where applicable)
- **Test specs** documented alongside feature specs
- **Scriptable test execution** for CI/CD readiness

### Documentation
- **Phase I**: CLI usage guide, command reference
- **Phase II+**: REST API documentation (OpenAPI/Swagger)
- **Phase III+**: Chatbot skills catalog, tool definitions
- **Phase IV–V**: Deployment runbooks, infrastructure diagrams

### Code Quality
- **Generated code only** – no manual patches
- **Type safety**: TypeScript (frontend), Python type hints (backend)
- **Consistent naming**: Islamic terms in English transliteration
- **Comments**: Minimal, only where domain logic is complex

---

## Workflow Guardrails

### Before Any Implementation
1. **Write or update Constitution** (this document) if project scope changes
2. **Create detailed Specification** in `/specs/{feature}.md`
3. **Generate Implementation Plan** in `/plans/{feature}.md`
4. **Break down into Tasks** in `/tasks/{feature}.md`
5. **Implement code** via Claude Code based on approved specs

### During Implementation
- **Never manually edit generated code** – regenerate from updated specs
- **Validate against specs** after each generation
- **Update specs first** if requirements change
- **Keep phase boundaries clear** – don't leak Phase III features into Phase I

### Code Generation Rules
- **Read existing code** before proposing changes
- **Follow domain model** strictly as defined in Constitution
- **Preserve existing functionality** when adding features
- **Use established patterns** from previous phases
- **No over-engineering** – implement only what specs require

---

## Example Use Cases

### Phase I Example
```
> Add task
Title: Attend Fajr at Masjid Al-Noor
Category: Farz
Priority: High
Area: DHA Phase 5
Task added successfully!
```

### Phase III Chatbot Example
```
User: "Kal se Fajr ke 15 minutes pehle mujhe yaad dilao"
Bot: "Understood. I'll create a recurring daily reminder 15 minutes before Fajr prayer time. Which masjid's timetable should I use?"
User: "Masjid Al-Huda"
Bot: "Reminder set! You'll receive a notification 15 minutes before Fajr at Masjid Al-Huda starting tomorrow."
```

---

## Success Criteria

### Per Phase
- **Phase I**: Working CLI with in-memory CRUD operations
- **Phase II**: Web app with persistent DB, all basic + intermediate features
- **Phase III**: Natural language chatbot can manage tasks and query masjid times
- **Phase IV**: Local Kubernetes deployment with Helm charts
- **Phase V**: Production deployment on DOKS with Kafka + Dapr

### Overall Project
- ✅ All "Evolution of Todo" requirements satisfied
- ✅ Islamic domain model fully implemented
- ✅ Spec-driven development maintained throughout
- ✅ Clean progression from Phase I → V
- ✅ Documentation complete for each phase
- ✅ Deployable and demonstrable end-to-end

---

## Constraints & Boundaries

### Must Have
- Spec-first approach for every feature
- Islamic terminology and prayer time integration
- Multi-phase progressive evolution
- Clean domain modeling

### Must Not Have
- Manual code patches (regenerate from specs instead)
- Phase leakage (Phase I code shouldn't have Phase III complexity)
- Hardcoded prayer times (use masjid timetables)
- Mixed English/Urdu in code (transliteration only)

### Nice to Have (Future)
- Qibla direction finder
- Zakat calculator integration
- Ramadan-specific features
- Community masjid event sharing

---

## File Structure Convention

```
/
├── specs/
│   ├── constitution.md (this file)
│   ├── phase1-cli.md
│   ├── phase2-webapp.md
│   ├── phase3-ai.md
│   ├── phase4-k8s.md
│   └── phase5-cloud.md
├── plans/
│   ├── phase1-plan.md
│   ├── phase2-plan.md
│   └── ...
├── tasks/
│   ├── phase1-tasks.md
│   └── ...
├── phase1/ (Python CLI)
├── phase2/ (Next.js + FastAPI)
├── phase3/ (AI integration)
├── phase4/ (K8s configs)
└── phase5/ (Cloud deployment)
```

---

## This Constitution Governs

- All `/sp.specify` commands must reference this Constitution
- All `/sp.plan` outputs must align with phase requirements here
- All `/sp.tasks` breakdowns must map to domain entities defined here
- All `/sp.implement` code generation must follow the domain model and tech stack specified here

**Last Updated**: 2025-12-27
**Status**: Active Constitution for SalaatFlow Hackathon Project
