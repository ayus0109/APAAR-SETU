import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Palette
PRIMARY = colors.HexColor("#082C54")       # AICTE Deep Navy
PRIMARY_LIGHT = colors.HexColor("#0A4A8F") # Medium Blue
ACCENT = colors.HexColor("#1478FF")        # Highlight Blue
TEXT_DARK = colors.HexColor("#1E293B")     # Slate 800
TEXT_MUTED = colors.HexColor("#64748B")    # Slate 500
BG_LIGHT = colors.HexColor("#F8FAFC")      # Slate 50
BORDER_COLOR = colors.HexColor("#CBD5E1")  # Slate 300


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 808, "AICTE APAAR Platform — System Architecture & Feature Specification")
            self.drawRightString(559, 808, "SIH 2026 · Problem Statement 26263")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)
        
        # Footer (All pages)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.drawString(36, 30, "Repository: savy-032007/SIH-2026  ·  AICTE Regulation Bureau")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 30, page_str)
        self.restoreState()


def build_pdf(filename="AICTE_APAAR_Platform_Complete_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=48,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=PRIMARY_LIGHT
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=PRIMARY_LIGHT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=TEXT_DARK
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=PRIMARY
    )

    story = []

    # ---------------------------------------------------------
    # HEADER BANNER
    # ---------------------------------------------------------
    header_table_data = [
        [
            Paragraph("<b>AICTE APAAR Platform</b><br/><font size=11 color='#1478FF'>Student Data Management & Verification System</font>", title_style),
            Paragraph("<b>SIH 2026 · Problem Statement 26263</b><br/>AICTE Regulation Bureau<br/>Theme: Smart Automation<br/>Repo: <i>savy-032007/SIH-2026</i>", subtitle_style)
        ]
    ]
    t_header = Table(header_table_data, colWidths=[330, 193])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    # Executive Summary Box
    summary_text = (
        "<b>Executive Purpose:</b> The AICTE APAAR Platform establishes a single, unified student-level data submission "
        "and real-time automated verification gateway keyed by the 12-digit <b>APAAR ID</b> (Automated Permanent Academic "
        "Account Registry / ABC ID). It resolves the national problem of inconsistent reporting across technical institutions, "
        "enforces AICTE Approval Process Handbook intake caps, prevents ghost student enrollments, and integrates with the "
        "official <b>API Setu / DigiLocker Sandbox</b> for instant academic credential verification."
    )
    t_summary = Table([[Paragraph(summary_text, callout_style)]], colWidths=[523])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 1: REPOSITORY INVENTORY (savy-032007/SIH-2026)
    # ---------------------------------------------------------
    story.append(Paragraph("1. Repository Structure & Artifacts Overview", h1_style))
    story.append(Paragraph("The <code>savy-032007/SIH-2026</code> repository contains a production-ready, full-stack microservice and web architecture:", body_style))

    repo_files = [
        [Paragraph("File / Directory", table_header_style), Paragraph("Component", table_header_style), Paragraph("Functional Responsibility", table_header_style)],
        [Paragraph("<b>index.html</b>", table_cell_bold), Paragraph("Institution Portal UI", table_cell_style), Paragraph("Complete HTML5 institutional portal interface covering Dashboard, Student Records, Add/Edit Student form, Validation Console, Reports, and Settings.", table_cell_style)],
        [Paragraph("<b>style.css</b>", table_cell_bold), Paragraph("Design System", table_cell_style), Paragraph("Lightweight, responsive AICTE design system (no external CSS dependencies), styled KPI cards, custom modal, SVG chart layouts, and data tables.", table_cell_style)],
        [Paragraph("<b>app.js</b>", table_cell_bold), Paragraph("Frontend Controller", table_cell_style), Paragraph("Modular ES6 client engine managing JWT authentication, API Setu verification, dynamic SVG Enrolment Trend curves, category donut charts, and CSV exports.", table_cell_style)],
        [Paragraph("<b>services/api/</b>", table_cell_bold), Paragraph("FastAPI Core Backend", table_cell_style), Paragraph("REST API engine powered by FastAPI (Python 3.12+), SQLAlchemy 2 sync ORM, Alembic migrations, Pydantic v2 schemas, and security modules.", table_cell_style)],
        [Paragraph("<b>services/api/app/integrations/</b>", table_cell_bold), Paragraph("Government Adapters", table_cell_style), Paragraph("<b>ApiSetuSandboxDigiLocker</b> (official API Setu ABC ID card endpoint) & MockDigiLocker, plus <b>AbcRegistry</b> adapter with retry/backoff.", table_cell_style)],
        [Paragraph("<b>services/api/app/routers/</b>", table_cell_bold), Paragraph("API Routers", table_cell_style), Paragraph("Modular endpoint controllers: <code>institution.py</code> (dashboard, students, verify), <code>auth.py</code> (MFA/TOTP), <code>audit_log.py</code> (Merkle verification).", table_cell_style)],
        [Paragraph("<b>apps/web/</b>", table_cell_bold), Paragraph("Next.js 15 Web Portal", table_cell_style), Paragraph("Alternative modern App Router application with TypeScript, Tailwind CSS, shadcn/ui, Recharts, and multi-language i18n support.", table_cell_style)],
        [Paragraph("<b>services/mock-abc/</b>", table_cell_bold), Paragraph("Mock ABC Registry", table_cell_style), Paragraph("Standalone mock service running on port 9001 injecting configurable chaos, latency, and 503 retries for offline simulation.", table_cell_style)],
        [Paragraph("<b>data/generator/</b>", table_cell_bold), Paragraph("Synthetic Data Generator", table_cell_style), Paragraph("Deterministic generator using Faker('en_IN') producing ~35,000 synthetic students, 100 colleges, and planted fraud anomalies for demo verification.", table_cell_style)],
        [Paragraph("<b>docker-compose.yml</b>", table_cell_bold), Paragraph("DevOps Orchestration", table_cell_style), Paragraph("Multi-container composition orchestrating PostgreSQL 16, FastAPI Backend (8000), Mock ABC (9001), and Next.js Web (3000).", table_cell_style)],
        [Paragraph("<b>SPEC.md</b>", table_cell_bold), Paragraph("Formal Specification", table_cell_style), Paragraph("374-line comprehensive regulatory specification covering requirements R1 to R10, data models, and V1 to V5 rule catalogs.", table_cell_style)],
    ]
    t_repo = Table(repo_files, colWidths=[120, 110, 293])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_repo)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 2: COMPLETE TECHNOLOGY STACK
    # ---------------------------------------------------------
    story.append(Paragraph("2. Complete Technology Stack & Topology", h1_style))
    story.append(Paragraph("The platform is engineered around high performance, mathematical determinism, and Zero-Trust government compliance:", body_style))

    tech_stack = [
        [Paragraph("Layer", table_header_style), Paragraph("Core Technologies", table_header_style), Paragraph("Architectural Rationale & Capabilities", table_header_style)],
        [Paragraph("<b>Frontend</b>", table_cell_bold), Paragraph("HTML5, CSS3, ES6 JavaScript<br/>Next.js 15, TypeScript, Tailwind", table_cell_style), Paragraph("Zero external script dependencies on the static portal; instant load times; native SVG vector charts; dynamic conic-gradient donut graphics; full mobile responsiveness.", table_cell_style)],
        [Paragraph("<b>Backend API</b>", table_cell_bold), Paragraph("FastAPI, Python 3.12+, Uvicorn, Pydantic v2", table_cell_style), Paragraph("Thread-pooled synchronous execution keeping database advisory locks deterministic; OpenAPI auto-documentation; strict typing and declarative request parsing.", table_cell_style)],
        [Paragraph("<b>Database</b>", table_cell_bold), Paragraph("PostgreSQL 16, psycopg3, SQLAlchemy 2, Alembic", table_cell_style), Paragraph("ACID compliant transactional storage, versioned snapshot history for student enrolments (enrolment_version), and zero-loss migrations.", table_cell_style)],
        [Paragraph("<b>Cryptography</b>", table_cell_bold), Paragraph("AES-256-GCM, HMAC-SHA256, Argon2id, PyOTP", table_cell_style), Paragraph("Envelope encryption for sensitive PII (APAAR, phone, email, passport); blind deterministic hashes for indexed queries; TOTP MFA for admins; Argon2id password hashing.", table_cell_style)],
        [Paragraph("<b>Audit Ledger</b>", table_cell_bold), Paragraph("SHA-256 Cryptographic Hash Chain", table_cell_style), Paragraph("Tamper-evident Merkle-style block chain where every record write or PII reveal links to the previous block hash; verified via GET /audit/verify.", table_cell_style)],
        [Paragraph("<b>Integrations</b>", table_cell_bold), Paragraph("API Setu Sandbox (DigiLocker), HTTPX, Tenacity", table_cell_style), Paragraph("Direct HTTP client querying official endpoint <code>POST /certificate/v3/abc/abcid</code> with HMAC API keys, structured consent, exponential backoff, and local fallback.", table_cell_style)],
        [Paragraph("<b>Validation & AI</b>", table_cell_bold), Paragraph("rapidfuzz, scikit-learn, networkx", table_cell_style), Paragraph("Token Sort Ratio fuzzy name matching (transliteration invariant); IsolationForest for outlier intake anomalies; NetworkX for ghost student cluster graph analysis.", table_cell_style)],
    ]
    t_tech = Table(tech_stack, colWidths=[80, 140, 303])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # Page Break for Features
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SECTION 3: SYSTEM FEATURES & HOW TO USE
    # ---------------------------------------------------------
    story.append(Paragraph("3. Core System Features & Operational Walkthrough", h1_style))
    story.append(Paragraph("The platform provides end-to-end capabilities addressing all requirements of SIH Problem Statement 26263:", body_style))

    story.append(Paragraph("3.1 Executive Dashboard & Interactive Visualizations", h2_style))
    story.append(Paragraph(
        "• <b>Executive KPI Counters:</b> Displays real-time counts for <b>Approved Intake</b> (600), <b>Actual Enrolment</b> (570+), "
        "<b>Remaining Seats</b>, and <b>Total Students</b>, dynamically recalculated on student addition or deletion.<br/>"
        "• <b>Dynamic SVG Enrolment Trend Line Chart:</b> A vector graphic showing actual enrolment from <b>2022 to 2026</b> "
        "against the 600-seat approved intake ceiling. Features smooth cubic Bezier splines, a soft gradient fill, circular markers, hover tooltips, "
        "and a callout badge on the active academic year.<br/>"
        "• <b>Category Distribution Donut:</b> Renders active demographic splits (General, OBC, SC/ST, NRI/Other) using a dynamic CSS conic-gradient ring.<br/>"
        "• <b>How to Use:</b> Navigate to <b>Dashboard</b> in the sidebar. Switch academic years (2026/2025/2024) via the topbar dropdown to inspect historical intake.",
        body_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.2 Student Records Lifecycle Management (CRUD)", h2_style))
    story.append(Paragraph(
        "• <b>Multi-Filter & Instant Search:</b> Search across student name, college ID, or 12-digit APAAR ID with instant debounced filtering. "
        "Filter simultaneously by Course (B.Tech CSE, AIML, ECE, Mechanical, B.Pharm, MBA), Category, and Verification Status.<br/>"
        "• <b>Add & Edit Student Form:</b> Capture student personal details (Name, APAAR ID, DOB, Gender), academic details (Course, Admission Year, College ID), "
        "and statutory quota flags (Category, Supernumerary Seats, NRI, OCI, and Foreign National status).<br/>"
        "• <b>Action Modal Confirmations:</b> Editing opens pre-filled forms; deletion triggers modal confirmation and updates audit logs.<br/>"
        "• <b>How to Use:</b> Click <b>Student Records</b> → <b>＋ Add Student</b>. Fill out required fields and click <b>Save Student</b>.",
        body_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.3 Government API Setu / DigiLocker APAAR Verification", h2_style))
    story.append(Paragraph(
        "• <b>Government Endpoint Integration:</b> Directly interfaces with <code>POST https://sandbox.api-setu.in/certificate/v3/abc/abcid</code> "
        "using configured API Setu Client IDs and API Keys.<br/>"
        "• <b>Consent Artifact Flow:</b> Packages structured JSON consent artifacts containing timestamp, consumer ID, data provider, and digital signature algorithm.<br/>"
        "• <b>Cryptographic Audit Hash:</b> Computes SHA-256 hash of the verified certificate bytes for proof of document authenticity.<br/>"
        "• <b>Resilient Fallback:</b> Automatically degrades to local format and registry verification if the external government sandbox times out.<br/>"
        "• <b>How to Use:</b> In the student form, enter a 12-digit APAAR number (e.g. <code>918273645012</code>) and click <b>Verify APAAR</b>. "
        "Observe the confirmation message with the SHA-256 document hash.",
        body_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.4 Automated Multi-Stage Validation Engine (Rule Groups V1–V5)", h2_style))
    story.append(Paragraph(
        "The platform executes an automated compliance pipeline that catches errors before data submission:",
        body_style
    ))

    rules_table_data = [
        [Paragraph("Rule Group", table_header_style), Paragraph("Severity", table_header_style), Paragraph("Regulatory Check Description", table_header_style)],
        [Paragraph("<b>V1: Duplicate Records</b>", table_cell_bold), Paragraph("<font color='#EF4444'><b>ERROR</b></font>", table_cell_style), Paragraph("Prevents identical APAAR IDs from being submitted twice in a batch or twice within the same institution.", table_cell_style)],
        [Paragraph("<b>V2: APAAR & Name Matching</b>", table_cell_bold), Paragraph("<font color='#EF4444'><b>ERROR</b></font> / <font color='#F59E0B'><b>WARN</b></font>", table_cell_style), Paragraph("Enforces 12-digit format, verifies existence in ABC registry, and executes RapidFuzz token-sort name matching (warns if 80-90%, blocks below 80%).", table_cell_style)],
        [Paragraph("<b>V3: Intake Cap Enforcement</b>", table_cell_bold), Paragraph("<font color='#EF4444'><b>ERROR</b></font>", table_cell_style), Paragraph("Enforces course-level limits: blocks total students > Approved Intake; blocks NRI > 5% cap; enforces 15%/25% supernumerary quota ceilings.", table_cell_style)],
        [Paragraph("<b>V4: Data Inconsistencies</b>", table_cell_bold), Paragraph("<font color='#F59E0B'><b>WARN</b></font> / <font color='#EF4444'><b>ERROR</b></font>", table_cell_style), Paragraph("Flags Foreign Nationals declaring Indian qualifying boards; checks age plausibility (<15 or >60); demands sponsor proof for NRI category.", table_cell_style)],
        [Paragraph("<b>V5: Cross-Institution Duplicate</b>", table_cell_bold), Paragraph("<font color='#EF4444'><b>CRITICAL</b></font>", table_cell_style), Paragraph("Detects if the same APAAR ID is actively enrolled at two different institutions in the same academic year.", table_cell_style)],
    ]
    t_rules = Table(rules_table_data, colWidths=[120, 75, 328])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_rules)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.5 Tamper-Evident SHA-256 Audit Chain", h2_style))
    story.append(Paragraph(
        "• <b>Cryptographic Merkle Chaining:</b> Every student insertion, update, deletion, or PII reveal appends a block: "
        "<code>entry_hash = SHA256(prev_hash || timestamp || actor_id || action || payload)</code>.<br/>"
        "• <b>Tamper Verification:</b> Accessing <code>GET /api/v1/audit/verify</code> walks the chain from the genesis block. If any database administrator "
        "or unauthorized party modifies a row directly in PostgreSQL, the hash chain breaks and identifies the exact tampered row number.<br/>"
        "• <b>How to Use:</b> Navigate to <b>Settings</b> → <b>Security</b>. Click <b>Verify Chain →</b> to execute instant cryptographic chain verification.",
        body_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.6 Regulatory Reports & CSV Data Exporter", h2_style))
    story.append(Paragraph(
        "• <b>Instant CSV Exporting:</b> Generates pre-formatted regulatory spreadsheets directly in the browser with one click.<br/>"
        "• <b>Available Reports:</b> 1) <i>Student Records Report</i> (full roster with APAAR status), 2) <i>Validation Issues Report</i> (rule codes V1-V5 and anomalies), "
        "and 3) <i>Enrolment Summary Report</i> (programme capacity vs actual admissions).<br/>"
        "• <b>How to Use:</b> Navigate to <b>Reports</b> in the sidebar. Click <b>⇩ Export CSV</b> under any card to instantly download the file.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Page Break for API & Contracts
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SECTION 4: GOVERNMENT API SETU CONTRACT
    # ---------------------------------------------------------
    story.append(Paragraph("4. API Setu / DigiLocker Technical Specification", h1_style))
    story.append(Paragraph("The platform integrates with the confirmed DigiLocker ABC ID Card v3 specification:", body_style))

    api_setu_spec = (
        "<b>Endpoint:</b> <code>POST https://sandbox.api-setu.in/certificate/v3/abc/abcid</code><br/>"
        "<b>Request Headers:</b><br/>"
        "• <code>Content-Type: application/json</code><br/>"
        "• <code>X-APISETU-APIKEY: demokey123456ABCD789</code> (configurable via <code>DIGILOCKER_API_KEY</code>)<br/>"
        "• <code>X-APISETU-CLIENTID: in.gov.sandbox</code> (configurable via <code>DIGILOCKER_CLIENT_ID</code>)<br/><br/>"
        "<b>Request Payload Structure:</b><br/>"
        "<font name='Courier' size=7.2 color='#082C54'>"
        "{\n"
        "  \"txnId\": \"f7f1469c-29b0-4325-9dfc-c567200a70f7\",\n"
        "  \"format\": \"pdf\",\n"
        "  \"certificateParameters\": {\n"
        "    \"IdentityType\": \"NA\",\n"
        "    \"IdentityValue\": \"123456\",\n"
        "    \"level1\": \"1\",\n"
        "    \"AdmissionYear\": \"2021\",\n"
        "    \"UID\": \"123412341234\",       // 12-digit APAAR ID\n"
        "    \"FullName\": \"Demo user\",\n"
        "    \"DOB\": \"31-12-1980\",          // DD-MM-YYYY format\n"
        "    \"GENDER\": \"Male\"\n"
        "  },\n"
        "  \"consentArtifact\": {\n"
        "    \"consent\": {\n"
        "      \"consentId\": \"ea9c43aa-7f5a-4bf3-a0be-e1caa24737ba\",\n"
        "      \"timestamp\": \"2024-12-03T12:15:26.958Z\",\n"
        "      \"dataConsumer\": { \"id\": \"in.gov.sandbox\" },\n"
        "      \"dataProvider\": { \"id\": \"in.gov.abc\" },\n"
        "      \"purpose\": { \"description\": \"APAAR ABC ID Card Verification\" },\n"
        "      \"user\": { \"idType\": \"string\", \"idNumber\": \"string\", \"mobile\": \"9988776655\", \"email\": \"test@email.com\" },\n"
        "      \"permission\": { \"access\": \"string\", \"dateRange\": { \"from\": \"2024-12-03T12:15:26.958Z\", \"to\": \"2024-12-03T12:15:26.958Z\" } }\n"
        "    },\n"
        "    \"signature\": { \"signature\": \"SHA256withRSA\" }\n"
        "  }\n"
        "}"
        "</font>"
    )
    t_setu = Table([[Paragraph(api_setu_spec, body_style)]], colWidths=[523])
    t_setu.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_setu)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 5: COMPLETE API DIRECTORY
    # ---------------------------------------------------------
    story.append(Paragraph("5. Backend REST API Directory", h1_style))
    story.append(Paragraph("FastAPI routes exposed under <code>/api/v1</code>:", body_style))

    api_routes = [
        [Paragraph("Endpoint", table_header_style), Paragraph("Method", table_header_style), Paragraph("Auth / RBAC", table_header_style), Paragraph("Purpose & Response", table_header_style)],
        [Paragraph("<code>/api/v1/auth/login</code>", table_cell_bold), Paragraph("POST", table_cell_style), Paragraph("Public", table_cell_style), Paragraph("Authenticates credentials; issues access/refresh tokens or demands TOTP MFA.", table_cell_style)],
        [Paragraph("<code>/api/v1/auth/mfa/verify</code>", table_cell_bold), Paragraph("POST", table_cell_style), Paragraph("Public (MFA token)", table_cell_style), Paragraph("Verifies 6-digit TOTP code; issues JWT session tokens.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/dashboard</code>", table_cell_bold), Paragraph("GET", table_cell_style), Paragraph("INST_ADMIN, OPERATOR", table_cell_style), Paragraph("Returns KPI stats, 2022-2026 enrolment trend points, and category distribution.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/students</code>", table_cell_bold), Paragraph("GET", table_cell_style), Paragraph("INST_ADMIN, OPERATOR", table_cell_style), Paragraph("Paginated student roster with search query and category/status filters.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/students</code>", table_cell_bold), Paragraph("POST", table_cell_style), Paragraph("INST_ADMIN, OPERATOR", table_cell_style), Paragraph("Creates student record, generates audit log, and runs V1-V5 validation checks.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/students/{id}</code>", table_cell_bold), Paragraph("PUT / DELETE", table_cell_style), Paragraph("INST_ADMIN", table_cell_style), Paragraph("Updates or removes student record; snapshots previous version in audit trail.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/students/verify-apaar</code>", table_cell_bold), Paragraph("POST", table_cell_style), Paragraph("INST_ADMIN, OPERATOR", table_cell_style), Paragraph("Queries API Setu Sandbox ABC ID endpoint; returns verified status and SHA-256 hash.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/validation</code>", table_cell_bold), Paragraph("GET", table_cell_style), Paragraph("INST_ADMIN, OPERATOR", table_cell_style), Paragraph("Returns summary metrics and detailed breakdown of active validation anomalies.", table_cell_style)],
        [Paragraph("<code>/api/v1/institution/profile</code>", table_cell_bold), Paragraph("GET / PUT", table_cell_style), Paragraph("INST_ADMIN", table_cell_style), Paragraph("Inspects or updates institution AICTE approval number, intake, and address.", table_cell_style)],
        [Paragraph("<code>/api/v1/audit/verify</code>", table_cell_bold), Paragraph("GET", table_cell_style), Paragraph("INST_ADMIN, AICTE_*", table_cell_style), Paragraph("Walks Merkle hash chain from genesis to tail; flags any direct DB tampering.", table_cell_style)],
        [Paragraph("<code>/api/v1/rules</code>", table_cell_bold), Paragraph("GET", table_cell_style), Paragraph("Authenticated", table_cell_style), Paragraph("Returns active AICTE approval process rule parameters for current academic year.", table_cell_style)],
    ]
    t_api = Table(api_routes, colWidths=[140, 50, 100, 233])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 6: OPERATIONAL GUIDE (HOW TO RUN)
    # ---------------------------------------------------------
    story.append(Paragraph("6. Operational Deployment & Execution Manual", h1_style))
    story.append(Paragraph("Commands to execute, test, and demonstrate the platform:", body_style))

    run_instructions = (
        "<b>A. Running with Docker Compose (Multi-Container Deployment):</b><br/>"
        "<font name='Courier' size=8 color='#0A4A8F'>docker compose up --build</font><br/>"
        "• Web UI: <code>http://localhost:3000</code>  |  FastAPI Backend: <code>http://localhost:8000</code><br/>"
        "• Interactive Swagger Docs: <code>http://localhost:8000/docs</code>  |  Mock ABC Registry: <code>http://localhost:9001</code><br/><br/>"
        "<b>B. Running Locally with Python Virtual Environment:</b><br/>"
        "1. Activate virtual environment: <font name='Courier' size=8 color='#0A4A8F'>.\\.venv\\Scripts\\activate</font><br/>"
        "2. Start Backend: <font name='Courier' size=8 color='#0A4A8F'>$env:PYTHONPATH=\"services/api\"; uvicorn app.main:app --port 8000 --reload --app-dir services/api</font><br/>"
        "3. Open Frontend: Open <code>index.html</code> directly in any web browser.<br/>"
        "4. Default Demo Login: <b>admin@xyzcollege.ac.in</b> / <b>Demo@1234</b><br/><br/>"
        "<b>C. Running Automated Unit & Integration Tests:</b><br/>"
        "<font name='Courier' size=8 color='#0A4A8F'>$env:PYTHONPATH=\"services/api\"; .\\.venv\\Scripts\\pytest services/api/tests -v</font><br/>"
        "• Validates all 5 test suites including API Setu live contract validation, Mock consent, and endpoint checks."
    )
    t_run = Table([[Paragraph(run_instructions, body_style)]], colWidths=[523])
    t_run.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_run)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")


if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "AICTE_APAAR_Platform_Complete_Documentation.pdf"
    build_pdf(out_pdf)
