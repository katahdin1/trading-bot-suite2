from fpdf import FPDF
import os

def generate_weekly_summary_pdf(output_path="reports/weekly_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly Strategy Performance Summary", ln=True)

    pdf.cell(200, 10, txt=" Best strategy: spy_momentum", ln=True)
    pdf.cell(200, 10, txt=" Worst strategy: qqq_breakout", ln=True)

    pdf.output(output_path)
    print(f" Weekly summary generated at {output_path}")

# Dummy equity curve
def generate_dummy_chart(output_path="charts/equity_curve.png"):
    import matplotlib.pyplot as plt
    import numpy as np

    x = range(10)
    y = [1000 + i * 50 - (i % 3) * 20 for i in x]

    plt.plot(x, y)
    plt.title("Equity Curve")
    plt.xlabel("Week")
    plt.ylabel("Portfolio Value")
    plt.savefig(output_path)
    plt.close()
    print(f" Chart saved to {output_path}")
