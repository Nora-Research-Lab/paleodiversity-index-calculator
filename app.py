import gradio as gr
import pandas as pd
from paleodiversity_index_calculator import calculate_indices, create_abundance_plot
import io
import base64
import matplotlib.pyplot as plt

def compute(abundance_df, input_type):
    if abundance_df is None or abundance_df.empty:
        # Return empty outputs
        return (gr.update(value=""),) * 7 + (gr.update(value=None),)
    # Validate columns
    if "Species" not in abundance_df.columns or "Abundance" not in abundance_df.columns:
        return ("Error: DataFrame must have 'Species' and 'Abundance' columns.",) * 7 + (gr.update(value=None),)
    # Clean: drop rows with missing species or abundance
    df = abundance_df.dropna(subset=["Species", "Abundance"]).copy()
    if df.empty:
        return ("Error: No valid rows.",) * 7 + (gr.update(value=None),)
    # Ensure abundance is numeric
    try:
        df["Abundance"] = pd.to_numeric(df["Abundance"], errors="coerce")
    except:
        return ("Error: Abundance must be numeric.",) * 7 + (gr.update(value=None),)
    df = df.dropna(subset=["Abundance"])
    if df.empty:
        return ("Error: No valid numeric abundances.",) * 7 + (gr.update(value=None),)
    if len(df) > 30:
        return ("Error: Maximum 30 species allowed.",) * 7 + (gr.update(value=None),)
    # Convert to list of tuples
    species_abundances = list(zip(df["Species"], df["Abundance"]))
    try:
        result = calculate_indices(species_abundances, input_type)
    except Exception as e:
        return (f"Error: {str(e)}",) * 7 + (gr.update(value=None),)
    # Format results
    S = str(result["S"])
    N = f"{result['N']:.4f}"
    H = f"{result['H']:.4f}"
    D = f"{result['D']:.4f}"
    one_minus_D = f"{result['1-D']:.4f}"
    one_over_D = f"{result['1/D']:.4f}"
    J = f"{result['J']:.4f}"
    # Create plot
    plot = create_abundance_plot(result["sorted_abundances"])
    return S, N, H, D, one_minus_D, one_over_D, J, plot

def download_results(abundance_df, input_type):
    # Recompute to get results
    if abundance_df is None or abundance_df.empty:
        return None, None
    df = abundance_df.dropna(subset=["Species", "Abundance"]).copy()
    if df.empty:
        return None, None
    try:
        df["Abundance"] = pd.to_numeric(df["Abundance"], errors="coerce")
    except:
        return None, None
    df = df.dropna(subset=["Abundance"])
    if df.empty or len(df) > 30:
        return None, None
    species_abundances = list(zip(df["Species"], df["Abundance"]))
    try:
        result = calculate_indices(species_abundances, input_type)
    except:
        return None, None
    # Prepare CSV string
    csv_lines = ["Metric,Value"]
    for key, value in result.items():
        if key != "sorted_abundances":
            csv_lines.append(f"{key},{value:.5f}")
    csv_str = "\n".join(csv_lines)
    csv_file = io.StringIO(csv_str)
    # Prepare plot PNG bytes
    fig = create_abundance_plot(result["sorted_abundances"])
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    png_bytes = buf.getvalue()
    plt.close(fig)
    return csv_str, png_bytes

# Gradio UI
with gr.Blocks(title="Paleodiversity Index Calculator") as demo:
    gr.Markdown("# Paleodiversity Index Calculator")
    gr.Markdown("Enter species names and their abundances. Select whether abundances are counts or percentages.")
    abundance_df = gr.Dataframe(
        headers=["Species", "Abundance"],
        datatype=["str", "number"],
        row_count=(1, "dynamic"),
        label="Species Abundances"
    )
    input_type = gr.Radio(choices=["Counts", "Percentages"], value="Counts", label="Input Type")
    compute_btn = gr.Button("Compute")
    with gr.Row():
        smd = gr.Number(label="S (species richness)", precision=0)
        nmd = gr.Number(label="N (total abundance)")
        hmd = gr.Number(label="Shannon H'")
        dmd = gr.Number(label="Simpson D (dominance)")
    with gr.Row():
        one_minus_d = gr.Number(label="1 - D (diversity)")
        one_over_d = gr.Number(label="1 / D (inverse Simpson)")
        jmd = gr.Number(label="Pielou's evenness J'")
    plot_output = gr.Plot(label="Sorted Abundance Bar Plot")
    download_btn = gr.Button("Download Results")
    download_csv = gr.File(label="Download CSV", file_types=[".csv"], visible=False)
    download_png = gr.File(label="Download PNG", file_types=[".png"], visible=False)

    compute_btn.click(
        compute,
        inputs=[abundance_df, input_type],
        outputs=[smd, nmd, hmd, dmd, one_minus_d, one_over_d, jmd, plot_output]
    )
    # Download handler: we need to produce files. Gradio's File component expects a filepath. We'll create temp files.
    def download_wrapper(abundance_df, input_type):
        csv_str, png_bytes = download_results(abundance_df, input_type)
        if csv_str is None:
            return None, None
        import tempfile, os
        # Write CSV
        csv_path = os.path.join(tempfile.gettempdir(), "paleodiversity_results.csv")
        with open(csv_path, "w") as f:
            f.write(csv_str)
        # Write PNG
        png_path = os.path.join(tempfile.gettempdir(), "paleodiversity_plot.png")
        with open(png_path, "wb") as f:
            f.write(png_bytes)
        return csv_path, png_path

    download_btn.click(
        download_wrapper,
        inputs=[abundance_df, input_type],
        outputs=[download_csv, download_png]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
