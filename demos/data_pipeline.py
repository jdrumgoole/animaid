#!/usr/bin/env python3
"""Demo: Data Pipeline

Demonstrates: Progress tracking with status transitions.

Simulates an ETL (Extract-Transform-Load) pipeline:
- Each stage shows progress from 0% to 100%
- Status colors change as stages complete
- Completion indicators show success
"""

import time

from animaid import Animate, HTMLDict, HTMLString


def create_progress_bar(percent: int) -> str:
    """Create a text-based progress bar."""
    filled = int(percent / 5)  # 20 chars total
    empty = 20 - filled
    return f"[{'=' * filled}{' ' * empty}] {percent}%"


def main() -> None:
    print("Starting Data Pipeline Demo...")
    print("Watch the ETL pipeline process data in stages!")
    print()

    with Animate(title="Demo: Data Pipeline") as anim:
        # Title
        title = HTMLString("ETL Data Pipeline").bold().xxl()
        anim.add(title)

        # Pipeline stages
        stages = ["Extract", "Transform", "Load"]

        # Create status dict
        pipeline_status = HTMLDict({
            "Extract": "Pending",
            "Transform": "Pending",
            "Load": "Pending",
        }).card().key_bold().key_width("120px")
        anim.add(pipeline_status)

        # Overall progress
        overall_label = HTMLString("Overall Progress").bold().large()
        anim.add(overall_label)

        overall_progress = HTMLString("0% Complete").muted()
        overall_id = anim.add(overall_progress)

        time.sleep(1)

        # Process each stage
        print("Processing pipeline stages:")
        print()

        for stage_idx, stage in enumerate(stages):
            print(f"Stage: {stage}")

            # Mark stage as in progress
            pipeline_status[stage] = "In Progress..."

            # Simulate progress
            for percent in range(0, 101, 10):
                progress_bar = create_progress_bar(percent)
                pipeline_status[stage] = progress_bar

                # Update overall progress
                overall_pct = ((stage_idx * 100) + percent) // len(stages)
                overall_progress = HTMLString(f"{overall_pct}% Complete").info()
                anim.update(overall_id, overall_progress)

                print(f"  {stage}: {percent}%")
                time.sleep(0.1)

            # Mark stage as complete
            pipeline_status[stage] = "Complete"
            print(f"  {stage}: Complete!")
            print()
            time.sleep(0.3)

        # All done!
        overall_progress = HTMLString("100% Complete!").success().bold()
        anim.update(overall_id, overall_progress)

        # Add success message
        success_msg = HTMLString("Pipeline completed successfully!").success().large()
        anim.add(success_msg)

        print("Pipeline completed successfully!")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
