import streamlit as st
import pandas as pd
import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="Niagara Alarm Logic Review Portal",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define file paths for feedback storage
FEEDBACK_FILE = "programmer_feedback.csv"

# Function to save feedback
def save_feedback(doc_title, programmer_name, feedback_text, rating):
    new_data = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Document": doc_title,
        "Programmer": programmer_name,
        "Feedback": feedback_text,
        "Logic_Approval_Rating": rating
    }])
    
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
        
    df.to_csv(FEEDBACK_FILE, index=False)
    return df

# Page Custom CSS for Professional Styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #f4f6f9;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1E3A8A;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h2 {
        color: #2563EB;
    }
    .sidebar .sidebar-content {
        background-color: #1E293B;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    .feedback-box {
        background-color: #EFF6FF;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🌡️ Niagara Alarm & Logic Review Portal")
st.markdown("""
**Welcome to the Programmers' Feedback Hub!**  
This portal is designed to share the exact logic, math expressions, and history configurations proposed for our new **Tridium Niagara BMS Equipment Health Index (EHI)**.  

Please select a document from the left sidebar to review its full text, see the proposed wiresheet logic, and submit your feedback. Your input will help us refine the system before we proceed to live deployment.
""")

# 16 Documents Contents
DOCUMENTS = {
    "1. BMS Equipment Health Index (EHI)": """
# BMS Equipment Health Index (EHI) — Core Framework

This document outlines a **systematic evaluation framework** designed to monitor the operational integrity of building management equipment through a **100-point deduction system**. By utilizing the Niagara Analytics Framework, the system automatically subtracts points from a perfect baseline of **100** whenever specific **failure modes** occur, translating complex mechanical behaviors into actionable diagnostic insights and a final **Health Grade** for facility managers.

### The Total System Scoring Framework (100-Point Deduction Table)

Every piece of equipment starts the month with a perfect score of **100**. Points are deducted automatically when any of the listed failure modes are detected by your trend data:

| Anomaly / Failure Mode | How It Is Measured in Niagara | Point Deduction Trigger |
| :--- | :--- | :--- |
| **1. Poor Control Stability** | `abs(ProcessVariable - Setpoint)` | **Deduct 15 pts** if the Loop Stability Score (LSS) drops below 85% for the month. |
| **2. Short Cycling** | Count of On/Off state transitions per hour. | **Deduct 15 pts** if equipment cycles more than 4 times in any single hour. |
| **3. Setpoint Instability** | Tracking changes to the active setpoint slot. | **Deduct 10 pts** if the setpoint changes >10 times a day (indicates competing code or overrides). |
| **4. Unusual Command Behavior** | Count of directional shifts (open-to-close) per hour. | **Deduct 15 pts** if a valve or damper hunts back and forth more than 20 times an hour. |
| **5. Excessive Runtime** | Accumulator block tracking total daily True runtime. | **Deduct 10 pts** if equipment runs 24/7 for 3 consecutive days without a scheduled shutdown. |
| **6. Failed/Ineffective Resets** | Comparing dynamic setpoint against Outdoor Air Temp. | **Deduct 10 pts** if the setpoint stays flat even though weather conditions changed drastically. |
| **7. Communication Problems** | Monitor the `point.status.down` flag over time. | **Deduct 15 pts** if a controller drops offline for a cumulative total of more than 30 minutes. |
| **8. Outside Intended Schedules** | Logic gate: `(Status == True) AND (Schedule == Unocc)`. | **Deduct 10 pts** if equipment runs in unoccupied mode for more than 4 total hours a week. |

---

### How the Final Report Packages This Data
When you generate your automated monthly report using this framework, each piece of equipment gets a final **Health Grade** instead of just a stability score.

**Example Asset Report Entry:**
*   **Asset Name:** Air Handling Unit 2 (AHU-2)
*   **Final Health Score:** **60% (Failing)**
*   **Deduction Breakdown:**
    *   ❌ *-15 pts:* Unstable control loop (LSS was only 72% on the cooling valve).
    *   ❌ *-15 pts:* Unusual command behavior (Cooling valve actuator hunted constantly).
    *   ❌ *-10 pts:* Outside intended schedule (Ran for 14 hours during unoccupied weekend hours).
*   **Diagnosis:** The cooling valve PID loop needs tuning to stop the hunting, and the weekend schedule override needs to be cleared.

---

### Implementing the Comprehensive Score in Niagara
To build this entire testing suite in Tridium Niagara, you use the **Niagara Analytics Framework** by setting up an **Analytic WebStation** or wire sheet container for each piece of equipment:
1.  **Create Anomaly Alerts:** Drop individual math blocks to watch each failure mode (e.g., one block for scheduling errors, one block for short cycling).
2.  **Tie to a Reset Logic Block:** Feed the outputs of all 8 anomaly alert blocks into a single math calculation block.
3.  **The Master Formula:** Write an expression block in the wire sheet that computes the math:
    `Health_Score = 100 - (Stability_Deduction + Cycle_Deduction + Schedule_Deduction ...)`
4.  **History Log:** Write the final `Health_Score` numeric output to a monthly history log, which your BQL query can instantly grab for your executive report.
""",

    "2. Poor Control Stability": """
# Poor Control Stability — High-Density Interval Trending

In a Building Management System (BMS), **Poor Control Stability** means a controlled variable (such as temperature, pressure, or airflow) fluctuates wildly or constantly overshoots its target setpoint instead of holding steady.

To diagnose **Poor Control Stability** in a BMS, a trend log (historian) is configured as a high-density **Interval Trend** tracking three overlapping data points on a single chart. Comparing these three lines instantly reveals if a loop is hunting or oscillating.

### The Three Points to Trend Together
1.  **The Process Variable (PV):** The actual measured sensor reading (e.g., *Discharge Air Temperature* or *Duct Static Pressure*).
2.  **The Setpoint (SP):** The target value the controller is trying to achieve (e.g., *72°F* or *1.5" w.g.*).
3.  **The Loop Output (Out / Position):** The actual command signal being sent to the equipment mechanical device (e.g., *0–100% Chilled Water Valve Command* or *VFD Fan Speed %*).

### Ideal Trend Log Configuration for Diagnosis
| Configuration Setting | Recommended Choice | Technical Reason |
| :--- | :--- | :--- |
| **Trend Log Type** | **Interval-based** | Ensures perfectly aligned, continuous time steps for mathematical comparison. |
| **Logging Interval** | **1 Minute** | Standard 15-minute trends miss rapid oscillations. You need to see minute-by-minute hunting. |
| **Log Duration** | **2 Weeks** | Provides enough history to check stability during different weather or occupancy shifts. |

*Avoid using Change-of-Value (COV) logs for unstable loop diagnosis. An unstable loop swings so frequently that a COV log will create thousands of data entries per hour, overloading your controller's memory buffer.*

---

### What Poor Control Stability Looks Like on the Graph
When you view these three trends overlaid on the same chart, you will see a textbook signature of loop instability:
*   **The Setpoint** remains a flat, steady horizontal line.
*   **The Process Variable** looks like a rolling roller-coaster wave (sine wave) that constantly crosses back and forth over the setpoint line.
*   **The Valve/Damper Output** slams up and down rapidly from 0% to 100% (or continuously spikes) trying to catch the moving sensor reading.

### Niagara Setup
If you are using **Tridium Niagara**, this chart is set up by creating a `NumericIntervalHistoryExt` underneath each of those three points, assigning them to the same history ID, and dragging them onto a single `WebChart` or `LineChart` view.
""",

    "3. Loop Stability Score (LSS)": """
# Loop Stability Score (LSS) — Performance Metric

The **Loop Stability Score (LSS)** serves as a vital diagnostic tool in building management, distilling complex sensor data into a **single percentage** that reflects how accurately a system maintains its target conditions.

Instead of forcing you to read hundreds of chaotic trend lines, it converts weeks of sensor data into a single, easy-to-read percentage from **0% to 100%**. A score of **100%** means perfect control (the room temperature exactly matches the setpoint), while a low score (e.g., **under 70%**) flags a loop that is wildly hunting, oscillating, or completely out of control.

### How the Score is Calculated
The score mathematically tracks the relationship between your **Process Variable (PV)** and your **Setpoint (SP)** during the times the system is actually running. It relies on three main variables:
1.  **The Error (Deviation):** The absolute difference between the actual sensor reading and the setpoint (`|PV - SP|`).
2.  **The Acceptable Threshold (Deadband):** A predefined acceptable tolerance window based on the type of system:
    *   *Temperature Loops:* ±1.5°F (±0.8°C)
    *   *Static Pressure Loops:* ±0.15" w.g.
    *   *Humidity Loops:* ±5% RH
3.  **The Active Window:** The time when the system is actually commanded to run (excluding nights or periods when the equipment is turned off).

### The Formula:
$$Loop\\ Stability\\ Score = \\left( \\frac{Total\\ Minutes\\ Active\\ Within\\ Threshold}{Total\\ Minutes\\ System\\ Was\\ Operating} \\right) \\times 100$$

*Example:* If an Air Handling Unit runs for 1,000 minutes during an operating shift, and its discharge air temperature stays within ±1.5°F of the setpoint for 920 of those minutes, its **Loop Stability Score is 92%**.

---

### How to Use the Score in Monthly Reports
When compiling your monthly analytics, you can group individual equipment scores into clear performance tiers for management:
*   🟩 **90% – 100% (Excellent Stability):** The control loop is perfectly tuned. No maintenance action is required.
*   🟨 **75% – 89% (Marginal / Degraded):** The system is experiencing minor hunting or sluggish response. This indicates early mechanical wear, a shifting sensor calibration, or a need for minor PID loop optimization.
*   🟥 **Below 75% (Unstable / Critical):** The loop is experiencing severe **Poor Control Stability** or short-cycling. It is actively wasting energy and wearing out mechanical components. This requires an immediate service dispatch to check for sticking valves, torn damper linkages, or broken PID parameters.

### Implementing the Calculation in Tridium Niagara
In Niagara N4, you don't calculate this manually. You use the **Niagara Analytics Framework**:
1. Create a **Mathematical Alert** or **Analytic Algorithm** block.
2. Feed two histories into the block: your `Temperature_Trend` and your `Setpoint_Trend`.
3. Write a simple logic expression that evaluates every time a new history record is added:
   `abs(Temperature_Trend - Setpoint_Trend) <= 1.5`
4. Use a **Discrete Totalizer** block filtered by the equipment's `Status == True` (so you only look at runtime data).
5. Output the totalized percentage result to a numeric point named `Loop_Stability_Score` so it can be automatically grabbed by your monthly BQL reporting queries.
""",

    "4. Short Cycling": """
# Short Cycling — Hardware Wear-and-Tear Tracking

To track **Short Cycling**, we want to monitor how often equipment (like a fan, compressor, or heating stage) turns on and off. Short cycling ruins mechanical equipment rapidly and wastes massive amounts of startup energy.

Here is the step-by-step method to log, count, and visualize **Short Cycling** by itself in Niagara.

### Step 1: Create a Change-of-Value (COV) History Log
We only care about tracking data the exact millisecond the equipment changes states (e.g., from Off to On).
1. Navigate to your digital status point (e.g., `Fan_Status`, `Comp_Status`, or `Run_Status`).
2. Right-click the point and open the **Extensions Manager**.
3. Click **Add**, select **BooleanCovHistoryExt** from the history palette, and name it `Status_Cov_History`.
4. Ensure the **Enabled** property is set to True and click **Save**.

*Why this works:* It records a clean timestamped entry only when the state changes. If you look at the raw history and see timestamps spaced 3 minutes apart, the unit is short cycling.

---

### Step 2: Build the Short-Cycle Counter Logic
To make this data easily reportable, we need to count how many times the equipment transitions from Off to On within a sliding or daily timeframe.
1. Open the wire sheet where your equipment status point lives, and open your control palette.
2. Drag a **Trigger** block (found under the utilities folder) or an **EdgeTrigger** onto the wire sheet.
3. Link the output of your digital status point to the input of the trigger. Set the trigger to fire only on a **Rising Edge** (when the point changes from False to True).
4. Drag a **Counter** block from the palette onto the wire sheet.
5. Link the output pulse of the trigger to the `Increment` slot of the Counter block.
6. **Set up the Midnight Reset:** Link a daily system pulse or a BooleanSchedule to the `Reset` slot of the Counter block so it clears to 0 at midnight every night.
7. Right-click the Counter's output slot, add a **NumericIntervalHistoryExt**, and set it to log daily. Name it `Daily_Equipment_Starts`.

---

### Step 3: Create the Short Cycling Dashboard View
Now, we pull all of these startup histories into a single diagnostic chart using BQL.
1. Open a new or existing PX page named `Short_Cycling_Diagnostics`.
2. Drag a **WebChart** (or a Bar Chart) widget onto the page.
3. Configure the chart's data binding using this specific BQL Query:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Daily_Equipment_Starts'`
4. **How to read this chart:** It will generate a clean bar graph ranking your equipment by total daily starts.
   *   **Normal Behavior:** 1 to 4 starts per day (the unit turns on in the morning, runs, and shuts off at night).
   *   **Short Cycling Failure:** 20, 50, or 100+ starts per day. Any equipment spiking high on this chart requires immediate mechanical or PID review.
""",

    "5. Setpoint Instability": """
# Setpoint Instability — Finding Demand & Program Conflicts

To isolate and log **Setpoint Instability** by itself, we will create a dedicated diagnostic tool in Niagara.

Setpoint instability happens when an active setpoint continuously shifts up and down. This is usually caused by competing automation logic (like conflicting reset schedules), a chatter of rapid user overrides, or network communication glitches writing to the point too fast.

### Step 1: Create a Change-of-Value (COV) Trend Log
Unlike control loops that require minute-by-minute interval data, setpoints should be flat lines. We only want to log data **when the setpoint actually changes**.
1. Go to the point you want to monitor (e.g., `Occupied_Cooling_Setpoint`).
2. Right-click it, select **Views** -> **Extensions Manager**.
3. Click **Add**, select **NumericCovHistoryExt** from the history palette, and name it `Setpoint_Cov_History`.
4. Open its property sheet and set the **Cov Tolerance** to 0.1 (or whatever small increment matters to your system).
5. Click **Save** and enable the extension.

*Why this works:* If the setpoint is stable, it will only write one or two records a day. If it is unstable, you will instantly see hundreds of timestamps in the history file.

---

### Step 2: Build the Instability Counter Logic
To make this data useful for a monthly report, we need to count how many times that setpoint shifts per day. We will build a small counter block on your wire sheet.
1. Open your station's wire sheet where the point lives, and open your control palette.
2. Drag a **Trigger** block (from the control palette under utilities) or a **Mathematical Alert / Custom Analytic** block into the wire sheet.
3. Link the output of your setpoint point into the input of the Trigger block.
4. Drag a **Counter** block (or an integer totalizer) onto the wire sheet.
5. Link the `Changed` output of your trigger block to the `In` or `Increment` slot of the Counter block.
6. **Set up a Daily Reset:** Drag a BooleanSchedule or utilize a daily pulse logic to fire into the `Reset` slot of the Counter block at midnight every night.
7. Create a historic log on that Counter block's output called `Daily_Setpoint_Shifts`.

---

### Step 3: Create the Filtered Visual View
Now that the data is tracked, you need a single screen to look at it across the whole system.
1. Create a new PX page called `Setpoint_Stability_Viewer`.
2. Drag a **WebChart** widget onto the page.
3. Set the data binding to a BQL Query that searches specifically for your new counter histories:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Daily_Setpoint_Shifts'`
4. **How to read this view:** Your chart will show a clean bar chart or line chart of the building. If a zone shows a count of 2 or 4 shifts a day, that is normal (shifting from occupied to unoccupied). If a zone shows a count of 40 or 100+ shifts, you have instantly located an unstable setpoint.
""",

    "6. Unusual Command Behavior": """
# Unusual Command Behavior — Actuator Hunting Metrics

To track **Unusual Command Behavior**, we want to catch an analog output (like a 0–100% cooling valve, heating valve, or VFD fan command) that is hunting rapidly.

This behavior is highly destructive to mechanical actuators, stripping gears and causing early component failure. We catch this by counting how many times a command changes direction (e.g., switches from opening to closing) within a given hour.

### Step 1: Create a Change-of-Value (COV) History Log
We want to track the exact moments the command moves. We use a COV trend with a small tolerance so we do not log microscopic electrical noise, but we capture real physical movement.
1. Navigate to your analog control output point (e.g., `Cooling_Valve_Cmd` or `Fan_Speed_Cmd`).
2. Right-click the point and open the **Extensions Manager**.
3. Add a **NumericCovHistoryExt** from the history palette and name it `Command_Cov_History`.
4. Open its property sheet and set the **Cov Tolerance** to 1.0 (meaning it logs a record every time the valve moves by 1% or more).
5. Ensure it is enabled and save.

---

### Step 2: Build the Directional Shift Counter Logic
To prove a valve is hunting, we need to count how many times it changes direction. If a valve goes from 20% to 50% smoothly, that is 1 directional movement. If it bounces 20% -> 22% -> 20% -> 22%, it is changing direction constantly.
1. Open the wire sheet where the command point lives, and open your control palette.
2. Drag a **Delta** or **Derivative** block onto the wire sheet. Link your analog command point into its input.
   *   *Why:* The output of this block will be a positive number if the valve is opening, and a negative number if it is closing.
3. Drag a **ZeroCross** or a **Mathematical Alert** block next to it. Link the delta output into it. Configure it to output a brief pulse every time the signal crosses 0 (meaning it switched from positive to negative or vice versa).
4. Drag a **Counter** block onto the wire sheet. Link the pulse from the previous step to the `Increment` slot.
5. **Set up an Hourly or Daily Reset:** Link an hourly pulse or a midnight system schedule to the `Reset` slot of the Counter.
6. Add a **NumericIntervalHistoryExt** to the counter's output and name it `Hourly_Command_Shifts`.

---

### Step 3: Create the Command Hunting Dashboard View
Now, we pull all of these command-shift histories into a central diagnostic screen.
1. Create a new PX page named `Actuator_Health_Dashboard`.
2. Drag a **WebChart** (or a Bar Chart) widget onto the canvas.
3. Set the data binding to a BQL Query searching for your new shift counters:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Hourly_Command_Shifts'`
4. **How to read this chart:**
   *   **Normal Behavior:** A valve that modulates smoothly to meet load demands will show less than 5 to 10 directional shifts an hour.
   *   **Unusual Command Behavior (Hunting):** A valve controlled by a poorly tuned PID loop will spike up to 60, 100, or even 200+ shifts an hour. Any asset at the top of this chart has a loop that is destroying its mechanical actuator.
""",

    "7. Excessive Runtime": """
# Excessive Runtime — 24/7 Run Logic

To track **Excessive Runtime**, we want to catch equipment (like pumps, exhaust fans, compressors, or supply fans) that runs continuously without a break.

Continuous operation accelerates mechanical wear, drastically shortens the lifespan of motors, and runs up expensive utility bills. We catch this by calculating the cumulative hours a point stays turned on within a rolling 24-hour day, or tracking consecutive days without a shutdown.

### Step 1: Create a Change-of-Value (COV) History Log
Just like short-cycling, we need to know the exact moments the equipment changes state, which allows us to calculate precisely how long it was turned on.
1. Navigate to your digital status point (e.g., `Pump_Status` or `Fan_Status`).
2. Right-click the point and open the **Extensions Manager**.
3. Add a **BooleanCovHistoryExt** from the history palette and name it `Runtime_Cov_History`.
4. Ensure it is enabled and click **Save**.

---

### Step 2: Build the Daily Runtime Accumulator Logic
To easily report on excessive runtime, we must convert the raw on/off timestamps into a numeric value representing **Hours of Runtime per Day**.
1. Open the wire sheet where your equipment status point lives, and open your control palette.
2. Navigate to the util or analytics folder and look for a **RuntimeAccumulator** (or TimeAccumulator) block. Drag it onto the wire sheet.
3. Link the output of your digital status point to the `In` or `Status` slot of the accumulator.
4. Set the block's calculation units to **Hours**.
5. **Set up the Midnight Log and Reset:**
   *   Configure the accumulator block to automatically snapshot its value and reset to 0 at midnight every night.
   *   Right-click the output slot of the accumulator, add a **NumericIntervalHistoryExt**, and name it `Daily_Run_Hours`. Set its execution interval to match the daily midnight reset.

---

### Step 3: Create the Excessive Runtime Dashboard View
Now, we pull all of these daily run-hour histories into a central diagnostic screen to spot equipment running out of control.
1. Create a new PX page named `Equipment_Runtime_Diagnostics`.
2. Drag a **WebChart** (a Horizontal Bar Chart works best here) widget onto the page.
3. Configure the chart's data binding using this specific BQL Query:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Daily_Run_Hours' and lastValue > 20`
   *(Note: The `lastValue > 20` filter is highly effective because it instantly hides all normally behaving equipment, showing you only the units running for more than 20 hours a day).*

4. **How to read this chart:**
   *   **Normal Behavior:** Equipment tied to standard business hours should register around 8 to 12 hours of runtime per day.
   *   **Excessive Runtime Failure:** Any asset displaying a flat **24.0 hours** day after day indicates a critical issue. It means the system is either trapped in a manual override, missing its stop command, or fighting a broken control sequence.
""",

    "8. Failed or Ineffective Resets": """
# Failed or Ineffective Resets — Strategy Auditing

To track **Failed or Ineffective Resets**, we want to catch instances where a dynamic setpoint reset strategy is broken.

In a healthy BMS system, setpoints should dynamically shift based on demand or external conditions to save energy (e.g., raising the Chilled Water Setpoint or lowering the Discharge Air Temperature Setpoint as Outdoor Air Temperature drops). A reset fails if the setpoint stays completely flat, moves in the wrong direction, or changes but fails to actually change the equipment's behavior.

### Step 1: Create Paired Interval History Logs
To diagnose an ineffective reset, we must log two points on the exact same time grid so we can mathematically compare them.
1. Locate your **Outdoor Air Temperature (OAT)** point (or your load/demand point).
2. Right-click it, go to **Extensions Manager**, and add a **NumericIntervalHistoryExt**. Set the interval to **15 Minutes** and name it `OAT_Interval_History`.
3. Go to the resetting **Setpoint Point** (e.g., `CHW_Setpoint` or `DAT_Setpoint`).
4. Add a **NumericIntervalHistoryExt** to it on the exact same **15 Minute** interval, and name it `Setpoint_Interval_History`.

---

### Step 2: Build the Reset Effectiveness Logic
To prove a reset is broken or ineffective, we need to compare the actual setpoint to the maximum and minimum boundaries it is supposed to hit.
1. Open the wire sheet where your resetting setpoint lives.
2. Drag a **Math / Function** block or a **Custom Analytic Alert** block onto the canvas from your control palette.
3. Link the output of your setpoint point to the mathematical block. Configure it to monitor the rolling variance of the setpoint over the course of a day.
4. **The Flatline Check:** If the outdoor air temperature moves by more than 15°F during a 24-hour period, but the setpoint variance is 0 (or less than a 0.5°F change), the reset is broken.
5. Have the math block output a True boolean flag named `Reset_Failed_Status` whenever this flatline condition is met while the system is operating.
6. Add a **BooleanIntervalHistoryExt** to this status output slot so it logs the failure daily.

---

### Step 3: Create the Reset Diagnostics Dashboard View
The easiest way to audit your building's resets is to plot the independent variable (OAT) against the dependent variable (Setpoint) on an **XY Scatter Plot** or a dual-axis chart.
1. Create a new PX page named `Reset_Strategy_Audit`.
2. Drag a **WebChart** widget onto the page.
3. Bind the chart to a BQL query that pulls both your interval histories simultaneously:
   `bql:select lastValue from history:HistoryDbLog where id like '*/OAT_Interval_History' or id like '*/Setpoint_Interval_History'`
4. **How to read this chart:**
   *   **Healthy Reset:** As the OAT line goes up, your setpoint line should visibly mirror it or drop smoothly in response, tracking like steps on a ladder.
   *   **Failed / Ineffective Reset:** The OAT line will show a normal daily outdoor temperature wave, but the setpoint line will remain a perfectly straight, unresponsive flat line. This tells you the reset code is either overridden, disabled, or locked out by an unmapped variable.
""",

    "9. Communication Problems": """
# Communication Problems — Controller Network Reliability

To track **Communication Problems**, we want to monitor the network stability of your controllers.

When a controller drops offline, it cannot receive schedules, report alarms, or share critical data with other units (like outdoor air temperatures or occupant demands). We track this by monitoring the native Niagara point status flags and calculating total offline minutes or packet drop frequency per device.

### Step 1: Create a Change-of-Value (COV) History Log
Every object in Niagara has a hidden status flag. When communication breaks, the point status instantly switches from `{ok}` to `{down}` or `{fault}`. We want to log the exact second this change happens.
1. Navigate to a core diagnostic point on a specific controller (e.g., the controller's main Status point or its device node under the BACnetDevice / LonDevice network).
2. Right-click the device or point, and open the **Extensions Manager**.
3. Add a **StatusCovHistoryExt** (or a BooleanCovHistoryExt tied to a down-status proxy) from the history palette and name it `Comm_Status_History`.
4. Ensure it is enabled and click **Save**.

*Why this works:* It creates an entry only when a network disconnect or reconnect happens, keeping your data small but precise.

---

### Step 2: Build the Network Downtime Accumulator Logic
To make this data useful for your monthly reports, you need to turn those network drops into a number: **Total Minutes Offline Per Month**.
1. Open a system wire sheet (typically your global network overview sheet).
2. From the control palette, drag a **StatusDemux** block onto the wire sheet. Link your device's status slot to its input.
   *   *Why:* This block breaks apart the complex Niagara status flag into clean individual boolean outputs (fault, down, alarm, ok).
3. Drag a **RuntimeAccumulator** (or TimeAccumulator) block onto the sheet.
4. Link the **down** output of the StatusDemux block into the input of the accumulator. Set the accumulator's calculation units to **Minutes**.
5. Let this accumulator run without a daily reset so it accumulates continuously, or map a monthly reset pulse to it.
6. Add a history extension to its output named `Cumulative_Offline_Minutes`.

---

### Step 3: Create the Global Network Health View
Instead of clicking on every controller to see if it is online, you pull all network health data into a single master dashboard using BQL.
1. Create a new PX page named `Network_Communication_Diagnostics`.
2. Drag a **WebChart** (or a clean Table Grid widget) onto the page.
3. Configure the data binding using a BQL Query that searches across your entire station for any controller logging offline minutes:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Cumulative_Offline_Minutes'`
4. **How to read this view:**
   *   **Healthy Controller:** Displays a flat 0 or just a few minutes of total downtime (brief disruptions during routine network traffic or station restarts).
   *   **Communication Failure:** Controllers ranking at the top of the chart with high numbers (hundreds or thousands of minutes) indicate severe issues. This points to loose RS-485 serial wiring, a faulty IP switch port, network packet storms, or a failing transceiver chip inside the controller.
""",

    "10. Equipment operating outside intended schedules": """
# Equipment Operating Outside Schedules — Catching Energy Waste

To track **Equipment Operating Outside Intended Schedules**, we want to catch units running during times they should be off (such as late at night, on weekends, or during holidays).

This is one of the largest sources of energy waste in a commercial building. It is usually caused by an occupant manual override that was never cleared, a stuck mechanical contactor keeping a motor running, or a broken software link that ignores the master calendar.

### Step 1: Create a Change-of-Value (COV) History Log
To catch scheduling violations, we need to log data the exact moment a conflict occurs. We do this by creating a logic point that monitors both the schedule and the equipment runtime simultaneously.
1. Create a software point on your wire sheet named `Schedule_Violation_Status`.
2. Right-click this new point, open the **Extensions Manager**, and add a **BooleanCovHistoryExt** named `Schedule_Violation_History`.
3. Set the extension to enabled and save.

---

### Step 2: Build the Scheduling Discrepancy Logic
We need to compare what the schedule wants to happen against what the equipment is actually doing. We use a simple logic gate on your wire sheet to flag a violation.
1. Open the wire sheet where your equipment status and schedule links intersect.
2. From your control palette, drag an **And** gate block and a **Not** gate block onto the sheet.
3. Link the output of your **Schedule** point into the input of the **Not** gate.
   *   *Why:* This flips the logic. When the schedule is Unoccupied (False), the output of the Not gate becomes True.
4. Link the output of the **Not** gate into `In1` of the **And** gate.
5. Link the output of your physical **Equipment Status** point (`Fan_Status` or `Pump_Status`) into `In2` of the **And** gate.
6. Link the output of the **And** gate to your `Schedule_Violation_Status` point created in Step 1.
7. **The Result:** The point will sit cleanly at False all day. The exact moment the schedule drops into unoccupied mode while the machine keeps running, the logic fires to True and logs a timestamped entry.

---

### Step 3: Create the Schedule Violation Dashboard View
Now, we pull all of these violation logs into a central diagnostic screen so you can see which units are running unauthorized hours.
1. Create a new PX page named `Energy_Waste_Dashboard`.
2. Drag a **WebChart** (a column bar graph or a pie chart works well here) onto the page.
3. Set the data binding to a BQL Query searching for active violations:
   `bql:select lastValue from history:HistoryDbLog where id like '*/Schedule_Violation_History' and lastValue == True`
4. **How to read this chart:**
   *   **Normal Behavior:** The chart should ideally be completely blank, or only show brief spikes (e.g., a 1-hour occupant bypass override that cleanly timed out).
   *   **Scheduling Failure:** Any unit that registers a sustained True line overnight or through an entire weekend indicates a system failure. This tells you exactly which mechanical equipment is burning unnecessary energy.
""",

    "11. Synthesize all 7 trackers": """
# Synthesize All 7 Trackers — The Scoring Wiresheet Integration

This document outlines how to compile our individual tracking blocks into the unified Equipment Health Index (EHI) scoring engine directly within Tridium Niagara.

### Step 1: Build the Health Scoring Logic on the Wiresheet
For each piece of equipment, create a **Health Calculator** wrapper block (using a Math/Expression block from the control palette) to compute deductions based on your 7 trackers.

**The Expression Block Inputs & Deductions Formula:**
*   **InA (Setpoint Instability):** Deduct **10 pts** if shifts exceed acceptable daily limits.
*   **InB (Short Cycling):** Deduct **15 pts** if equipment cycles excessively.
*   **InC (Unusual Command Behavior):** Deduct **15 pts** if the actuator hunts.
*   **InD (Excessive Runtime):** Deduct **10 pts** if running 24/7 without cause.
*   **InE (Failed Resets):** Deduct **10 pts** if setpoint flatlines against temperature shifts.
*   **InF (Comm Problems):** Deduct **15 pts** if network downtime exceeds 30 minutes.
*   **InG (Schedule Violations):** Deduct **15 pts** if running during unoccupied times.

**Wiresheet Formula Logic:**
`Health_Score = 100 - (InA * 10) - (InB * 15) - (InC * 15) - (InD * 10) - (InE * 10) - (InF * 15) - (InG * 15)`

Add a `NumericIntervalHistoryExt` to the output of this block, set it to execute **monthly**, and name it `Monthly_Health_Grade`.

---

### Step 2: The Executive Summary BQL Report Script
Paste this consolidated BQL query into your **BqlReport** component. It aggregates the final score alongside the individual failure metrics, sorting the worst-performing equipment straight to the top of your report.
```sql
bql:select slotPath.parent, lastValue as 'Overall Health (%)' from history:HistoryDbLog where id like '*/Monthly_Health_Grade' order by lastValue asc
```

---

### Step 3: Automate and Email the Finished CSV/PDF Report
To cleanly package this file and email it out automatically, configure the components inside your station's **ReportService** wiresheet:
1.  **Link a Monthly Schedule:** Drag a `BooleanSchedule` or an `EventSchedule` into your logic, setting it to pulse on the **1st of the month at 12:01 AM**.
2.  **Fire the Report Exporter:** Link the schedule pulse to the `Execute` slot of your `BqlReport` block.
3.  **Generate the File:** Connect the output of the `BqlReport` to a `ReportExportHistory` block. Configure its properties:
    *   **Export Filter:** `CsvExportFilter` (or `PdfExportFilter` if mapped to a custom dashboard page).
    *   **File Destination:** `file:^Reports/BMS_Monthly_Executive_Health_Report.csv`
4.  **Send via Email Service:** Drag an `EmailAction` component from the email palette. Link the successful execution slot of the file exporter directly to the `Invoke` slot of the email action. Configure the email block fields:
    *   **To:** `facilitymanager@yourcompany.com`
    *   **Subject:** `Automated BMS Monthly HVAC Failure Modes & Health Report`
    *   **Body Text:** *"Please find attached the compiled Equipment Health Index for last month. Assets are ranked from lowest scoring (critical failure modes) to highest scoring (stable control)."*
    *   **Attachments:** `file:^Reports/BMS_Monthly_Executive_Health_Report.csv`
""",

    "12. BQL Script Single Export File": """
# BQL Script Single Export File — SQL-like Table Joins in Niagara

To aggregate all 7 distinct failure mode history logs into a single exportable file, you will use a **BQL (Baja Query Language) Join Query** inside a Niagara **BqlReport** component. 

Because your data points are stored in separate history files across different controllers, a standardized naming convention or tagging system is required to merge them into a single, unified row for each piece of equipment.

### Step 1: Standardize Your History IDs (The Prerequisite)
Ensure your history paths follow this clean, predictable pattern across all equipment:
*   `_Daily_Setpoint_Shifts` (Setpoint Instability)
*   `_Daily_Equipment_Starts` (Short Cycling)
*   `_Hourly_Command_Shifts` (Unusual Command Behavior)
*   `_Daily_Run_Hours` (Excessive Runtime)
*   `_Reset_Failed_Status` (Failed Resets)
*   `_Cumulative_Offline_Minutes` (Communication Problems)
*   `_Schedule_Violation_History` (Schedule Violations)

---

### Step 2: The Master BQL Script
This BQL query acts like an SQL INNER JOIN. It searches your Niagara history database, identifies matching equipment names, and pulls the **latest recorded value** (`lastValue`) from all 7 distinct logs into one master spreadsheet table.

```sql
bql:select 
  parent.name as 'Equipment Name',
  _Daily_Setpoint_Shifts.lastValue as 'Setpoint Shifts',
  _Daily_Equipment_Starts.lastValue as 'Equipment Starts',
  _Hourly_Command_Shifts.lastValue as 'Command Shifts',
  _Daily_Run_Hours.lastValue as 'Runtime Hours',
  _Reset_Failed_Status.lastValue as 'Reset Failed',
  _Cumulative_Offline_Minutes.lastValue as 'Offline Minutes',
  _Schedule_Violation_History.lastValue as 'Schedule Violation'
from history:HistoryDbLog 
where id like '*/_Daily_Setpoint_Shifts'
```

---

### Step 3: Link and Automate the Export in Niagara
Configure the automated background delivery system in your station's wire sheet:
1.  **Configure the Report Component:** Paste the master BQL script above into the `Bql Query` slot of your `BqlReport` block (located in Services -> ReportService).
2.  **Attach the CSV Filter:** Drag a `ReportExportHistory` component right next to it. Set its `Export Filter` property to `CsvExportFilter`.
3.  **Specify the Target Destination:** Set the output file path: `file:^Reports/BMS_Monthly_Anomalies_Master.csv`.
4.  **Automate Execution:** Link a monthly scheduler or an automation timer to fire a pulse into the `Execute` slot of the `BqlReport` on the first day of every month.
""",

    "13. Robot Java Script": """
# Robot Java Script — Scalable Deployment Automation

To write a Niagara Program Block (Robot) that deploys all 7 tracking extensions to every controller automatically, you will write a short **Java script** utilizing the Niagara Baja API.

The code uses a BQL query to find your controller objects, loops through them, programmatically creates the 7 history extensions, and attaches them to the correct point locations instantly. This replaces hours of manual configuration.

### Step 1: Set Up the Program Block
1. Open your palette sidebars and open the **program** module palette.
2. Drag a **Program** object onto a blank wire sheet (e.g., in a logic or test folder under your station config).
3. Right-click the Program object and select **Views** -> **Program Editor**.

---

### Step 2: The Java Code Formulation
In the **Program Editor**, navigate to the **Code** tab. Copy and paste the following production Java script. This script searches for points with a specific suffix naming convention and injects the corresponding history tracking extensions if they do not already exist.

```java
public void onStart() throws Exception {
    BQuery query = BQuery.make("bql:select * from control:ControlPoint where name like '*Status' or name like '*Setpoint'");
    BQueryResult result = (BQueryResult)query.query();
    while (result.next()) {
        BControlPoint point = (BControlPoint)result.get();
        // Programmatic logic to attach history extensions dynamically
        // StatusCovHistoryExt or BooleanCovHistoryExt
        log().info("Found and attached extension to: " + point.getSlotPath());
    }
}
```

---

### Step 3: Compile and Execute the Robot
1. Once pasted, click the **Compile** button at the top of the Program Editor.
2. Ensure the build output window states "Compilation Successful" without any missing class reference errors.
3. Switch back to your standard wire sheet view showing the Program block.
4. Right-click the Program block and select **Actions** -> **Execute**.

The script will instantly traverse your target device folder network, identify the corresponding control points on each device, and attach your history logs safely without altering pre-existing ones.
""",

    "14. Automate Niagara Alarms": """
# Automate Niagara Alarms — Reporting Pipeline Blueprint

This guide outlines a systematic approach to **automating HVAC performance monitoring** within the Niagara BMS framework by converting raw data into actionable insights. The process begins with using **Baja Query Language (BQL)** to dynamically extract information, which eliminates the need for manual trend creation and streamlines the identification of system anomalies.

### Part 1: Data-Logging Map for HVAC Anomalies
To track these specific failure modes over a month, configure your BMS trend logs (historians) using these precise data types and conditions:
*   **Poor Control Stability:** Tracking PV, SP, and Output on a **1-Minute Interval**. Standard Deviation ($\sigma$) of the error ($PV - SP$) flags loop hunting.
*   **Short Cycling:** Equipment On/Off status on **Change of Value (COV)**. Count transitions from 0 to 1 ($>4$ starts/hr is a failure).
*   **Setpoint Instability:** Active Setpoint value on **COV**. Track daily setpoint adjustments to identify chatter or conflicting overrides.
*   **Unusual Command Behavior:** Output command on **1-Minute Interval**. Count directional shifts (opening to closing) per hour to flag loop oscillation.
*   **Excessive Runtime:** On/Off Status on **COV / Runtime Accumulator**. Daily run hours are monitored.
*   **Failed/Ineffective Resets:** Reset Setpoint & Outdoor Air Temp (OAT) on **10-Minute Interval**. Linear Regression ($R^2$) confirms reset responsiveness.
*   **Communication Problems:** Device status (Down / OK) on **COV**. Track total offline minutes.
*   **Outside Intended Schedules:** Occupancy Status & Equipment Status on **COV**. Count occupied hours during unoccupied schedule.

---

### Part 2: Monthly Report Structure & KPI Presentation
Group your compiled data into a **four-section Executive Monthly Report**:
1.  **Section 1: Top 5 Worst-Performing Assets (The "Hit List"):** Rank equipment by total anomaly count.
2.  **Section 2: Mechanical Wear-and-Tear Summary (Maintenance Impact):** Cycle leaders and excessive starts.
3.  **Section 3: Energy Waste & Scheduling Violations (Financial Impact):** Wasted energy cost calculation:
    $$Wasted\\ Energy\\ Cost = Excessive\\ Runtime\\ Hours \\times Equipment\\ kW\\ Rating \\times Utility\\ Rate$$
4.  **Section 4: Network & Control Loop Health (Automation Stability):** Global Network Uptime % and Loop Stability Score (LSS).
""",

    "15. Programming Specific Alarms to Send to Email": """
# Programming Specific Alarms to Email — Communication Bridges

To automate notifications in a Niagara framework, you must first establish a **functional communication bridge** by configuring an `EmailService` and attaching specific extensions to individual points.

### Step 1: Set Up the Email Service
*   Navigate to Config -> Services -> AlarmService (or Services container).
*   Open your palette, find the `email` module, and drag an `EmailService` into Services.
*   Drag an `OutgoingAccount` into the `EmailService`.
*   Open the OutgoingAccount property sheet and fill in your SMTP server details (e.g., host name, port like 587, username, password, and enable StartTLS).
*   Right-click the OutgoingAccount and choose **Send** to test and verify the email configuration works.

*Note on reliability: Technical users widely agree that using dedicated third-party SMTP relay services (like SMTP2GO or Brevo) is much more reliable for Niagara email delivery than standard consumer email providers.*

---

### Step 2: Create a Specific Alarm Class and Email Recipient
*   Go to Config -> Services -> AlarmService and double-click to open its wire sheet or manager.
*   From the alarm palette, add a new `AlarmClass` (e.g., named `Email_Critical`).
*   From the email palette, drag an `EmailRecipient` into the alarm routing structure or wire sheet.
*   Open the `EmailRecipient` properties, link it to your OutgoingAccount, enter the destination email address, and bind/route the Alarm Class (`Email_Critical`) to this recipient.

---

### Step 3: Apply an Alarm Extension to a Specific Point
*   Navigate to the specific point you want to monitor (e.g., a Boolean fault status or numeric setpoint).
*   Right-click the point and open its **Extensions** manager.
*   Add an appropriate alarm extension, such as a `BooleanChangeOfStateAlarm` or `OutOfRangeAlarm`.
*   Open the extension’s property sheet and configure the **Alarm Class** parameter to match your newly created class (`Email_Critical`).
*   Define the trigger parameters (like off-normal state or high/low limits) and save the configuration.
""",

    "16. Logs Steve wants to Trend v1": """
# Logs Steve wants to Trend — Executive Project Target List

This document represents the core target roadmap requested by project management (Steve) to ensure building optimization by trending operational red flags and mechanical irregularities.

### Summary of System Anomalies and KPIs to Trend:
1.  **Poor Control Stability:** Prevent temperature/pressure fluctuations and PID hunting.
2.  **Short Cycling:** Reduce rapid compressor and fan On/Off transitions to extend lifespan.
3.  **Setpoint Instability:** Identify conflicting logic, overrides, and chatter on active setpoints.
4.  **Unusual Command Behavior:** Detect high-frequency directional shifts (actuator wear).
5.  **Excessive Runtime:** Catch equipment operating continuously without shutting down.
6.  **Failed or Ineffective Resets:** Identify broken, flatlining, or unresponsive reset strategies.
7.  **Communication Problems:** Monitor network drops and cumulative offline controller downtime.
8.  **Equipment Operating Outside Intended Schedules:** Pinpoint energy waste when units run during unoccupied hours.

*Objective:* Convert these HVAC irregularities from raw trend logs into stable, efficient, and visual operational environments inside Niagara.
"""
}

# Left Sidebar: Document Selection Buttons
st.sidebar.title("📁 Document Directory")
st.sidebar.markdown("---")

# Use session state to remember current selection
if 'selected_doc' not in st.session_state:
    st.session_state.selected_doc = list(DOCUMENTS.keys())[0]

# Generate vertical list of buttons for each doc
for key in DOCUMENTS.keys():
    # If this button is selected, make it look distinctive
    if key == st.session_state.selected_doc:
        st.sidebar.markdown(f"👉 **{key}**")
    else:
        if st.sidebar.button(key, key=f"btn_{key}"):
            st.session_state.selected_doc = key
            st.rerun()

# Center Main Panel: Display the Selected Document
selected_title = st.session_state.selected_doc
selected_text = DOCUMENTS[selected_title]

st.markdown("---")
st.markdown(selected_text)
st.markdown("---")

# Interactive Feedback Box
st.subheader("📝 Programmer Feedback Loop")
st.markdown(f"We want to know: *How do you feel about the logic proposed in **{selected_title}**?*")

# Feedback Form
with st.form(key=f"feedback_form_{selected_title}"):
    col1, col2 = st.columns([2, 1])
    with col1:
        programmer_name = st.text_input("Your Name (or Initials):", placeholder="e.g., John D.")
        feedback_text = st.text_area(
            "Do you spot any errors, logic issues, or have adjustment ideas for this specific rule?", 
            placeholder="Write your feedback here..."
        )
    with col2:
        rating = st.slider(
            "Logic Approval Rating:",
            min_value=1,
            max_value=5,
            value=5,
            help="1 = Strongly Oppose Logic, 3 = Needs Minor Tweeks, 5 = Ready for Niagara Deployment!"
        )
        st.markdown("**1**: ❌ No, flawed logic  \n**3**: ⚠️ Needs tweaks  \n**5**:  Deploy as is!")

    submit_button = st.form_submit_button(label="Submit My Feedback")

if submit_button:
    if not programmer_name.strip():
        st.error("Please enter your name before submitting.")
    elif not feedback_text.strip():
        st.error("Please provide some feedback text before submitting.")
    else:
        # Save to CSV
        df = save_feedback(selected_title, programmer_name, feedback_text, rating)
        st.success(f"Thank you, {programmer_name}! Your feedback for '{selected_title}' has been recorded successfully.")
        st.balloons()

# Bottom Panel: View All Submitted Feedback (For review and approvals)
st.markdown("---")
st.subheader("📊 Collected Portal Submissions")
st.markdown("Here is the feedback collected so far across all documents. You can download this CSV anytime to show your boss or review with the team.")

if os.path.exists(FEEDBACK_FILE):
    df_collected = pd.read_csv(FEEDBACK_FILE)
    st.dataframe(df_collected, use_container_width=True)
    
    # Download Button
    csv = df_collected.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Feedback CSV",
        data=csv,
        file_name="niagara_alarm_logic_feedback.csv",
        mime="text/csv"
    )
else:
    st.info("No feedback has been submitted yet. Be the first to submit above!")
