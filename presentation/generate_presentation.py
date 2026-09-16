#!/usr/bin/env python3
"""
Generateur du support de soutenance ChurnScope (11 diapositives, format 16:9).

Ce script reconstruit integralement le fichier soutenance_churnscope.pptx a partir
des resultats reels et verifies du projet (voir docs/01_analyse_preparation.md,
docs/02_apprentissage_modeles.md, docs/03_validation_conclusion.md). Il ne depend
d'aucun fichier binaire existant : relancer ce script recree la presentation a
l'identique, ce qui la rend reproductible et versionnable en toute securite (le
.pptx final reste volontairement hors du depot Git, voir .gitignore).

Prerequis : pip install python-pptx

Utilisation :
    python presentation/generate_presentation.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# --------------------------------------------------------------------------- #
# Palette et constantes de mise en page
# --------------------------------------------------------------------------- #

NAVY = RGBColor(0x1E, 0x3A, 0x5F)  # Bleu principal (titres, blocs forts)
GOLD = RGBColor(0xC9, 0x8A, 0x2C)  # Accent (mise en avant du modele retenu)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF4, 0xF7)
DARK_TEXT = RGBColor(0x22, 0x2A, 0x35)
MID_GRAY = RGBColor(0x5B, 0x64, 0x70)

SLIDE_W = Inches(10)
SLIDE_H = Inches(5.63)

PRESENTATION_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = PRESENTATION_DIR / "soutenance_churnscope.pptx"


# --------------------------------------------------------------------------- #
# Fonctions utilitaires de mise en forme
# --------------------------------------------------------------------------- #


def new_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_slide(prs: Presentation):
    layout = prs.slide_layouts[6]  # layout vierge
    slide = prs.slides.add_slide(layout)
    bg = slide.shapes.add_shape(1, 0, 0, SLIDE_W, SLIDE_H)  # MSO_SHAPE.RECTANGLE
    bg.fill.solid()
    bg.fill.fore_color.rgb = WHITE
    bg.line.fill.background()
    bg.shadow.inherit = False
    # Renvoyer la forme en arriere-plan
    spTree = slide.shapes._spTree
    spTree.remove(bg._element)
    spTree.insert(2, bg._element)
    return slide


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text,
    *,
    size=14,
    bold=False,
    color=DARK_TEXT,
    align=PP_ALIGN.LEFT,
    font="Calibri",
    anchor=None,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    if anchor is not None:
        tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    return box


def set_shape_text(
    shape,
    text,
    *,
    size=14,
    bold=False,
    color=DARK_TEXT,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.MIDDLE,
):
    """Ecrit un texte dans une forme deja existante (au lieu d'une nouvelle zone de texte)."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return shape


def add_bullets(
    slide, left, top, width, height, items, *, size=13, color=DARK_TEXT, bullet_char="•"
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(6)
        run = p.add_run()
        run.text = f"{bullet_char} {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = "Calibri"
    return box


def add_header(slide, kicker, title):
    """Bandeau de titre commun a toutes les diapositives de contenu."""
    bar = slide.shapes.add_shape(1, 0, 0, SLIDE_W, Inches(0.9))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    bar.shadow.inherit = False
    add_textbox(
        slide,
        Inches(0.4),
        Inches(0.08),
        Inches(9),
        Inches(0.3),
        kicker,
        size=11,
        bold=True,
        color=RGBColor(0xB9, 0xC7, 0xD8),
    )
    add_textbox(
        slide,
        Inches(0.4),
        Inches(0.35),
        Inches(9),
        Inches(0.5),
        title,
        size=24,
        bold=True,
        color=WHITE,
    )


def add_stat_box(slide, left, top, width, height, value, label, *, accent=NAVY):
    box = slide.shapes.add_shape(1, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_GRAY
    box.line.color.rgb = accent
    box.line.width = Pt(1)
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run()
    r1.text = value
    r1.font.size = Pt(20)
    r1.font.bold = True
    r1.font.color.rgb = accent
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = label
    r2.font.size = Pt(10)
    r2.font.color.rgb = MID_GRAY


def add_footer(slide, page_no):
    add_textbox(
        slide,
        Inches(0.4),
        SLIDE_H - Inches(0.35),
        Inches(6),
        Inches(0.3),
        "ChurnScope — Prediction et prevention du churn client",
        size=9,
        color=MID_GRAY,
    )
    add_textbox(
        slide,
        SLIDE_W - Inches(1.2),
        SLIDE_H - Inches(0.35),
        Inches(0.8),
        Inches(0.3),
        str(page_no),
        size=9,
        color=MID_GRAY,
        align=PP_ALIGN.RIGHT,
    )


# --------------------------------------------------------------------------- #
# Diapositives
# --------------------------------------------------------------------------- #


def slide_01_title(prs):
    slide = blank_slide(prs)
    band = slide.shapes.add_shape(
        1, Inches(0.75), Inches(0.72), Inches(3.1), Inches(0.42)
    )
    band.fill.solid()
    band.fill.fore_color.rgb = NAVY
    band.line.fill.background()
    band.shadow.inherit = False
    set_shape_text(
        band,
        "Soutenance AIA01 — Septembre 2026",
        size=14,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_textbox(
        slide,
        Inches(0.75),
        Inches(1.55),
        Inches(8.5),
        Inches(0.75),
        "ChurnScope",
        size=38,
        bold=True,
        color=NAVY,
    )
    add_textbox(
        slide,
        Inches(0.78),
        Inches(2.35),
        Inches(8.5),
        Inches(0.55),
        "Prediction et prevention du depart client",
        size=18,
        color=DARK_TEXT,
    )
    add_textbox(
        slide,
        Inches(0.78),
        Inches(2.95),
        Inches(8.5),
        Inches(0.6),
        "« Quels clients devons-nous contacter cette semaine, et pourquoi ? »",
        size=14,
        color=MID_GRAY,
    )

    tag = slide.shapes.add_shape(1, Inches(0.75), Inches(4.7), Inches(2.6), Inches(0.4))
    tag.fill.solid()
    tag.fill.fore_color.rgb = LIGHT_GRAY
    tag.line.color.rgb = NAVY
    tag.line.width = Pt(0.75)
    tag.shadow.inherit = False
    set_shape_text(
        tag, "TELECOMMUNICATIONS", size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER
    )
    return slide


def slide_02_business_problem(prs):
    slide = blank_slide(prs)
    add_header(slide, "CONTEXTE", "Le probleme metier")

    stats = [
        ("7 043", "clients analyses"),
        ("26,54 %", "de churn"),
        ("Cible binaire", "Churn (0/1)"),
        ("Une probabilite", "a interpreter"),
    ]
    box_w = Inches(2.1)
    gap = Inches(0.15)
    x = Inches(0.4)
    for value, label in stats:
        add_stat_box(slide, x, Inches(1.2), box_w, Inches(1.1), value, label)
        x = Emu(int(x) + int(box_w) + int(gap))

    add_bullets(
        slide,
        Inches(0.5),
        Inches(2.7),
        Inches(8.8),
        Inches(1.6),
        [
            "L'entreprise veut reperer les clients qui risquent de partir "
            "pour leur proposer une action de fidelisation.",
            "Le modele aide a decider, mais ne remplace pas l'humain.",
        ],
        size=14,
    )
    add_footer(slide, 2)
    return slide


def slide_03_pipeline(prs):
    slide = blank_slide(prs)
    add_header(slide, "METHODE", "Pipeline de traitement")

    steps = [
        "Donnees brutes",
        "Controle qualite",
        "Nettoyage et preparation",
        "Separation train / test",
        "Entrainement des modeles",
        "Validation et comparaison",
        "Predictions et explicabilite",
        "Dashboard et monitoring",
    ]
    top = Inches(1.25)
    for i, step in enumerate(steps):
        box = slide.shapes.add_shape(1, Inches(1.6), top, Inches(6.8), Inches(0.4))
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY if i % 2 == 0 else GOLD
        box.line.fill.background()
        box.shadow.inherit = False
        set_shape_text(
            box, step, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER
        )
        top = Emu(int(top) + int(Inches(0.5)))
    add_footer(slide, 3)
    return slide


def slide_04_data_analysis(prs):
    slide = blank_slide(prs)
    add_header(slide, "ETAPE 1", "Analyse et preparation des donnees")

    add_textbox(
        slide,
        Inches(0.4),
        Inches(1.1),
        Inches(4.4),
        Inches(0.3),
        "Variables analysees",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.4),
        Inches(1.45),
        Inches(4.4),
        Inches(1.8),
        [
            "Demographiques : genre, senior, partenaire",
            "Services : telephone, internet, streaming",
            "Contrat : type, paiement, facturation",
            "Facturation : MonthlyCharges, TotalCharges, tenure",
        ],
        size=12,
    )

    add_textbox(
        slide,
        Inches(5.1),
        Inches(1.1),
        Inches(4.5),
        Inches(0.3),
        "Problemes de qualite detectes",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(5.1),
        Inches(1.45),
        Inches(4.5),
        Inches(1.8),
        [
            "TotalCharges importe en texte (object)",
            "11 chaines vides -> tenure = 0",
            "customerID supprime de l'apprentissage",
            "Aucun doublon exact detecte",
        ],
        size=12,
    )

    add_textbox(
        slide,
        Inches(0.4),
        Inches(3.3),
        Inches(9.2),
        Inches(0.3),
        "Repartition du churn : 5 174 clients restes (73,46 %) / 1 869 clients "
        "partis (26,54 %)",
        size=12,
        color=DARK_TEXT,
    )
    add_footer(slide, 4)
    return slide


def slide_05_split(prs):
    slide = blank_slide(prs)
    add_header(slide, "ETAPE 1", "Preparation sans fuite de donnees")

    box = slide.shapes.add_shape(
        1, Inches(2.75), Inches(1.15), Inches(4.5), Inches(0.55)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = NAVY
    box.line.fill.background()
    box.shadow.inherit = False
    set_shape_text(
        box,
        "80 % TRAIN   /   20 % TEST",
        size=16,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(2.05),
        Inches(6),
        Inches(0.3),
        "Regles appliquees",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.5),
        Inches(2.4),
        Inches(8.6),
        Inches(1.4),
        [
            "stratify=y pour preserver la proportion de churn",
            "Imputation, normalisation et encodage appris uniquement sur le train",
            "Toutes les transformations sont regroupees dans un Pipeline scikit-learn",
        ],
        size=13,
    )

    quote = slide.shapes.add_shape(1, Inches(0.5), Inches(3.95), Inches(9), Inches(0.9))
    quote.fill.solid()
    quote.fill.fore_color.rgb = LIGHT_GRAY
    quote.line.fill.background()
    quote.shadow.inherit = False
    set_shape_text(
        quote,
        "« Le jeu de test ne doit intervenir ni dans l'apprentissage des "
        "transformations ni dans le choix des hyperparametres. »",
        size=13,
        color=DARK_TEXT,
    )
    add_footer(slide, 5)
    return slide


def slide_06_comparison(prs):
    slide = blank_slide(prs)
    add_header(slide, "ETAPE 2", "Comparaison des modeles")

    rows = [
        ("Regression logistique", "0,783", "0,614", "0,841", False),
        ("Ridge Classifier", "0,789", "0,615", "0,836", False),
        ("Arbre de decision", "0,759", "0,622", "0,832", False),
        ("Random Forest ★", "0,791", "0,632", "0,842", True),
    ]
    table_shape = slide.shapes.add_table(
        5, 4, Inches(0.6), Inches(1.15), Inches(8.8), Inches(2.2)
    )
    table = table_shape.table
    headers = ["Modele", "Rappel", "F1-score", "AUC"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = WHITE
        p.runs[0].font.size = Pt(13)

    for r, (name, recall, f1, auc, highlight) in enumerate(rows, start=1):
        for c, val in enumerate([name, recall, f1, auc]):
            cell = table.cell(r, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = (
                RGBColor(0xFB, 0xF2, 0xDF) if highlight else WHITE
            )
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.bold = highlight
            p.runs[0].font.color.rgb = GOLD if highlight else DARK_TEXT

    add_textbox(
        slide,
        Inches(0.5),
        Inches(3.55),
        Inches(9),
        Inches(0.3),
        "Pourquoi Random Forest ?",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_textbox(
        slide,
        Inches(0.5),
        Inches(3.9),
        Inches(9),
        Inches(0.6),
        "Meilleur rappel : 0,791   •   Meilleur F1-score : 0,632   •   "
        "Meilleure AUC : 0,842   •   Capture des relations non lineaires",
        size=12,
        color=DARK_TEXT,
    )
    add_footer(slide, 6)
    return slide


def slide_07_optimization(prs):
    slide = blank_slide(prs)
    add_header(slide, "ETAPE 3", "Optimisation et hyperparametres")

    params = [
        "n_estimators = 200",
        "max_depth = 6",
        "min_samples_leaf = 1",
        'class_weight = "balanced"',
    ]
    x = Inches(0.4)
    box_w = Inches(2.25)
    for param in params:
        add_stat_box(slide, x, Inches(1.2), box_w, Inches(0.85), param, "", accent=NAVY)
        x = Emu(int(x) + int(box_w) + int(Inches(0.1)))

    add_textbox(
        slide,
        Inches(0.5),
        Inches(2.35),
        Inches(6),
        Inches(0.3),
        "Methode",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.5),
        Inches(2.7),
        Inches(8.8),
        Inches(1.3),
        [
            "Validation croisee stratifiee a 5 plis",
            "Recherche par grille (GridSearchCV)",
            "Optimisation du score rappel (recall)",
        ],
        size=13,
    )

    quote = slide.shapes.add_shape(
        1, Inches(0.5), Inches(4.05), Inches(9), Inches(0.85)
    )
    quote.fill.solid()
    quote.fill.fore_color.rgb = LIGHT_GRAY
    quote.line.fill.background()
    quote.shadow.inherit = False
    set_shape_text(
        quote,
        "Un churn non detecte peut representer une perte commerciale plus "
        "importante qu'une fausse alerte.",
        size=13,
        color=DARK_TEXT,
    )
    add_footer(slide, 7)
    return slide


def slide_08_final_results(prs):
    slide = blank_slide(prs)
    add_header(slide, "ETAPE 4", "Resultats sur le jeu de test")

    top_stats = [
        ("0,841", "AUC"),
        ("79,4 %", "Rappel churn"),
        ("51,4 %", "Precision churn"),
        ("0,624", "F1-score"),
        ("74,6 %", "Accuracy"),
    ]
    x = Inches(0.3)
    box_w = Inches(1.82)
    for value, label in top_stats:
        add_stat_box(slide, x, Inches(1.15), box_w, Inches(0.95), value, label)
        x = Emu(int(x) + int(box_w) + int(Inches(0.08)))

    bottom_stats = [
        ("297", "churns detectes"),
        ("77", "churns manques"),
        ("281", "fausses alertes"),
        ("754", "non-churn corrects"),
    ]
    x = Inches(0.3)
    box_w2 = Inches(2.27)
    for value, label in bottom_stats:
        add_stat_box(
            slide, x, Inches(2.3), box_w2, Inches(0.95), value, label, accent=GOLD
        )
        x = Emu(int(x) + int(box_w2) + int(Inches(0.08)))

    add_textbox(
        slide,
        Inches(0.4),
        Inches(3.55),
        Inches(9),
        Inches(0.4),
        "Matrice de confusion : [[754  281]  [77  297]]",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_footer(slide, 8)
    return slide


def slide_09_synthesis(prs):
    slide = blank_slide(prs)
    add_header(slide, "SYNTHESE", "Synthese des decisions")

    steps = [
        "Analyse\nexploratoire",
        "Comparaison\ndes 4 modeles",
        "Choix du\nRandom Forest",
        "Optimisation\ndes parametres",
        "Validation\nfinale",
    ]
    box_w = Inches(1.55)
    gap = Inches(0.18)
    x = Inches(0.35)
    for i, step in enumerate(steps):
        box = slide.shapes.add_shape(1, x, Inches(1.2), box_w, Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY
        box.line.fill.background()
        box.shadow.inherit = False
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        for j, line in enumerate(step.split("\n")):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = line
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = WHITE
        x = Emu(int(x) + int(box_w) + int(gap))
        if i < len(steps) - 1:
            add_textbox(
                slide,
                x - Emu(int(gap) - int(Inches(0.02))),
                Inches(1.45),
                Inches(0.15),
                Inches(0.4),
                "→",
                size=16,
                bold=True,
                color=GOLD,
                align=PP_ALIGN.CENTER,
            )

    add_textbox(
        slide,
        Inches(0.4),
        Inches(2.55),
        Inches(4.3),
        Inches(0.3),
        "Decision 1",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.4),
        Inches(2.9),
        Inches(4.3),
        Inches(0.8),
        ["L'accuracy seule est trompeuse sur une cible desequilibree"],
        size=12,
    )

    add_textbox(
        slide,
        Inches(5.1),
        Inches(2.55),
        Inches(4.3),
        Inches(0.3),
        "Decision 2",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(5.1),
        Inches(2.9),
        Inches(4.3),
        Inches(0.8),
        ["Le seuil est ajustable selon l'arbitrage rappel / precision"],
        size=12,
    )
    add_footer(slide, 9)
    return slide


def slide_10_code_quality(prs):
    slide = blank_slide(prs)
    add_header(slide, "MISE EN PRODUCTION", "Code, deploiement et qualite")

    add_textbox(
        slide,
        Inches(0.4),
        Inches(1.1),
        Inches(4.4),
        Inches(0.3),
        "Architecture du code",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.4),
        Inches(1.45),
        Inches(4.4),
        Inches(2.2),
        [
            "src/data/ : chargement, Pydantic, HMAC-SHA256",
            "src/models/ : entrainement + SHAP",
            "src/monitoring/ : Evidently AI",
            "tests/ : validation, pipeline, performance, securite",
            "CI/CD : Flake8 + Black + Pytest",
        ],
        size=12,
    )

    add_textbox(
        slide,
        Inches(5.1),
        Inches(1.1),
        Inches(4.5),
        Inches(0.3),
        "Dashboard Streamlit",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(5.1),
        Inches(1.45),
        Inches(4.5),
        Inches(2.9),
        [
            "Modele .joblib charge au demarrage",
            "Clients tries par probabilite",
            "Seuil ajustable en temps reel",
            "Explications SHAP par client",
            "Simulateur What-If",
            "Monitoring Evidently AI",
        ],
        size=12,
    )
    add_footer(slide, 10)
    return slide


def slide_11_limits_conclusion(prs):
    slide = blank_slide(prs)
    add_header(slide, "POUR CONCLURE", "Limites, ameliorations et conclusion")

    add_textbox(
        slide,
        Inches(0.4),
        Inches(1.05),
        Inches(4.4),
        Inches(0.3),
        "Limites actuelles",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(0.4),
        Inches(1.4),
        Inches(4.4),
        Inches(2.1),
        [
            "Un seul decoupage train / test",
            "Dataset historique, population limitee",
            "Associations ≠ causalite",
            "Nombreuses fausses alertes",
            "Seuil 0,5 non calibre sur le cout reel",
            "Pas de validation temporelle",
        ],
        size=11.5,
    )

    add_textbox(
        slide,
        Inches(5.1),
        Inches(1.05),
        Inches(4.5),
        Inches(0.3),
        "Ameliorations",
        size=13,
        bold=True,
        color=NAVY,
    )
    add_bullets(
        slide,
        Inches(5.1),
        Inches(1.4),
        Inches(4.5),
        Inches(2.1),
        [
            "Validation sur plusieurs periodes",
            "Calibration des probabilites",
            "Seuil selon les couts metier",
            "Test A/B des offres",
            "Monitoring continu en production",
            "Comparer XGBoost / LightGBM",
        ],
        size=11.5,
    )

    quote = slide.shapes.add_shape(
        1, Inches(0.4), Inches(3.7), Inches(9.2), Inches(1.15)
    )
    quote.fill.solid()
    quote.fill.fore_color.rgb = NAVY
    quote.line.fill.background()
    quote.shadow.inherit = False
    tf = quote.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run()
    r1.text = "ChurnScope est un outil d'aide a la priorisation."
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = WHITE
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = (
        "Le Random Forest detecte environ 4 churns sur 5, avec controle humain "
        "et suivi continu."
    )
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(0xD9, 0xE3, 0xEE)
    add_footer(slide, 11)
    return slide


# --------------------------------------------------------------------------- #
# Point d'entree
# --------------------------------------------------------------------------- #


def build_presentation() -> Path:
    prs = new_presentation()
    for slide_fn in (
        slide_01_title,
        slide_02_business_problem,
        slide_03_pipeline,
        slide_04_data_analysis,
        slide_05_split,
        slide_06_comparison,
        slide_07_optimization,
        slide_08_final_results,
        slide_09_synthesis,
        slide_10_code_quality,
        slide_11_limits_conclusion,
    ):
        slide_fn(prs)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT_PATH))
    return OUTPUT_PATH


def main():
    path = build_presentation()
    print(f"Presentation generee avec succes : {path}")
    print("Nombre de diapositives : 11")


if __name__ == "__main__":
    main()
