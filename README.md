# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit pet care planner that helps an owner manage tasks across pets, sort them into a daily plan, and explain why those tasks were chosen. This build uses a light Alaska brown bear / modern Goldilocks theme for the sample data while still following the project requirements.

## Features

- Add pets and care tasks from the Streamlit app
- Store owner, pet, and task data in backend Python classes
- Generate a daily plan based on time budget, task time, and priority
- Sort tasks chronologically and filter out completed work
- Detect same-time conflicts and show warnings in the UI
- Create the next occurrence automatically for daily and weekly recurring tasks
- Run a CLI demo through `main.py` to verify the logic outside Streamlit

## System Design

The project uses four core classes:

- `Owner`: stores the owner's name, available time budget, preferences, and pets
- `Pet`: stores pet details and the list of tasks assigned to that pet
- `Task`: stores title, time, duration, priority, frequency, date, and completion state
- `Scheduler`: sorts tasks, builds a plan, flags conflicts, and handles recurring tasks

```mermaid
classDiagram
    class Owner {
        +name: str
        +daily_time_budget: int
        +preferences: list[str]
        +pets: list[Pet]
        +add_pet(pet)
        +find_pet(pet_name)
        +all_tasks_for_day(target_day)
    }
    class Pet {
        +name: str
        +species: str
        +age: int
        +notes: str
        +tasks: list[Task]
        +add_task(task)
        +pending_tasks_for_day(target_day)
    }
    class Task {
        +title: str
        +time: str
        +duration_minutes: int
        +priority: str
        +frequency: str
        +due_date: date
        +completed: bool
        +mark_complete()
        +next_occurrence()
    }
    class Scheduler {
        +sort_tasks(task_pairs)
        +filter_tasks(task_pairs, pet_name, completed)
        +detect_conflicts(target_day)
        +generate_daily_plan(target_day)
        +mark_task_complete(pet_name, task_title, target_day)
    }
    Owner "1" --> "*" Pet
    Pet "1" --> "*" Task
    Scheduler --> Owner
```

## Smarter Scheduling

The scheduler applies a few simple algorithms:

- Sort tasks by date, time, and priority
- Skip tasks that do not fit within the owner's daily time budget
- Warn when multiple tasks share the same start time
- Create the next daily or weekly task when a recurring task is marked complete

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To preview the backend in the terminal:

```bash
python main.py
```

## Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

The current test suite covers task completion, task addition, chronological sorting, recurring task creation, and exact-time conflict detection.

Confidence Level: `★★★★☆`

## Demo

This demo uses a light Alaska brown bear / modern Goldilocks theme to make the sample data more memorable while keeping the required scheduler structure intact.

### Demo Flow

1. Start with the seeded pets `Kodiak` and `Maple`, or add a new pet from the UI.
2. Create a task with a time, duration, priority, and frequency.
3. Click `Generate schedule` to build the daily plan.
4. Review the sorted task table, explanation captions, and any conflict warnings.

### What The Screenshots Show

- Owner profile and daily time budget setup
- Adding pets and themed care tasks from the Streamlit form
- A generated schedule sorted by time and priority
- Conflict warnings when two tasks share the same start time

### App Screens

**1. Owner setup and seeded pet data**

<img width="901" height="770" alt="PawPal owner setup and seeded brown bear data" src="https://github.com/user-attachments/assets/48c41ad7-9957-4a14-96d0-d455c2e1c141" />

**2. Adding a new pet and task**

<img width="1063" height="863" alt="PawPal form for adding a pet and scheduling a task" src="https://github.com/user-attachments/assets/d62df43b-09d6-4154-9708-f7cd6172c2ad" />

**3. Generated daily schedule**

<img width="782" height="695" alt="PawPal generated daily schedule table" src="https://github.com/user-attachments/assets/ff25d3b0-e875-4c9f-add2-b1a8c35f762a" />

**4. Conflict warning example**

<img width="762" height="774" alt="PawPal warning showing a same-time task conflict" src="https://github.com/user-attachments/assets/4d62940b-5ee4-4fc1-bccb-905cffbecf94" />

### Notes

I manually tested the app by adding pets, creating tasks, generating a schedule, and confirming that same-time tasks produce a warning in the UI. I also verified the backend behavior separately through `main.py` and the automated pytest suite.

I tested adding a pet, creating tasks, generating a schedule, and verifying conflict warnings.



