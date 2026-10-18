import html
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd

from src.server_models import ServerHardware
from src.server_diagnostics import diagnose_server
from src.repair_workflow import repair_and_retest
from src.repair_history import save_repair_record, load_repair_history


st.set_page_config(
    page_title="RACK//OPS | Infrastructure Diagnostics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# SIMULATED SERVER INVENTORY
# --------------------------------------------------

def create_simulated_servers():

    return [
        ServerHardware(
            rack_id="LAB-RACK-001",
            server_model="SIMULATED-X86",
            cpu_temperature=65,
            memory_utilization=55,
            disk_temperature=40,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=True,
        ),
        ServerHardware(
            rack_id="LAB-RACK-002",
            server_model="SIMULATED-X86",
            cpu_temperature=95,
            memory_utilization=55,
            disk_temperature=40,
            disk_healthy=False,
            power_supply_healthy=False,
            network_connected=True,
        ),
        ServerHardware(
            rack_id="LAB-RACK-003",
            server_model="SIMULATED-X86",
            cpu_temperature=70,
            memory_utilization=95,
            disk_temperature=75,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=False,
        ),
    ]


# --------------------------------------------------
# VISUAL DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(34, 211, 238, 0.09),
                transparent 35%
            ),
            #080F1D;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #E6EDF7;
        letter-spacing: -0.025em;
    }

    [data-testid="stSidebar"] {
        background: #0D1727;
        border-right: 1px solid #223249;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #142238,
            #0C1728
        );
        border: 1px solid #263A54;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    [data-testid="stMetricLabel"] {
        color: #8EA5BF;
    }

    [data-testid="stMetricValue"] {
        color: #F1F7FF;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263A54;
        border-radius: 12px;
        overflow: hidden;
    }

    .brand {
        font-size: 2.3rem;
        font-weight: 850;
        letter-spacing: -0.06em;
        color: #F0F7FF;
    }

    .brand span {
        color: #22D3EE;
    }

    .eyebrow {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        color: #22D3EE;
        margin-bottom: 8px;
    }

    .subtitle {
        color: #8EA5BF;
        font-size: 0.95rem;
        margin-bottom: 22px;
    }

    .status-pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 20px;
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: #86EFAC;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .rack-scene {
        perspective: 900px;
        padding: 35px 20px 45px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 370px;
        background:
            radial-gradient(
                ellipse at center,
                rgba(34, 211, 238, 0.08),
                transparent 65%
            );
        border: 1px solid #243750;
        border-radius: 18px;
    }

    .rack {
        width: 245px;
        padding: 18px;
        background: linear-gradient(
            110deg,
            #1B2C43,
            #0C1524 65%
        );
        border: 7px solid #354961;
        border-radius: 10px;
        box-shadow:
            18px 18px 0 #07101C,
            25px 28px 35px rgba(0,0,0,0.6),
            inset 0 0 18px rgba(0,0,0,0.6);
        transform: rotateY(-13deg) rotateX(3deg);
    }

    .rack-header {
        font-size: 0.65rem;
        letter-spacing: 0.18em;
        color: #8EA5BF;
        text-align: center;
        margin-bottom: 15px;
    }

    .server-unit {
        background: linear-gradient(
            180deg,
            #263A53,
            #142135
        );
        border: 1px solid #46607B;
        border-radius: 5px;
        padding: 14px 12px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 10px rgba(0,0,0,0.35);
    }

    .server-name {
        font-size: 0.68rem;
        font-weight: 700;
        color: #D8E7F8;
    }

    .server-led {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        box-shadow: 0 0 10px currentColor;
    }

    .led-green {
        background: #22C55E;
        color: #22C55E;
    }

    .led-red {
        background: #EF4444;
        color: #EF4444;
    }

    .led-amber {
        background: #F59E0B;
        color: #F59E0B;
    }

    .panel {
        background: #101C2E;
        border: 1px solid #263A54;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .panel-title {
        font-size: 0.75rem;
        letter-spacing: 0.13em;
        color: #8EA5BF;
        margin-bottom: 10px;
    }

    .panel-value {
        font-size: 1.25rem;
        font-weight: 750;
        color: #F1F7FF;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# DATA
# --------------------------------------------------

if "servers" not in st.session_state:
    st.session_state.servers = create_simulated_servers()

servers = st.session_state.servers
results = [diagnose_server(server) for server in servers]

server_lookup = {
    server.rack_id: server
    for server in servers
}


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand">RACK<span>//</span>OPS</div>',
        unsafe_allow_html=True,
    )

    st.caption("INFRASTRUCTURE OPERATIONS")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Hardware Diagnostics",
            "Repair & Retest",
            "Repair History",
        ],
    )

    st.divider()

    st.markdown(
        '<span class="status-pill">● SIMULATION ACTIVE</span>',
        unsafe_allow_html=True,
    )

    st.caption("Synthetic hardware telemetry")
    st.caption("Python 3.11 | Streamlit")


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="eyebrow">INFRASTRUCTURE VALIDATION PLATFORM</div>',
    unsafe_allow_html=True,
)

