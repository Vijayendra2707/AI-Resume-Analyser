import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_resume_report(data, output_folder="reports"):
    # Ensure folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, f"{data['candidate_name']}_Report.pdf")
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # --- Header Section ---
    c.setFillColor(colors.HexColor("#2C3E50")) # Dark Blue
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 60, "Resume Screening Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 85, f"Candidate: {data['candidate_name']}")
    c.drawRightString(width - 50, height - 85, f"Date: {data['date']}")

    # --- Match Summary ---
    y = height - 150
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Analysis Summary")
    
    # Status Badge
    status_color = colors.green if data['shortlisted'] == 1 else colors.red
    status_text = "SHORTLISTED" if data['shortlisted'] == 1 else "REJECTED"
    
    c.setFillColor(status_color)
    c.rect(50, y - 40, 150, 30, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(125, y - 28, status_text)

    # Score Metrics
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(220, y - 20, f"Match Score: {data['score']}%")
    c.drawString(220, y - 40, f"Semantic Similarity: {round(data.get('similarity', 0) * 100, 2)}%")

    # --- Skill Analysis ---
    y -= 100
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Matched Skills")
    c.line(50, y - 5, 200, y - 5)
    
    c.setFont("Helvetica", 10)
    y -= 25
    col_x = 50
    for i, skill in enumerate(data['matched_skills']):
        if i % 3 == 0 and i != 0: 
            y -= 15
            col_x = 50
        c.drawString(col_x, y, f"• {skill}")
        col_x += 180

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Missing Skills (Gaps)")
    c.line(50, y - 5, 200, y - 5)
    
    c.setFont("Helvetica", 10)
    y -= 25
    col_x = 50
    for i, skill in enumerate(data['missing_skills']):
        if i % 3 == 0 and i != 0:
            y -= 15
            col_x = 50
        c.drawString(col_x, y, f"• {skill}")
        col_x += 180

    # --- 🔴 NEW: Personalized Learning Path (Recommendations) ---
    course_links = data.get('course_links', {})
    if course_links:
        y -= 60
        # Check if we need a new page
        if y < 150:
            c.showPage()
            y = height - 50

        c.setFillColor(colors.HexColor("#1E40AF")) # Professional Blue
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Personalized Learning Path")
        c.line(50, y - 5, 250, y - 5)
        
        y -= 25
        for skill, links in course_links.items():
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, f"Skill: {skill.upper()}")
            y -= 15
            
            # Draw Links
            link_x = 70
            c.setFont("Helvetica-Oblique", 9)
            
            for platform, url in links.items():
                c.setFillColor(colors.blue)
                # This creates the visible text
                text = f"[{platform}]"
                c.drawString(link_x, y, text)
                
                # This makes the text clickable in the PDF
                text_width = c.stringWidth(text, "Helvetica-Oblique", 9)
                c.linkURL(url, (link_x, y, link_x + text_width, y + 10), relative=0)
                
                link_x += text_width + 15
            
            y -= 25 # Space between skills
            
            # Page overflow protection
            if y < 50:
                c.showPage()
                y = height - 50

    # --- Footer ---
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 30, "AI-Based Resume Screening System - Final Year Project 2026")

    c.showPage()
    c.save()
    return file_path