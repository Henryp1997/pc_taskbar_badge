from pathlib import Path
import cx_Freeze

HERE = Path(__file__).parent

executables = [
    cx_Freeze.Executable(
        str(HERE / "pc_taskbar_badge.py"),
        base="gui",
        target_name="pc_taskbar_badge.exe",
    )
]

cx_Freeze.setup(
    name="pc_taskbar_badge",
    executables=executables,
    options={
        "build_exe": {
            "include_files": [
                # Copy assets folder to build folder
                (str(HERE / "config.yml"), "config.yml"),
            ],
        }
    }
)
