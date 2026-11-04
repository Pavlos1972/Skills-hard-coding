"""
Fill the OM Application Template (assets/OM_Application_Template.pdf) for one
client, one product/transaction at a time, and optionally render the result
to PNG pages for a visual sanity check before delivery.

This is a library, not a fire-and-forget CLI: every client's field values
differ, and getting them right (correct replacement policy numbers, correct
N/A discipline, correct signature date) takes judgement the skill's
instructions cover — this script only handles the mechanical part of writing
real AcroForm field values into the real template.

Usage pattern (see SKILL.md for the full field-value rules):

    from fill_om_form import fill_om_application

    common = {
        "Title": "Mr", "FullName": "...", "IDNumber": "...",
        ... # every client-bio field from references/field-mappings.md
    }
    sheet = {
        "Product": "OM Tax Free recurring - R 1,000 p.m.",
        "DateOfEntry": "01/10/2026",
        "DeferredPremiumFacility": "No",
        "IsReplacement": "No",
        "ReplacedPolicyNumbers": "N/A",
        ... # every transaction-specific field
    }
    fill_om_application(
        template_path="assets/OM_Application_Template.pdf",
        common=common,
        sheet=sheet,
        out_path="OM Tax-Free - R 1000 p.m. - 27.08.26 - (Client Name).pdf",
    )
"""

import warnings

warnings.filterwarnings("ignore")

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, TextStringObject

# Products the dropdown ships with out of the box (from field-mappings.md).
# Used to find where a new amount-specific variant should be inserted.
_BASE_PRODUCT_PREFIXES = [
    "OM Flexi Investment Plan",
    "OM RA – Xtra Max 8.5% - section 14 transfer",
    "OM RA – Xtra Max 8.5%",
    "OM RA – Xtra Max 5%",
    "OM Optimal RA – Recurring",
    "OM Tax Free recurring",
    "OM Tax Free Lumpsum",
    "OM RA – Wealth recurring",
]


def add_product_option(writer: PdfWriter, new_value: str) -> None:
    """Add new_value to the Product field's dropdown /Opt array if it isn't
    already there. Product is a closed AcroForm choice field, not free text —
    pypdf's update_page_form_field_values will silently accept any string for
    a /Ch field's value, but the value should also exist in /Opt so the PDF
    renders it consistently in every viewer and the dropdown stays honest.
    """
    root = writer._root_object
    acro = root["/AcroForm"]
    for f in acro["/Fields"]:
        obj = f.get_object()
        if obj.get("/T") == "Product":
            opts = obj.get("/Opt")
            values = [str(o) for o in opts] if opts else []
            if new_value in values:
                return
            insert_at = len(values)
            for i, v in enumerate(values):
                if any(v.strip().startswith(p) for p in _BASE_PRODUCT_PREFIXES if v.strip() == p.strip() or v.strip().startswith(p.split(" – ")[0])):
                    insert_at = i + 1
            # Simpler, robust fallback: insert right after the base product
            # this is a variant of, matched by shared leading words.
            base_words = new_value.split(" - ")[0].strip()
            for i, v in enumerate(values):
                if v.strip() == base_words or base_words.startswith(v.strip()):
                    insert_at = i + 1
                    break
            values.insert(insert_at, new_value)
            obj[NameObject("/Opt")] = ArrayObject([TextStringObject(v) for v in values])
            return
    raise RuntimeError("Product field not found in template — has the template changed? Re-check field-mappings.md")


def fill_om_application(template_path: str, common: dict, sheet: dict, out_path: str) -> str:
    """Fill one copy of the OM template for one client/product and write it
    to out_path. Returns out_path. Raises if the Product field is missing
    (template changed) so a bad fill never ships silently.
    """
    reader = PdfReader(template_path)
    writer = PdfWriter()
    writer.append(reader)

    if "Product" in sheet:
        add_product_option(writer, sheet["Product"])

    values = dict(common)
    values.update(sheet)

    for page in writer.pages:
        writer.update_page_form_field_values(page, values, auto_regenerate=False)
    try:
        writer.set_need_appearances_writer(True)
    except Exception:
        pass

    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def dump_filled_values(pdf_path: str, field_names: list[str]) -> dict:
    """Read back the values actually written to a filled PDF, for the
    pre-delivery verification step (compare against what you intended to
    set). Use alongside a visual render — a field can be set correctly and
    still render oddly, and a render can look fine while a field silently
    kept its old value.
    """
    reader = PdfReader(pdf_path)
    fields = reader.get_fields() or {}
    return {name: (fields[name].get("/V") if name in fields else "<MISSING FIELD>") for name in field_names}
