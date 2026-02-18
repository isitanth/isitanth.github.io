#!/usr/bin/env python3
"""
build_cv.py — reads cv_data.yaml, renders anthony-chambet-cv.pdf
usage: python build_cv.py
       python build_cv.py --data other_cv.yaml
       python build_cv.py --out custom_name.pdf

requires: pip install reportlab pyyaml
"""

import argparse
import yaml
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

BLACK      = colors.HexColor("#111111")
GRAY_MID   = colors.HexColor("#555555")
GRAY_LIGHT = colors.HexColor("#888888")
RULE_COLOR = colors.HexColor("#DDDDDD")

MARGIN_H = 18 * mm
MARGIN_V = 16 * mm


def build_styles():
    return {
        "name": ParagraphStyle("name",
            fontName="Helvetica-Bold", fontSize=22, leading=26,
            textColor=BLACK, spaceAfter=2),
        "tagline": ParagraphStyle("tagline",
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=GRAY_MID, spaceAfter=0),
        "contact": ParagraphStyle("contact",
            fontName="Helvetica", fontSize=8.5, leading=12,
            textColor=GRAY_MID, spaceAfter=0),
        "section_head": ParagraphStyle("section_head",
            fontName="Helvetica-Bold", fontSize=7.5, leading=10,
            textColor=GRAY_LIGHT, spaceBefore=10, spaceAfter=4,
            letterSpacing=1.2),
        "job_title": ParagraphStyle("job_title",
            fontName="Helvetica-Bold", fontSize=9.5, leading=13,
            textColor=BLACK, spaceBefore=6, spaceAfter=1),
        "job_meta": ParagraphStyle("job_meta",
            fontName="Helvetica", fontSize=8.5, leading=12,
            textColor=GRAY_MID, spaceAfter=3),
        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=8.8, leading=13,
            textColor=BLACK, leftIndent=10, spaceAfter=1.5),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=8.8, leading=13,
            textColor=BLACK, spaceAfter=2),
        "skills_label": ParagraphStyle("skills_label",
            fontName="Helvetica-Bold", fontSize=8.5, leading=12,
            textColor=BLACK),
        "skills_val": ParagraphStyle("skills_val",
            fontName="Helvetica", fontSize=8.5, leading=12,
            textColor=GRAY_MID),
    }


def rule(S):
    return HRFlowable(width="100%", thickness=0.5,
                      color=RULE_COLOR, spaceAfter=4, spaceBefore=2)


def section(title, S):
    return [Spacer(1, 2), Paragraph(title.upper(), S["section_head"]), rule(S)]


def job_block(entry, S):
    blocks = [
        Paragraph(entry["title"], S["job_title"]),
        Paragraph(
            f"{entry['company']} · {entry['location']} · {entry['period']}",
            S["job_meta"]
        ),
    ]
    for b in entry.get("bullets", []):
        blocks.append(Paragraph(f"— {b}", S["bullet"]))
    return blocks


def skills_row(label, value, S):
    return Table(
        [[Paragraph(label, S["skills_label"]), Paragraph(value, S["skills_val"])]],
        colWidths=[28 * mm, None],
        style=TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ])
    )


def build(data, output_path):
    S = build_styles()
    story = []

    h = data["header"]
    story.append(Paragraph(h["name"], S["name"]))
    story.append(Paragraph(h["tagline"], S["tagline"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("  ·  ".join(h["contact"]), S["contact"]))
    story.append(Spacer(1, 8))

    if data.get("summary"):
        story += section("Summary", S)
        story.append(Paragraph(data["summary"].strip(), S["body"]))

    if data.get("experience"):
        story += section("Experience", S)
        for entry in data["experience"]:
            story += job_block(entry, S)

    if data.get("education"):
        story += section("Education", S)
        for entry in data["education"]:
            story.append(Paragraph(entry["degree"], S["job_title"]))
            story.append(Paragraph(
                f"{entry['school']} · {entry['location']} · {entry['period']}",
                S["job_meta"]
            ))

    if data.get("skills"):
        story += section("Technical skills", S)
        for row in data["skills"]:
            story.append(skills_row(row["label"], row["value"], S))

    if data.get("certifications"):
        story += section("Certifications", S)
        for cert in data["certifications"]:
            story.append(Paragraph(f"— {cert}", S["bullet"]))

    if data.get("languages"):
        story += section("Languages", S)
        story.append(Paragraph(data["languages"], S["body"]))

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN_H, rightMargin=MARGIN_H,
        topMargin=MARGIN_V, bottomMargin=MARGIN_V,
        title=data["meta"]["title"],
        author=data["meta"]["author"],
    )
    doc.build(story)
    print(f"built → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="cv_data.yaml", help="path to yaml data file")
    parser.add_argument("--out",  default=None,           help="override output pdf path")
    args = parser.parse_args()

    with open(args.data) as f:
        data = yaml.safe_load(f)

    output = args.out or data["meta"]["output"]
    build(data, output)
