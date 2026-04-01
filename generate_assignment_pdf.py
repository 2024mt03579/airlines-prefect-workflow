"""
Script to generate PDF document from assignment writeup.
Run: python generate_assignment_pdf.py
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

# Document setup
output_path = "ASSIGNMENT_SUBMISSION.pdf"
doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#003366'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=colors.HexColor('#003366'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=11,
    textColor=colors.HexColor('#0066CC'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

# Title Page
story.append(Paragraph("CCZG506 - API-driven Cloud Native Solutions", title_style))
story.append(Paragraph("Assignment I: Cloud-based Data Science / Machine Learning Application", title_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Project Submission Write-up", styles['Heading2']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Submitted: {datetime.now().strftime('%B %d, %Y')}", body_style))
story.append(PageBreak())

# Executive Summary
story.append(Paragraph("Executive Summary", heading1_style))
story.append(Paragraph(
    "This project implements a <b>Cloud-based Data Science Pipeline</b> using <b>Prefect Cloud</b> for orchestration and deployment. "
    "The application processes airline fare data, performs exploratory data analysis, trains machine learning models, and exposes "
    "application details via APIs. All workflows are scheduled, logged, and deployed on Prefect Cloud infrastructure.",
    body_style
))
story.append(Spacer(1, 0.15*inch))

# Objective Mapping
story.append(Paragraph("Objective Mapping", heading1_style))

# Objective 1
story.append(Paragraph("Objective 1: Design and Development of a Data Pipeline (6 marks)", heading2_style))

story.append(Paragraph("<b>1.1 Business Understanding</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Problem Statement:</b> Predict average airline fares based on historical data to understand pricing trends and help airlines optimize revenue management.",
    body_style
))
story.append(Paragraph("<b>Dataset:</b> US DOT Airfare Historical Data (2008-2025)", body_style))
story.append(Paragraph("<b>Target Variable:</b> avg_fare (average passenger fare)", body_style))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>1.2 Data Ingestion</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Dataset Source:</b> GitHub public repository (US DOT Airfare Historical Data)<br/>"
    "<b>Loading Method:</b> Automated remote loading via pandas read_csv()<br/>"
    "<b>Implementation:</b> Prefect task 'load_dataset()' fetches data from remote URL",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>1.3 Data Pre-processing</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Activities Implemented:</b><br/>"
    "• Missing Values Detection &amp; Imputation (median strategy)<br/>"
    "• Data Type Conversion (numeric coercion)<br/>"
    "• Normalization using Min-Max Scaling<br/>"
    "• Date parsing and conversion<br/>",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>1.4 Exploratory Data Analysis (EDA)</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Activities Implemented:</b><br/>"
    "• Pearson Correlation Analysis (largest_carrier_fare vs avg_fare)<br/>"
    "• Distance Binning (4 categories: Very Short, Short, Medium, Long)<br/>"
    "• One-Hot Encoding for Quarter categorical feature<br/>"
    "• Data Visualization (scatter plots saved to output/)<br/>",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>1.5 DataOps - Workflow Automation &amp; Scheduling</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Orchestration:</b> Prefect Cloud (v3.6.22)<br/>"
    "<b>Scheduling:</b> Automated execution every 120 seconds<br/>"
    "<b>Cloud Dashboard:</b> All logs captured and displayed on Prefect Cloud<br/>"
    "<b>Monitoring:</b> Real-time status updates and flow execution history",
    body_style
))
story.append(Spacer(1, 0.2*inch))

# Objective 2
story.append(Paragraph("Objective 2: Design and Development of a ML Pipeline (4 marks)", heading2_style))

story.append(Paragraph("<b>2.1 Model Preparation</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Algorithm Selected:</b> Linear Regression<br/>"
    "<b>Rationale:</b> Suitable for time-series fare prediction with interpretable coefficients",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>2.2 Model Training</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Data Split:</b> 80% training, 20% testing (with random_state=42 for reproducibility)<br/>"
    "<b>Algorithm:</b> scikit-learn LinearRegression",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>2.3 Model Evaluation</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Metrics Computed:</b><br/>"
    "• MAE (Mean Absolute Error)<br/>"
    "• RMSE (Root Mean Squared Error)<br/>"
    "• R² Score (Coefficient of Determination)",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>2.4 MLOps - Model Monitoring &amp; Logging</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Metrics Tracked:</b> MAE, RMSE, R² Score, Feature Importance<br/>"
    "<b>Cloud Integration:</b> All metrics logged to Prefect Cloud<br/>"
    "<b>Monitoring:</b> Task execution histories and performance trends visible on dashboard",
    body_style
))
story.append(Spacer(1, 0.2*inch))

# Objective 3
story.append(Paragraph("Objective 3: API Access (2 marks)", heading2_style))

story.append(Paragraph("<b>3.1 Retrieve Application Details</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>APIs Utilized:</b><br/>"
    "• Prefect Cloud Flow Details API<br/>"
    "• Prefect Cloud Deployment Details API",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>3.2 Display Application Details</b>", styles['Heading3']))
story.append(Paragraph(
    "<b>Details Retrieved &amp; Displayed:</b><br/>"
    "• Flow Information: ID, name, description, tags<br/>"
    "• Deployment Information: ID, name, schedule, status",
    body_style
))
story.append(PageBreak())

# Architecture
story.append(Paragraph("Technology Stack &amp; Architecture", heading1_style))

tech_data = [
    ['Component', 'Technology'],
    ['Orchestration', 'Prefect Cloud v3.6.22'],
    ['Language', 'Python 3.14.2'],
    ['Data Processing', 'pandas, numpy'],
    ['ML Framework', 'scikit-learn'],
    ['Statistics', 'scipy'],
    ['Visualization', 'matplotlib'],
    ['API Client', 'requests'],
]

tech_table = Table(tech_data, colWidths=[2.5*inch, 3.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0F0F0')),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
story.append(tech_table)
story.append(Spacer(1, 0.2*inch))

# Compliance Summary
story.append(Paragraph("Compliance Summary", heading1_style))

compliance_data = [
    ['Requirement', 'Status', 'Details'],
    ['1.1 Business Understanding', '✓ Complete', 'Airline fare prediction problem identified'],
    ['1.2 Data Ingestion', '✓ Complete', 'Public dataset from GitHub'],
    ['1.3 Data Preprocessing', '✓ Complete', 'Missing values, normalization, encoding'],
    ['1.4 EDA', '✓ Complete', 'Correlation, binning, visualization performed'],
    ['1.5 DataOps', '✓ Complete', 'Prefect workflows, scheduled execution, cloud logging'],
    ['2.1 Model Preparation', '✓ Complete', 'Linear Regression selected'],
    ['2.2 Model Training', '✓ Complete', '80/20 train/test split'],
    ['2.3 Model Evaluation', '✓ Complete', 'MAE, RMSE, R² metrics computed'],
    ['2.4 MLOps', '✓ Complete', 'Metrics logged to Prefect Cloud'],
    ['3.1 API Retrieval', '✓ Complete', 'Prefect Cloud APIs utilized'],
    ['3.2 API Display', '✓ Complete', 'Flow &amp; deployment details displayed'],
]

compliance_table = Table(compliance_data, colWidths=[2.0*inch, 1.2*inch, 2.8*inch])
compliance_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0F0F0')),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
story.append(compliance_table)
story.append(Spacer(1, 0.3*inch))

# Key Achievements
story.append(Paragraph("Key Achievements", heading1_style))
story.append(Paragraph(
    "• <b>End-to-End Pipeline:</b> Complete data ingestion → preprocessing → EDA → ML modeling<br/>"
    "• <b>Cloud-Native Design:</b> Leverages Prefect Cloud for enterprise-grade orchestration<br/>"
    "• <b>Automated Scheduling:</b> Workflows run automatically every 120 seconds<br/>"
    "• <b>Comprehensive Monitoring:</b> All activities accessible via cloud dashboard<br/>"
    "• <b>API Integration:</b> Demonstrates Prefect API consumption<br/>"
    "• <b>Production-Ready:</b> Uses version control and environment management",
    body_style
))

# Build PDF
doc.build(story)
print(f"✓ PDF document generated: {output_path}")
print(f"✓ File size: {os.path.getsize(output_path) / 1024:.1f} KB")
print(f"✓ Ready for submission")
