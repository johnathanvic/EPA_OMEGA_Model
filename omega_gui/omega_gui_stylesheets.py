"""

This code contains stylesheets for the various graphical elements of the OMEGA GUI.
The color scheme is set to the standard EPA publication Pantone palette.

"""


def tab_stylesheet():
    """
    Loads the stylesheet for the tab area of the gui.

    :return: String containing stylesheet.

    """
    return """
            QTabBar::tab { 
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 rgb(00, 113, 188), stop: 1.0 rgb(00, 113, 188));
                min-width: 100px;       /* Sets the width of the tabs */
                height: 30px;           /* Sets the height of the tabs */
                padding-top : 0px;      /* Sets extra space at the top of the tabs */
                padding-bottom : 0px;   /* Sets extra space at the bottom of the tabs */
                color: white;           /* Sets the text color and frame color of the tabs */
                font: 12pt "Arial";     /* Sets the font for the tabs */
                }
            QTabBar::tab:hover { 
                font: bold;
                }    
            QTabWidget::tab-bar { 
                left: 15px;             /* Moves the tabs to the right */
                }    
            QTabWidget::pane {
                border-top: 1px solid white;     /* Sets the border color and thickness of the tab area */
                border-left: 1px solid white;
                border-right: 1px solid white;
                border-bottom: 1px solid white;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgb(00, 113, 188), stop: 1.0 rgb(00, 113, 188));
                }  
            QTabBar::tab:!selected {
                margin-top: 2px; /* Shrinks non-selected tabs */
                }
            QTabWidget {
                background: rgb(32, 84, 147);  /* Sets the color of the unselected tabs */
                }
            """


def vtab_stylesheet():
    """
    Loads the stylesheet for the tab area of the gui.

    :return: String containing stylesheet.

    """
    return """
            QTabBar::tab { 
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 rgb(00, 113, 188), stop: 1.0 rgb(00, 113, 188));
                min-width: 30px;       /* Sets the width of the tabs */
                height: 100px;           /* Sets the height of the tabs */
                padding-top : 0px;      /* Sets extra space at the top of the tabs */
                padding-bottom : 0px;   /* Sets extra space at the bottom of the tabs */
                padding-left : 0px;      /* Sets extra space at the top of the tabs */
                padding-right : 0px;   /* Sets extra space at the bottom of the tabs */
                color: white;           /* Sets the text color and frame color of the tabs */
                font: 12pt "Arial";     /* Sets the font for the tabs */
                }
            QTabBar::tab:hover { 
                font: bold;
                }    
            QTabWidget::tab-bar { 
                left: 0px;             /* Moves the tabs to the right */
                right: 0px;            /* Moves the tabs to the right */
                }    
            QTabWidget::pane {
                border-top: 1px solid white;     /* Sets the border color and thickness of the tab area */
                border-left: 1px solid white;
                border-right: 1px solid white;
                border-bottom: 1px solid white;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgb(00, 113, 188), stop: 1.0 rgb(00, 113, 188));
                }  
            QTabBar::tab:!selected {
                margin-top: 2px; /* Shrinks non-selected tabs */
                }
            QTabWidget {
                background: rgb(32, 84, 147);  /* Sets the color of the unselected tabs */
                }
            """


def button_stylesheet():
    """
    Loads the stylesheet for buttons contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QPushButton {
            border: 1px solid darkGray;
            border-radius: 6px;
            background-color: lightGray;
        }
        QPushButton:enabled {
            border: 1px solid black;            
            background-color: white;
        }
        QPushButton:hover {
            border: 2px solid lightBlue;
            border-radius: 6px;
        }
        QPushButton:pressed {
            border: 4px solid lightBlue;
            border-radius: 6px;
        }
     """


def logo_button_stylesheet():
    """
    Loads the stylesheet for logo buttons contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QPushButton {
            background-color: rgb(00, 113, 188);
            border: 0px solid white;
            border-radius: 6px;
        }
            QPushButton:enabled {
            background-color: rgb(00, 113, 188); 
            border: 0px solid white;
            color: white;
        }
        QPushButton:hover {
            border: 2px solid white;
            border-radius: 6px;
            font: bold;
            color: white;
        }
        QPushButton:pressed {
            border: 4px solid white;
            border-radius: 6px;
            font: bold;
            color: white;
        }
     """


def label_stylesheet():
    """
    Loads the stylesheet for labels contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QLabel { color : white; 
                }
     """


def checkbox_stylesheet():
    """
    Loads the stylesheet for checkboxes contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QCheckBox { color : white; }
     """


def groupbox_stylesheet():
    """
    Loads the stylesheet for checkboxes contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QGroupBox { color : white; }
     """


def textbox_stylesheet():
    """
    Loads the stylesheet for textboxes contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QTextEdit { border: 1px solid; 
                    border-radius:6px; 
                    background-color: palette(base);  }
     """


def listbox_stylesheet():
    """
    Loads the stylesheet for listboxes contained in the gui.

    :return: String containing stylesheet.

    """
    return """
        QListWidget { border: 1px solid; 
                      border-radius:6px; 
                      background-color: palette(base);
                      }
     """
