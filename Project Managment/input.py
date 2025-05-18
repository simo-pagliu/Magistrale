# -----------------------------
# input_data.py
# -----------------------------
section_colors = {
    'Engineering': '#005580',
    'Procurement': '#0073e6',
    'Construction': '#008000',
    'Testing': '#FFA500'
}
# Updated task list matching the network diagram, with unique names and correct durations,
# parents adjusted to reflect the “PFD – Heat&Mass Balance” root, and all duplicates renamed.

tasks = [
  {
    "name": "PFD - Heat&Mass Balance",
    "duration": 13.0,
    "section": "Engineering",
    "parents": [],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Filter Procurement",
    "duration": 1.0,
    "section": "Procurement",
    "parents": [
      "Filter Data Sheet"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Filter Data Sheet",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pump Data Sheet",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Sterilizer&mineralizer DS",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Valve Data Sheet",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Instrument Data Sheet",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 2500.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Logic Map",
    "duration": 5.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance",
      "P&ID"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6666.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Instruments List",
    "duration": 2.0,
    "section": "Engineering",
    "parents": [
      "P&ID"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6666.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pneumatic Calculation",
    "duration": 3.0,
    "section": "Engineering",
    "parents": [
      "Instruments List"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6666.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Piping Class",
    "duration": 2.0,
    "section": "Engineering",
    "parents": [
      "Pneumatic Calculation"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 1120.0
    }
  },
  {
    "name": "Painting Procedure",
    "duration": 2.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 1120.0
    }
  },
  {
    "name": "Valve List",
    "duration": 2.0,
    "section": "Engineering",
    "parents": [
      "P&ID"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 1120.0
    }
  },
  {
    "name": "P&ID",
    "duration": 5.0,
    "section": "Engineering",
    "parents": [
      "PFD - Heat&Mass Balance",
      "Piping Class"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 2800.0
    }
  },
  {
    "name": "BOM BOP",
    "duration": 2.0,
    "section": "Engineering",
    "parents": [
      "3D Model"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "General Arrangement",
    "duration": 1.0,
    "section": "Engineering",
    "parents": [
      "BOM BOP"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Isometric DWG",
    "duration": 5.0,
    "section": "Engineering",
    "parents": [],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Structures DWG",
    "duration": 3.0,
    "section": "Engineering",
    "parents": [],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "3D Model",
    "duration": 20.0,
    "section": "Engineering",
    "parents": [
      "P&ID"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 6000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Control Panel Logic",
    "duration": 25.0,
    "section": "Engineering",
    "parents": [
      "Logic Map"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 8000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Control Systems",
    "duration": 10.0,
    "section": "Engineering",
    "parents": [
      "Logic Map"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 8000.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Electrical Hook-Up",
    "duration": 25.0,
    "section": "Engineering",
    "parents": [
      "Control Systems"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 8333.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Wiring Diagram",
    "duration": 10.0,
    "section": "Engineering",
    "parents": [
      "Control Panel Logic"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 8333.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pneumatic Hook-Up",
    "duration": 10.0,
    "section": "Engineering",
    "parents": [
      "Wiring Diagram"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 8333.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Filter",
    "duration": 140.0,
    "section": "Procurement",
    "parents": [
      "Pneumatic Hook-Up"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 6000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Sterilizer&mineralizer",
    "duration": 150.0,
    "section": "Procurement",
    "parents": [
      "Filter"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 7000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pump",
    "duration": 150.0,
    "section": "Procurement",
    "parents": [
      "Sterilizer&mineralizer"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 8000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Fitting",
    "duration": 30.0,
    "section": "Procurement",
    "parents": [
      "Pump"
    ],
    "resources": {
      "Materials": 10000.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Flanges",
    "duration": 40.0,
    "section": "Procurement",
    "parents": [
      "Fitting"
    ],
    "resources": {
      "Materials": 4000.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Gaskets",
    "duration": 25.0,
    "section": "Procurement",
    "parents": [
      "Flanges"
    ],
    "resources": {
      "Materials": 1500.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Stud&Nuts",
    "duration": 15.0,
    "section": "Procurement",
    "parents": [
      "Gaskets"
    ],
    "resources": {
      "Materials": 1000.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Manual Valves",
    "duration": 90.0,
    "section": "Procurement",
    "parents": [
      "Stud&Nuts"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 3000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Actuated Valves",
    "duration": 120.0,
    "section": "Procurement",
    "parents": [
      "Manual Valves"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 10000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "ESD valves",
    "duration": 130.0,
    "section": "Procurement",
    "parents": [
      "Actuated Valves"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 8000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Flow Computer",
    "duration": 170.0,
    "section": "Procurement",
    "parents": [
      "Control Panel Logic",
      "P&ID"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 12000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "P/T Gauges",
    "duration": 25.0,
    "section": "Procurement",
    "parents": [
      "Flow Computer"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 900.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "P/T Transmitters",
    "duration": 60,
    "section": "Procurement",
    "parents": [
      "P/T Gauges"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 4000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Level Transmitter",
    "duration": 90.0,
    "section": "Procurement",
    "parents": [
      "P/T Transmitters"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 8000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Flow Orifices",
    "duration": 40.0,
    "section": "Procurement",
    "parents": [
      "Level Transmitter"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 1300.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "JBs Procurement",
    "duration": 25.0,
    "section": "Procurement",
    "parents": [
      "Flow Orifices"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 500.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Steelworks&support Material",
    "duration": 20.0,
    "section": "Procurement",
    "parents": [
      "JBs Procurement"
    ],
    "resources": {
      "Materials": 5000.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Structures Prefabbrication",
    "duration": 5.0,
    "section": "Construction",
    "parents": [
      "Steelworks&support Material"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 2000.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Painting Structures",
    "duration": 10.0,
    "section": "Construction",
    "parents": [
      "Structures Prefabbrication"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 7000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Piping Prefabbrication",
    "duration": 35.0,
    "section": "Construction",
    "parents": [
      "Painting Structures"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 14000.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pickling",
    "duration": 5.0,
    "section": "Construction",
    "parents": [
      "Piping Prefabbrication"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 3000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Painting Piping",
    "duration": 15.0,
    "section": "Construction",
    "parents": [
      "Painting Procedure"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 21000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Equipment",
    "duration": 1.0,
    "section": "Construction",
    "parents": [
      "Painting Piping"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Piping",
    "duration": 5.0,
    "section": "Construction",
    "parents": [
      "Equipment"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 2000.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Valves",
    "duration": 5.0,
    "section": "Construction",
    "parents": [
      "Piping"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 2000.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Instruments Installation",
    "duration": 5.0,
    "section": "Construction",
    "parents": [
      "Valves"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 5400.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "JBs Installation",
    "duration": 2.0,
    "section": "Construction",
    "parents": [
      "Instruments Installation"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 5400.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Cable & Cabletray Installation",
    "duration": 10.0,
    "section": "Construction",
    "parents": [
      "JBs Installation"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 5400.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Actuated Valve Setup",
    "duration": 2.0,
    "section": "Construction",
    "parents": [
      "Cable & Cabletray Installation"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 5400.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Tubing",
    "duration": 10,
    "section": "Construction",
    "parents": [
      "Actuated Valve Setup"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Pump Test",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Tubing"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Sterilizer&mineralizer Test",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Pump Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Filter Test",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Sterilizer&mineralizer Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Control Panel Test",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Filter Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Assembled Skid",
    "duration": 1.0,
    "section": "Testing",
    "parents": [
      "Control Panel Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "NDT on Weldings (Structure)",
    "duration": 1.0,
    "section": "Testing",
    "parents": [
      "Assembled Skid"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 100.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Dimensional Check (Structure)",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "NDT on Weldings (Structure)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 100.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Painting Check (Structure)",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Dimensional Check (Structure)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 100.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "NDT on Weldings (Piping)",
    "duration": 1.0,
    "section": "Testing",
    "parents": [
      "Painting Check (Structure)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 200.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Dimensional Check (Piping)",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "NDT on Weldings (Piping)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 200.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Hydrostatic Pressure Test",
    "duration": 3.0,
    "section": "Testing",
    "parents": [],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 200.0,
      "Internal Manpower": 1200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Painting Check (Piping)",
    "duration": 1.0,
    "section": "Testing",
    "parents": [
      "Hydrostatic Pressure Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Observer (Third Party)",
    "duration": 3.0,
    "section": "Testing",
    "parents": [
      "Painting Check (Piping)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 8000.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Dimensional Check (Observer)",
    "duration": 0.5,
    "section": "Testing",
    "parents": [
      "Observer (Third Party)"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "IECEx Detailed Test",
    "duration": 3.0,
    "section": "Testing",
    "parents": [
      "Automation Test",
      "Control Systems"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 1200.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Automation Test",
    "duration": 1.0,
    "section": "Testing",
    "parents": [],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Final Tests",
    "duration": 1.0,
    "section": "Testing",
    "parents": [
      "Automation Test"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 400.0,
      "Internal Engineering": 0.0
    }
  },
  {
    "name": "Documentation Pack",
    "duration": 2.0,
    "section": "Testing",
    "parents": [
      "Final Tests"
    ],
    "resources": {
      "Materials": 0.0,
      "External Engineering": 0.0,
      "Supplier": 0.0,
      "Internal Manpower": 0.0,
      "Internal Engineering": 1120.0
    }
  }
]

# load_tasks_from_csv.py

import pandas as pd

# Load the enriched CSV (assumed to be exported already)
df = pd.read_csv("final_task_comparison.csv")  # update with actual path if needed

# Fill NaNs with defaults
df.fillna({'Translated Dependencies': ''}, inplace=True)
df.fillna(0, inplace=True)

# Build the tasks list
tasks = []
for _, row in df.iterrows():
    task = {
        "name": row["Exported Task Name"],
        "duration": max(1, round(float(row["duration"]))),  # round and ensure min 1
        "section": row.get("Unnamed: 1", ""),  # or a default
        "parents": [p.strip() for p in row["Translated Dependencies"].split(",") if p.strip()],
        "resources": {
            "Materials": float(row.get("materials cost", 0)),
            "External Engineering": float(row.get("ext engineering", 0)),
            "Supplier": float(row.get("supplier", 0)),
            "Internal Manpower": float(row.get("manpower", 0)),
            "Internal Engineering": float(row.get("internal engineerign", 0)),
        }
    }
    tasks.append(task)

# Now `tasks` is ready for export or use
print(f"Loaded {len(tasks)} tasks from CSV.")

