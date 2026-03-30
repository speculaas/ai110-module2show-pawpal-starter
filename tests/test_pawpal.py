from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_scheduler() -> tuple[Scheduler, Pet]:
    owner = Owner(name="Jordan", daily_time_budget=180)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    return Scheduler(owner), pet


def test_mark_complete_updates_status() -> None:
    scheduler, pet = build_scheduler()
    task = Task("Morning walk", "08:00", 20, "high", "once", date.today())
    pet.add_task(task)

    scheduler.mark_task_complete("Mochi", "Morning walk")

    assert task.completed is True


def test_add_task_increases_task_count() -> None:
    _, pet = build_scheduler()

    pet.add_task(Task("Breakfast", "07:30", 10))

    assert len(pet.tasks) == 1


def test_sorting_returns_tasks_in_chronological_order() -> None:
    scheduler, pet = build_scheduler()
    today = date.today()
    pet.add_task(Task("Evening walk", "18:00", 30, due_date=today))
    pet.add_task(Task("Breakfast", "07:00", 10, due_date=today))
    pet.add_task(Task("Lunch", "12:00", 10, due_date=today))

    pairs = scheduler.owner.all_tasks_for_day(today)
    sorted_pairs = scheduler.sort_tasks(pairs)

    assert [task.title for _, task in sorted_pairs] == ["Breakfast", "Lunch", "Evening walk"]


def test_daily_task_creates_next_occurrence_when_completed() -> None:
    scheduler, pet = build_scheduler()
    today = date.today()
    task = Task("Medication", "09:00", 5, "high", "daily", today)
    pet.add_task(task)

    scheduler.mark_task_complete("Mochi", "Medication", today)

    tomorrow_tasks = pet.pending_tasks_for_day(today + timedelta(days=1))
    assert len(tomorrow_tasks) == 1
    assert tomorrow_tasks[0].title == "Medication"


def test_detect_conflicts_flags_duplicate_times() -> None:
    scheduler, pet = build_scheduler()
    today = date.today()
    pet.add_task(Task("Morning walk", "08:00", 20, due_date=today))
    pet.add_task(Task("Breakfast", "08:00", 10, due_date=today))

    conflicts = scheduler.detect_conflicts(today)

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
