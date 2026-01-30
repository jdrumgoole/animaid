#!/usr/bin/env python3
"""Demo: Dashboard

Demonstrates: Multiple HTML types working together in a real-world pattern.

Shows a dashboard with:
- Title (HTMLString)
- Stats panel (HTMLDict)
- Activity log (HTMLList)
- Tags (HTMLSet)

All updating in real-time!
"""

import random
import time

from animaid import App, HTMLDict, HTMLList, HTMLSet, HTMLString


def main() -> None:
    print("Starting Dashboard Demo...")
    print("Watch all components update together in real-time!")
    print()

    with App(title="Demo: Dashboard") as app:
        # Dashboard Title
        title = HTMLString("System Dashboard").bold().xxl()
        app.add(title)

        # Stats Panel (Dict)
        stats_label = HTMLString("System Stats").bold().large()
        app.add(stats_label)

        stats = (
            HTMLDict(
                {
                    "Requests": 0,
                    "Users": 42,
                    "CPU": "23%",
                    "Memory": "1.2 GB",
                }
            )
            .card()
            .key_width("100px")
        )
        app.add(stats)

        # Activity Log (List)
        log_label = HTMLString("Recent Activity").bold().large()
        app.add(log_label)

        activity_log = HTMLList([]).menu().max_width("400px")
        app.add(activity_log)

        # Active Tags (Set)
        tags_label = HTMLString("Active Services").bold().large()
        app.add(tags_label)

        tags = HTMLSet({"web", "api"}).pills()
        app.add(tags)

        time.sleep(1)

        # Simulate activity
        print("Simulating dashboard activity...")
        print()

        activities = [
            ("User login", "auth"),
            ("API request", "api"),
            ("File upload", "storage"),
            ("Cache hit", "cache"),
            ("DB query", "database"),
            ("Payment processed", "billing"),
            ("Email sent", "email"),
            ("Report generated", "reports"),
        ]

        for i in range(12):
            # Increment requests
            stats["Requests"] = i + 1

            # Random CPU/Memory changes
            stats["CPU"] = f"{random.randint(15, 85)}%"
            stats["Memory"] = f"{random.uniform(1.0, 3.5):.1f} GB"

            # Random user change
            stats["Users"] = stats["Users"] + random.choice([-1, 0, 1, 2])

            # Add activity
            activity_text, service = random.choice(activities)
            timestamp = f"{12 + (i // 5)}:{(i * 7) % 60:02d}"
            log_entry = HTMLString(f"[{timestamp}] {activity_text}").small()

            # Keep only last 5 entries
            if len(activity_log) >= 5:
                activity_log.pop(0)
            activity_log.append(log_entry)

            # Add/remove random services
            if random.random() > 0.7:
                tags.add(service)
            if random.random() > 0.85 and len(tags) > 2:
                try:
                    tags.discard(random.choice(list(tags)))
                except KeyError:
                    pass

            print(f"  Update {i + 1}: {activity_text} ({service})")
            time.sleep(0.4)

        print()
        print("Dashboard simulation complete!")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
