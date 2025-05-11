import pandas as pd
import numpy as np
from control import frd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to read CSV file
def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df

# Function to perform Bode analysis and return the FRD object
def bode_analysis(filepath):
    df = read_csv(filepath)

    # Assuming the CSV has columns 'Frequency[Hz]', 'Magnitude[dB]', and 'Phase[deg]'
    omega = 2 * np.pi * df['Frequency[Hz]']  # Convert frequency to radians per second
    magnitude = 10 ** (df["Magnitude[dB]"] / 20)  # Convert magnitude from dB to linear scale
    phase = np.unwrap(np.deg2rad(df["Phase[deg]"]))  # Convert phase to radians and unwrap it

    # Create FRD object
    bode_frd = frd(magnitude * np.exp(1j * phase), omega)

    return bode_frd

def ol(cl):
    return cl/(1-cl)

# Function to generate the Bode plot using Plotly
def generate_bode_plot(filepath):
    # Get the FRD object
    bode_frd = bode_analysis(filepath)
    bode_frd = ol(bode_frd)

    # Extract magnitude, phase, and frequency from the FRD object
    magnitude = np.abs(np.squeeze(bode_frd.response))  # Magnitude (linear scale)
    phase = np.angle(np.squeeze(bode_frd.response))  # Phase (in radians)
    omega = bode_frd.frequency  # Frequency (in rad/s)

    # Create subplots (two rows, one column)
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True,  # Share the x-axis (frequency)
        subplot_titles=('Magnitude [dB]', 'Phase [degrees]'),
        vertical_spacing=0.4  # Adjust space between subplots
    )

    # Create Magnitude plot
    magnitude_trace = go.Scatter(
        x=omega,
        y=20 * np.log10(magnitude),  # Convert magnitude to dB
        mode='lines',
        name='Magnitude [dB]',
        line=dict(color='blue')
    )

    # Create Phase plot
    phase_trace = go.Scatter(
        x=omega,
        y=np.rad2deg(phase),  # Convert phase to degrees
        mode='lines',
        name='Phase [degrees]',
        line=dict(color='red')
    )

    # Add the traces to the subplots
    fig.add_trace(magnitude_trace, row=1, col=1)  # Magnitude on top subplot
    fig.add_trace(phase_trace, row=2, col=1)      # Phase on bottom subplot

    # Layout settings for the subplots
    fig.update_layout(
        title='Bode Plot',
        xaxis=dict(
            title='Frequency [rad/s]',  # Set x-axis title (frequency)
            type='log',  # Logarithmic scale for frequency
        ),
        xaxis2=dict(
            title='Frequency [rad/s]',  # Set x-axis title (frequency)
            type='log',  # Logarithmic scale for frequency
        ),
        yaxis=dict(
            title='Magnitude [dB]',  # Set y-axis title for magnitude plot
            side='left'
        ),
        yaxis2=dict(
            title='Phase [degrees]',  # Set y-axis title for phase plot
            side='left'
        ),
        showlegend=True
    )


    # Return the figure as an HTML div
    plot_html = fig.to_html(full_html=False)

    return plot_html
