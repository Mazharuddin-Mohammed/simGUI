"""
README for Simulation Project Manager GUI
========================================

Overview
--------
This application is a modular, extensible GUI for managing and running simulation projects. It features:
- Project management (create, open, edit, recent projects)
- Simulation workflow (Device, Mesh, Material Properties, Physical Models, Solution, Visualization, Help & Support, About)
- Vulkan-based visualization
- Shared log window with filtering/search
- User preferences/settings

Directory Structure
-------------------
- main.py: Application entry point
- settings.py/settings.json: Persistent user and app settings
- ui/: All UI modules (main window, secondary window, dialogs, log, tabs)
- vulkan/: VulkanWidget for rendering/visualization

Usage
-----
1. Run the application:
   python3 main.py
2. Use the primary window to create, open, or edit simulation projects.
3. Access recent projects and preferences from the main window.
4. Launch the simulation workflow (secondary window) for project-specific tasks.
5. Use the log window to view and filter all actions/events.

Extending
---------
- Add new simulation steps by creating new tab widgets in ui/secondary_window.py.
- Add new dialogs or settings in ui/dialogs.py.
- Customize Vulkan rendering in vulkan/vulkan_widget.py.

Requirements
------------
- Python 3.10+
- PySide6

Author & License
----------------
(c) 2025 Dr. Mazharuddin Mohammed. All rights reserved.

"""