st.title("Server Validation & Debug Automation")

st.markdown(
    '<div class="subtitle">'
    'Hardware diagnostics, simulated repairs, and validation intelligence.'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    total = len(results)
    healthy = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    critical = sum(r["severity"] == "CRITICAL" for r in results)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("TOTAL SERVERS", total)
    c2.metric("HEALTHY", healthy)
    c3.metric("FAILED", failed)
    c4.metric("CRITICAL", critical)

    st.write("")

    left, right = st.columns([1.2, 1])

    with left:

        st.subheader("Server Rack Visualization")

        rack_units = ""

        for result in results:
            severity = result["severity"]

            led_class = {
                "HEALTHY": "led-green",
                "WARNING": "led-amber",
                "CRITICAL": "led-red",
            }.get(severity, "led-amber")

            rack_id = html.escape(result["rack_id"])

            rack_units += (
                '<div class="server-unit">'
                f'<span class="server-name">{rack_id}</span>'
                '<span class="server-vents"></span>'
                f'<span class="server-led {led_class}"></span>'
                '</div>'
            )

        rack_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .rack-scene {{
                perspective: 900px;
                min-height: 390px;
                padding: 35px;
                display: flex;
                justify-content: center;
                align-items: center;
                background: radial-gradient(
                    ellipse at center,
                    rgba(34, 211, 238, 0.08),
                    transparent 70%
                );
                border: 1px solid #243750;
                border-radius: 18px;
            }}

            .rack {{
                width: 260px;
                padding: 20px;
                background: linear-gradient(
                    110deg,
                    #1B2C43,
                    #0C1524 65%
                );
                border: 7px solid #354961;
                border-radius: 10px;
                box-shadow:
                    18px 18px 0 #07101C,
                    25px 28px 35px rgba(0,0,0,0.6),
                    inset 0 0 18px rgba(0,0,0,0.6);
                transform: rotateY(-13deg) rotateX(3deg);
            }}

            .rack-header {{
                font-size: 10px;
                letter-spacing: 2px;
                color: #8EA5BF;
                text-align: center;
                margin-bottom: 20px;
            }}

            .server-unit {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 16px 12px;
                margin-bottom: 14px;
                background: linear-gradient(
                    180deg,
                    #293E57,
                    #142135
                );
                border: 1px solid #46607B;
                border-radius: 5px;
                box-shadow:
                    0 5px 12px rgba(0,0,0,0.4),
                    inset 0 1px rgba(255,255,255,0.08);
            }}

            .server-name {{
                color: #D8E7F8;
                font-size: 11px;
                font-weight: bold;
                white-space: nowrap;
            }}

            .server-vents {{
                width: 35px;
                height: 15px;
                background: repeating-linear-gradient(
                    90deg,
                    #060C15 0px,
                    #060C15 3px,
                    #34475C 3px,
                    #34475C 5px
                );
                border-radius: 2px;
            }}

            .server-led {{
                width: 11px;
                height: 11px;
                flex-shrink: 0;
                border-radius: 50%;
                box-shadow: 0 0 12px currentColor;
            }}

            .led-green {{
                background: #22C55E;
                color: #22C55E;
            }}

            .led-red {{
                background: #EF4444;
                color: #EF4444;
            }}

            .led-amber {{
                background: #F59E0B;
                color: #F59E0B;
            }}
        </style>
        </head>

        <body>
            <div class="rack-scene">
                <div class="rack">
                    <div class="rack-header">
                        SIMULATED SERVER RACK
                    </div>
                    {rack_units}
                </div>
            </div>
        </body>
        </html>
        """

        components.html(
            rack_html,
            height=430,
            scrolling=False,
        )

    st.subheader("Hardware Validation Results")

    table = pd.DataFrame(
        [
            {
                "Rack ID": r["rack_id"],
                "Server Model": r["server_model"],
                "Status": r["status"],
                "Severity": r["severity"],
                "Failures": r["failure_count"],
            }
            for r in results
        ]
    )

    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
    )


# --------------------------------------------------
# HARDWARE DIAGNOSTICS
# --------------------------------------------------

elif page == "Hardware Diagnostics":

    st.subheader("Hardware Diagnostics")

    selected_id = st.selectbox(
        "Select Server",
        list(server_lookup.keys()),
    )

    server = server_lookup[selected_id]
    diagnostic = diagnose_server(server)

    c1, c2, c3 = st.columns(3)

    c1.metric("CPU Temperature", f"{server.cpu_temperature} °C")
    c2.metric("Memory Utilization", f"{server.memory_utilization}%")
    c3.metric("Disk Temperature", f"{server.disk_temperature} °C")

    st.divider()

    st.write("### Component Health")

    components = {
        "Disk": server.disk_healthy,
        "Power Supply": server.power_supply_healthy,
        "Network": server.network_connected,
    }

    for name, healthy in components.items():
        if healthy:
            st.success(f"{name}: HEALTHY")
        else:
            st.error(f"{name}: FAILURE")

    st.divider()

    st.write("### Diagnostic Results")

    if diagnostic["failures"]:

        st.dataframe(
            pd.DataFrame(diagnostic["failures"]),
            hide_index=True,
            width="stretch",
        )

    else:
        st.success("All diagnostic checks passed.")


# --------------------------------------------------
# REPAIR AND RETEST
# --------------------------------------------------

elif page == "Repair & Retest":

    st.subheader("Repair & Retest")

    selected_id = st.selectbox(
        "Select Server",
        list(server_lookup.keys()),
    )

    server = server_lookup[selected_id]
    initial = diagnose_server(server)

    st.write("### Initial Diagnostic")

    c1, c2, c3 = st.columns(3)

    c1.metric("Status", initial["status"])
    c2.metric("Severity", initial["severity"])
    c3.metric("Failures", initial["failure_count"])

    st.divider()

    st.write("### Simulated Repair Actions")

    with st.form("repair_form"):

        cpu = st.number_input(
            "CPU Temperature (°C)",
            min_value=0.0,
            max_value=150.0,
            value=float(server.cpu_temperature),
        )

        memory = st.number_input(
            "Memory Utilization (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(server.memory_utilization),
        )

        disk_temp = st.number_input(
            "Disk Temperature (°C)",
            min_value=0.0,
            max_value=120.0,
            value=float(server.disk_temperature),
        )

        disk_healthy = st.checkbox(
            "Disk Healthy",
            value=server.disk_healthy,
        )

        power_healthy = st.checkbox(
            "Power Supply Healthy",
            value=server.power_supply_healthy,
        )

        network_connected = st.checkbox(
            "Network Connected",
            value=server.network_connected,
        )

        notes = st.text_area(
            "Repair Notes",
            placeholder="Describe simulated corrective actions...",
        )

        submitted = st.form_submit_button(
            "Execute Repair & Retest",
            width="stretch",
        )

    if submitted:

        repairs = {
            "cpu_temperature": cpu,
            "memory_utilization": memory,
            "disk_temperature": disk_temp,
            "disk_healthy": disk_healthy,
            "power_supply_healthy": power_healthy,
            "network_connected": network_connected,
        }

        if not notes.strip():
            st.error("Repair notes are required.")

        elif initial["status"] == "PASS":
            st.warning(
                "This server already passes validation. "
                "Select a failed server to demonstrate the repair workflow."
            )

        else:

            record = repair_and_retest(
                server=server,
                repairs=repairs,
                repair_notes=notes,
            )

            save_repair_record(record)

            st.session_state["last_repair"] = record

            if record["repair_successful"]:
                st.success("Repair simulation completed successfully.")
            else:
                st.warning(
                    "Repair simulation completed, but unresolved "
                    "diagnostic failures remain."
                )

    if "last_repair" in st.session_state:

        record = st.session_state["last_repair"]

        st.divider()
        st.write("### Repair Validation Comparison")

        comparison = pd.DataFrame(
            [
                {
                    "Stage": "Initial",
                    "Status": record["initial_diagnostic"]["status"],
                    "Severity": record["initial_diagnostic"]["severity"],
                    "Failures": record["initial_diagnostic"]["failure_count"],
                },
                {
                    "Stage": "Post-Repair",
                    "Status": record["final_diagnostic"]["status"],
                    "Severity": record["final_diagnostic"]["severity"],
                    "Failures": record["final_diagnostic"]["failure_count"],
                },
            ]
        )

        st.dataframe(
            comparison,
            hide_index=True,
            width="stretch",
        )


# --------------------------------------------------
# REPAIR HISTORY
# --------------------------------------------------

elif page == "Repair History":

    st.subheader("Repair History")

    history = load_repair_history()

    if not history:

        st.info("No repair records have been saved yet.")

    else:

        history_rows = []

        for record in history:

            history_rows.append(
                {
                    "Rack ID": record["rack_id"],
                    "Timestamp": record["repair_timestamp"],
                    "Initial Status": record["initial_diagnostic"]["status"],
                    "Final Status": record["final_diagnostic"]["status"],
                    "Successful": record["repair_successful"],
                    "Repair Notes": record["repair_notes"],
                }
            )

        st.dataframe(
            pd.DataFrame(history_rows),
            width="stretch",
            hide_index=True,
        )

        st.caption(f"Total saved repair records: {len(history)}")