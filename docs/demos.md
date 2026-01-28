# Demo Programs

AnimAID includes demo programs that showcase its interactive capabilities. Each demo opens a browser window and shows real-time updates as Python code executes.

## Running Demos

List all available demos:
```bash
animaid-demo --list
```

Run a specific demo:
```bash
animaid-demo countdown_timer
```

Or run directly with Python:
```bash
python demos/countdown_timer.py
```

## Core Demos

### Countdown Timer

Real-time countdown with color transitions (green → yellow → red).

```bash
animaid-demo countdown_timer
```

![Countdown Timer Demo](images/demos/countdown_timer.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/countdown_timer.py)

### Sorting Visualizer

Bubble sort algorithm with step-by-step visualization.

```bash
animaid-demo sorting_visualizer
```

![Sorting Visualizer Demo](images/demos/sorting_visualizer.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/sorting_visualizer.py)

### Dashboard

Multi-type dashboard with HTMLString, HTMLDict, HTMLList, and HTMLSet all updating together.

```bash
animaid-demo dashboard
```

![Dashboard Demo](images/demos/dashboard.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/dashboard.py)

### Todo App

Interactive todo list with CRUD operations.

```bash
animaid-demo todo_app
```

![Todo App Demo](images/demos/todo_app.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/todo_app.py)

### Live List

Reactive shopping cart showing `.append()` and `.pop()` with automatic updates.

```bash
animaid-demo live_list
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/live_list.py)

### Score Tracker

Game score tracking with automatic dict updates.

```bash
animaid-demo score_tracker
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/score_tracker.py)

### Typewriter

Typewriter effect with progressive styling animation.

```bash
animaid-demo typewriter
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/typewriter.py)

### Data Pipeline

ETL pipeline progress tracking with status transitions.

```bash
animaid-demo data_pipeline
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/data_pipeline.py)

## Input Widget Demos

### Button Showcase

Button styles (default, primary, success, warning, danger), sizes, and click event handling.

```bash
animaid-demo input_button
```

![Button Demo](images/demos/input_button.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_button.py)

### Text Input

Text input with live character counting, validation, and mirroring.

```bash
animaid-demo input_text
```

![Text Input Demo](images/demos/input_text.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_text.py)

### Checkbox Showcase

Checkbox toggles, preferences panel, and multi-checkbox patterns.

```bash
animaid-demo input_checkbox
```

![Checkbox Demo](images/demos/input_checkbox.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_checkbox.py)

### Select Dropdown

Select dropdowns with dynamic updates and styling.

```bash
animaid-demo input_select
```

![Select Demo](images/demos/input_select.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_select.py)

### RGB Color Mixer

Sliders for real-time color mixing.

```bash
animaid-demo input_slider
```

![Slider Demo](images/demos/input_slider.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_slider.py)

### Interactive Counter

Counter with increment/decrement buttons.

```bash
animaid-demo input_counter
```

![Counter Demo](images/demos/input_counter.gif)

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_counter.py)

### Interactive Greeter

Text input with greeting button.

```bash
animaid-demo input_greeter
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_greeter.py)

### Registration Form

Complete form with multiple input widget types.

```bash
animaid-demo input_form
```

[View Source](https://github.com/jdrumgoole/animaid/blob/main/demos/input_form.py)

## Command Line Options

```
usage: animaid-demo [-h] [--list] [name]

Run AnimAID demo programs

positional arguments:
  name        Name of the demo to run

options:
  -h, --help  show this help message and exit
  --list, -l  List all available demos
```
