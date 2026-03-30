from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single pet care task on a specific date."""

    title: str
    time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def __post_init__(self) -> None:
        """Normalize incoming task values for predictable scheduling."""
        self.priority = self.priority.lower()
        self.frequency = self.frequency.lower()
        datetime.strptime(self.time, "%H:%M")
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        if self.priority not in PRIORITY_ORDER:
            raise ValueError("priority must be low, medium, or high")
        if self.frequency not in {"once", "daily", "weekly"}:
            raise ValueError("frequency must be once, daily, or weekly")

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task | None:
        """Create the next recurring task if this task repeats."""
        if self.frequency == "daily":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=7),
            )
        return None


@dataclass
class Pet:
    """Stores pet details and the tasks assigned to that pet."""

    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def pending_tasks_for_day(self, target_day: date) -> list[Task]:
        """Return incomplete tasks scheduled for the given day."""
        return [
            task
            for task in self.tasks
            if task.due_date == target_day and not task.completed
        ]


@dataclass
class Owner:
    """Tracks the pet owner and the pets in their care."""

    name: str
    daily_time_budget: int = 180
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def find_pet(self, pet_name: str) -> Pet | None:
        """Look up a pet by name."""
        pet_name = pet_name.strip().lower()
        for pet in self.pets:
            if pet.name.lower() == pet_name:
                return pet
        return None

    def all_tasks_for_day(self, target_day: date) -> list[tuple[Pet, Task]]:
        """Collect tasks for every pet on the requested day."""
        scheduled: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.pending_tasks_for_day(target_day):
                scheduled.append((pet, task))
        return scheduled


class Scheduler:
    """Builds and explains a daily pet care plan."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets will be scheduled."""
        self.owner = owner

    def sort_tasks(self, task_pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Order tasks by time and then by priority."""
        return sorted(
            task_pairs,
            key=lambda pair: (
                pair[1].due_date,
                pair[1].time,
                PRIORITY_ORDER[pair[1].priority],
                pair[0].name.lower(),
            ),
        )

    def filter_tasks(
        self,
        task_pairs: list[tuple[Pet, Task]],
        *,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet name and completion state."""
        filtered = task_pairs
        if pet_name is not None:
            pet_name = pet_name.strip().lower()
            filtered = [pair for pair in filtered if pair[0].name.lower() == pet_name]
        if completed is not None:
            filtered = [pair for pair in filtered if pair[1].completed == completed]
        return filtered

    def detect_conflicts(self, target_day: date | None = None) -> list[str]:
        """Return warning messages for tasks that share the same start time."""
        target_day = target_day or date.today()
        conflicts: list[str] = []
        grouped: dict[str, list[str]] = {}
        for pet, task in self.owner.all_tasks_for_day(target_day):
            grouped.setdefault(task.time, []).append(f"{pet.name}: {task.title}")
        for time_slot, labels in grouped.items():
            if len(labels) > 1:
                conflicts.append(
                    f"Conflict at {time_slot}: " + ", ".join(labels)
                )
        return conflicts

    def generate_daily_plan(self, target_day: date | None = None) -> list[dict[str, str | int]]:
        """Build a daily plan that respects the owner's time budget."""
        target_day = target_day or date.today()
        scheduled = self.sort_tasks(self.owner.all_tasks_for_day(target_day))
        remaining = self.owner.daily_time_budget
        plan: list[dict[str, str | int]] = []

        for pet, task in scheduled:
            if task.duration_minutes > remaining:
                continue
            explanation = (
                f"Scheduled because {pet.name} needs {task.title.lower()} at {task.time} "
                f"and it is marked {task.priority} priority."
            )
            plan.append(
                {
                    "pet": pet.name,
                    "task": task.title,
                    "time": task.time,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "reason": explanation,
                }
            )
            remaining -= task.duration_minutes

        return plan

    def mark_task_complete(self, pet_name: str, task_title: str, target_day: date | None = None) -> Task | None:
        """Complete a task and spawn the next recurring instance when needed."""
        target_day = target_day or date.today()
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if (
                task.title == task_title
                and task.due_date == target_day
                and not task.completed
            ):
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return task
        return None
