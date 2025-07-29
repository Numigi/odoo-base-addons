# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Document URL Chatter List",
    "summary": """
        Display URL attachments in a dedicated list in the chatter""",
    "description": """
        This module enhances the chatter component to:
        - Keep the standard display of attachments
        - Add a separate section listing URL attachments in a table view
        - Show name and creation date for each URL attachment
        - Requires the OCA 'document_url' module
        - Works on all form views with chatter
    """,
    "author": "Numigi",
    "website": "https://www.numigi.com",
    "category": "Discuss",
    "version": "14.0.1.0.0",
    "depends": ["mail", "web", "document_url"],
    "data": [
        "views/templates.xml",
    ],
    "qweb": [
        "static/src/xml/chatter_url_list.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
