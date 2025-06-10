import streamlit as st
import pandas as pd
import numpy as np

# Load the JSON data into DataFrames
w_data = pd.read_csv('assets/data/w-member-data.csv').set_index('Shape')
mc_data = pd.read_csv('assets/data/mc-member-data.csv').set_index('Shape')

st.title("Structural Terminal")

st.markdown("""
**Commands:** `<member> <command>` (e.g., `W12X16 LR`)

| Command | Description |
|---------|-------------|
| `LR`    | Residual length limit (Lr) |
| `LP`    | Plastic length limit (Lp)  |
""")

# Input field
command = st.text_input("Enter command")

# State management
if 'state' not in st.session_state:
    st.session_state.state = None

if command:
    tokens = command.strip().upper().split()

    if len(tokens) == 2:
        shape, cmd = tokens

        if shape in w_data.index:
            shape_obj = w_data.loc[shape]

            if cmd == 'LR':
                st.session_state.shape_obj = shape_obj
                st.session_state.state = 'awaiting_fy_lr'
                st.write("Using default E = 29000 ksi")

            elif cmd == 'LP':
                st.session_state.shape_obj = shape_obj
                st.session_state.state = 'awaiting_fy_lp'
                st.write("Using default E = 29000 ksi")

            else:
                st.error("Unknown command")

        else:
            st.error(f"Shape {shape} not found.")

    elif st.session_state.state == 'awaiting_fy_lr':
        try:
            fy = float(command)
            st.session_state.fy = fy
            st.session_state.state = 'awaiting_c_lr'
        except ValueError:
            st.error("Invalid Fy value.")

    elif st.session_state.state == 'awaiting_c_lr':
        try:
            c = float(command)
            shape_obj = st.session_state.shape_obj
            rts_orig = shape_obj['rts']
            r_ts = rts_orig * np.sqrt(c)
            ho = shape_obj['d'] - shape_obj['tf']
            Sx = shape_obj['Sx']
            J = shape_obj['J']
            E = 29000
            fy = st.session_state.fy

            term = (0.7 * fy / E) * ((Sx * ho) / (J * c))
            inside = 1 + np.sqrt(1 + 6.76 * term**2)
            Lr = 1.95 * r_ts * np.sqrt(E / (0.7 * fy)) * np.sqrt(inside)
            Lr_ft = Lr / 12
            st.write(f"**Lr:** {Lr_ft:.2f} ft")
            st.session_state.state = None

        except ValueError:
            st.error("Invalid c value.")

    elif st.session_state.state == 'awaiting_fy_lp':
        try:
            fy = float(command)
            shape_obj = st.session_state.shape_obj
            ry = shape_obj['ry']
            E = 29000
            Lp_in = 1.76 * ry * np.sqrt(E / fy)
            Lp_ft = Lp_in / 12
            st.write(f"**Lp:** {Lp_ft:.2f} ft")
            st.session_state.state = None

        except ValueError:
            st.error("Invalid Fy value.")

    else:
        # Direct shape info
        if command in w_data.index:
            st.dataframe(w_data.loc[command])
        elif command in mc_data.index:
            st.dataframe(mc_data.loc[command])
        else:
            st.error("Shape not found.")