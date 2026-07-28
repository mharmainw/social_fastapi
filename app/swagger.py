from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse


def get_dark_swagger_ui_html(openapi_url: str, title: str) -> HTMLResponse:
    swagger_html = get_swagger_ui_html(
        openapi_url=openapi_url,
        title=title,
    ).body.decode("utf-8")

    dark_css = """
    <style>
      :root {
        color-scheme: dark;
      }

      body {
        background: #05070d;
      }

      .swagger-ui {
        color: #f8fafc;
      }

      .swagger-ui .topbar {
        background: #030712;
        border-bottom: 1px solid #1f2937;
      }

      .swagger-ui .wrapper,
      .swagger-ui .information-container {
        background: transparent;
      }

      .swagger-ui .info {
        margin: 34px 0 28px;
      }

      .swagger-ui .info .title {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        margin: 0 0 10px;
        color: #f8fafc;
        font-size: 36px;
        line-height: 1.2;
      }

      .swagger-ui .info .title small {
        position: static;
        top: auto;
        display: inline-flex;
        align-items: center;
        margin: 0;
        padding: 0;
        background: transparent !important;
        border: 0 !important;
      }

      .swagger-ui .info .title small pre {
        margin: 0;
        padding: 4px 9px;
        background: #172033 !important;
        color: #dbeafe !important;
        border: 1px solid #475569;
        border-radius: 999px;
        font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
        font-size: 12px;
        font-weight: 700;
        line-height: 1;
      }

      .swagger-ui .info .title .version-stamp pre {
        background: #0d2a1a !important;
        color: #86efac !important;
        border-color: #22c55e;
      }

      .swagger-ui .info a {
        color: #60a5fa;
        text-decoration: none;
      }

      .swagger-ui .info a:hover {
        color: #93c5fd;
        text-decoration: underline;
      }

      .swagger-ui .info .title,
      .swagger-ui .info p,
      .swagger-ui .info li,
      .swagger-ui .opblock-tag,
      .swagger-ui .opblock-summary-description,
      .swagger-ui .opblock-description-wrapper p,
      .swagger-ui .parameter__name,
      .swagger-ui .parameter__type,
      .swagger-ui .parameter__deprecated,
      .swagger-ui .response-col_status,
      .swagger-ui .response-col_description,
      .swagger-ui .tab li,
      .swagger-ui table thead tr td,
      .swagger-ui table thead tr th,
      .swagger-ui table tbody tr td,
      .swagger-ui .model,
      .swagger-ui .model-title,
      .swagger-ui .model-toggle,
      .swagger-ui .prop-type,
      .swagger-ui .prop-format,
      .swagger-ui .property,
      .swagger-ui label,
      .swagger-ui section.models h4,
      .swagger-ui section.models h5 {
        color: #f8fafc;
      }

      .swagger-ui .info .title small,
      .swagger-ui .info .base-url,
      .swagger-ui .parameter__in,
      .swagger-ui .renderedMarkdown,
      .swagger-ui .response-col_links,
      .swagger-ui .responses-header h4 {
        color: #cbd5e1;
      }

      .swagger-ui .scheme-container,
      .swagger-ui .opblock,
      .swagger-ui .opblock .opblock-section-header,
      .swagger-ui .responses-inner,
      .swagger-ui .model-box,
      .swagger-ui .model-container,
      .swagger-ui section.models {
        background: #0b1020;
        border-color: #334155;
        box-shadow: none;
      }

      .swagger-ui .opblock {
        border-radius: 8px;
      }

      .swagger-ui .opblock .opblock-summary {
        border-color: #334155;
      }

      .swagger-ui .opblock.opblock-get {
        background: rgba(14, 165, 233, 0.13);
        border-color: #38bdf8;
      }

      .swagger-ui .opblock.opblock-post {
        background: rgba(34, 197, 94, 0.13);
        border-color: #4ade80;
      }

      .swagger-ui .opblock.opblock-put {
        background: rgba(245, 158, 11, 0.14);
        border-color: #fbbf24;
      }

      .swagger-ui .opblock.opblock-delete {
        background: rgba(239, 68, 68, 0.14);
        border-color: #f87171;
      }

      .swagger-ui .opblock-summary-method {
        color: #020617;
        text-shadow: none;
      }

      .swagger-ui input,
      .swagger-ui textarea,
      .swagger-ui select {
        background: #020617;
        color: #f8fafc;
        border: 1px solid #64748b;
        border-radius: 6px;
      }

      .swagger-ui input[type="text"],
      .swagger-ui input[type="number"],
      .swagger-ui input[type="password"],
      .swagger-ui input[type="email"],
      .swagger-ui textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        caret-color: #60a5fa;
        -webkit-text-fill-color: #f8fafc;
      }

      .swagger-ui input[type="text"]:focus,
      .swagger-ui input[type="number"]:focus,
      .swagger-ui input[type="password"]:focus,
      .swagger-ui input[type="email"]:focus,
      .swagger-ui textarea:focus,
      .swagger-ui select:focus {
        background-color: #111827 !important;
        border-color: #60a5fa;
        outline: 2px solid rgba(96, 165, 250, 0.28);
        outline-offset: 1px;
      }

      .swagger-ui input:-webkit-autofill,
      .swagger-ui input:-webkit-autofill:hover,
      .swagger-ui input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px #0f172a inset;
        -webkit-text-fill-color: #f8fafc;
        caret-color: #60a5fa;
      }

      .swagger-ui input::placeholder,
      .swagger-ui textarea::placeholder {
        color: #94a3b8;
      }

      .swagger-ui .btn,
      .swagger-ui .btn.cancel,
      .swagger-ui .download-contents {
        background: #111827;
        color: #f8fafc;
        border-color: #94a3b8;
        box-shadow: none;
      }

      .swagger-ui .btn:hover,
      .swagger-ui .download-contents:hover {
        background: #1f2937;
      }

      .swagger-ui .btn.execute {
        background: #2563eb;
        border-color: #60a5fa;
        color: #ffffff;
      }

      .swagger-ui .highlight-code,
      .swagger-ui .microlight,
      .swagger-ui pre {
        background: #020617 !important;
        color: #e2e8f0 !important;
      }

      .swagger-ui table tbody tr td {
        border-color: #334155;
      }

      .swagger-ui .errors-wrapper {
        background: #450a0a;
        border-color: #ef4444;
        color: #fee2e2;
      }

      .swagger-ui section.models {
        overflow: hidden;
        background: #080d1b;
        border: 1px solid #334155;
        border-radius: 8px;
      }

      .swagger-ui section.models h4 {
        min-height: 54px;
        margin: 0;
        padding: 0 18px;
        display: flex;
        align-items: center;
        font-size: 18px;
        background: #0d1424;
        border-bottom: 1px solid #273449;
      }

      .swagger-ui section.models h4 svg {
        fill: #cbd5e1;
      }

      .swagger-ui section.models .model-container {
        margin: 0;
        padding: 0 18px;
        background: transparent;
        border-bottom: 1px solid #1e293b;
        border-radius: 0;
        transition: background-color 140ms ease;
      }

      .swagger-ui section.models .model-container:last-child {
        border-bottom: 0;
      }

      .swagger-ui section.models .model-container:hover {
        background: #10182a;
      }

      .swagger-ui section.models .model-box,
      .swagger-ui section.models .model-box-control,
      .swagger-ui section.models button {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
      }

      .swagger-ui section.models .model-box {
        padding: 16px 0;
      }

      .swagger-ui section.models button {
        color: #e2e8f0 !important;
      }

      .swagger-ui section.models .model-title,
      .swagger-ui section.models .model-title__text {
        color: #f8fafc !important;
        font-weight: 650;
      }

      .swagger-ui section.models .model-toggle {
        color: #cbd5e1 !important;
      }

      .swagger-ui section.models .model-toggle::after {
        filter: invert(90%) sepia(8%) saturate(390%) hue-rotate(178deg)
          brightness(94%) contrast(91%);
      }

      .swagger-ui section.models .prop-type {
        color: #93c5fd;
      }

      .swagger-ui section.models .prop-format {
        color: #94a3b8;
      }

      .swagger-ui section.models .property {
        color: #e2e8f0;
      }
    </style>
    """

    swagger_html = swagger_html.replace("</head>", f"{dark_css}</head>")
    return HTMLResponse(swagger_html)
