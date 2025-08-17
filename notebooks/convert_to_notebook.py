import nbformat
from nbformat.v4 import new_notebook, new_code_cell
import sys

def py_to_ipynb(py_file, ipynb_file):
    """
    Converts a Python script to a Jupyter notebook.
    This is a simplified converter; it doesn't handle markdown cells from the comments like jupytext does.
    It will put all the code in a single cell.
    """
    with open(py_file, 'r') as f:
        code = f.read()

    # Create a new notebook
    nb = new_notebook()

    # Create a code cell with the script's content
    code_cell = new_code_cell(code)

    # Add the cell to the notebook
    nb['cells'].append(code_cell)

    # Write the notebook to a file
    with open(ipynb_file, 'w') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_notebook.py <input_script.py> <output_notebook.ipynb>")
        sys.exit(1)

    py_to_ipynb(sys.argv[1], sys.argv[2])
