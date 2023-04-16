#!/bin/bash

echo "Choose an option:"
echo "1. Run with default parameters"
echo "2. Run interactively (customize parameters)"
echo "3. Run with GUI"
read -p "Enter your choice (1, 2, or 3): " choice

run_defaults() {
    echo "Running with default parameters..."
    source venv/bin/activate
    python app.py
    deactivate
}

run_gui() {
    echo "Running with GUI..."
    source venv/bin/activate
    python gui.py
    deactivate
}

interactive() {
    echo "Interactive mode: Enter your desired parameter values or press Enter to use default values."
    read -p "Input folder [default=_INPUT]: " input_folder
    input_folder=${input_folder:-_INPUT}
    read -p "Output folder [default=_OUTPUT]: " output_folder
    output_folder=${output_folder:-_OUTPUT}
    read -p "Horizontal offset of face center [default=0.0]: " offset_x
    offset_x=${offset_x:-0.0}
    read -p "Vertical offset of face center [default=-15.0]: " offset_y
    offset_y=${offset_y:--15.0}
    read -p "Size of face in the resulting photo as a percentage [default=40.0]: " face_percent
    face_percent=${face_percent:-40.0}
    read -p "Size of the output image [default=512]: " resize
    resize=${resize:-512}
    read -p "Threshold of face detection (0-1) [default=0.5]: " threshold
    threshold=${threshold:-0.5}
    read -p "Output format (jpg, png, etc.) [default=jpg]: " output_format
    output_format=${output_format:-jpg}

    source venv/bin/activate
    python app.py --input_folder "$input_folder" --output_folder "$output_folder" --offset_x "$offset_x" --offset_y "$offset_y" --face_percent "$face_percent" --resize "$resize" --threshold "$threshold" --output_format "$output_format"
    deactivate
}

case $choice in
    1)
        run_defaults
        ;;
    2)
        interactive
        ;;
    3)
        run_gui
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
