from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create sample PawPal+ data for terminal testing."""
    owner = Owner(
        name="Goldie",
        daily_time_budget=120,
        preferences=["cold-weather walks", "short evening check-ins"],
    )

    kodiak = Pet(name="Kodiak", species="brown bear", age=5, notes="Loves river splashing.")
    maple = Pet(name="Maple", species="brown bear", age=3, notes="Prefers calm snack breaks.")

    today = date.today()
    kodiak.add_task(Task("Berry breakfast", "08:00", 15, "high", "daily", today))
    kodiak.add_task(Task("River walk", "07:30", 30, "high", "daily", today))
    maple.add_task(Task("Salmon enrichment", "09:15", 20, "medium", "weekly", today))
    maple.add_task(Task("Cozy den cleanup", "07:30", 25, "low", "once", today))
    kodiak.add_task(Task("Porridge check", "18:00", 10, "medium", "once", today + timedelta(days=1)))

    owner.add_pet(kodiak)
    owner.add_pet(maple)
    return owner


def print_schedule() -> None:
    """Display the current schedule in a readable terminal format."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner)
    today = date.today()
    plan = scheduler.generate_daily_plan(today)
    conflicts = scheduler.detect_conflicts(today)

    print(f"Today's Schedule for {owner.name}")
    print("-" * 60)
    for item in plan:
        print(
            f"{item['time']} | {item['pet']:<6} | {item['task']:<18} | "
            f"{item['duration_minutes']:>3} min | {item['priority']}"
        )
        print(f"      Why: {item['reason']}")
    if conflicts:
        print("\nWarnings")
        print("-" * 60)
        for warning in conflicts:
            print(f"* {warning}")


if __name__ == "__main__":
    print_schedule()
