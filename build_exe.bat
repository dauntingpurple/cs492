pyinstaller --onefile --windowed ^
    --add-data "src;src" ^
    --add-data "gui;gui" ^
    --add-data "school_management_system.db;." ^
    main.py
