====================================
Translation Data Translation Manager
====================================

Context
=======
Odoo's default translations are sometimes inadequate for specific regional requirements (e.g., French Canada vs. European French). Moreover, maintaining and replacing specific terms across hundreds of records and modules manually is a tedious and error-prone process.

Description
===========
This module provides a generic and robust toolset to manage translations across the entire Odoo database. It is not limited to any specific application (like Accounting) and works on any model.

The module introduces two main features:

1. **Global Term Mapping:** It intercepts Odoo's native translation loading process. You can define rules to automatically replace a specific source term with a new term, either globally or restricted to a specific model.
2. **Mass Translation Manager:** A wizard that allows administrators to dynamically copy, export, or import translations from one language to another for a specific subset of records.

Usage
=====
Global Translation Mapping
--------------------------
1. Navigate to **Settings / Translations / Mapping Terms**.
2. Create a new mapping rule. Set the original term and the new term.
3. Leave the `Model` field empty for a global replacement, or specify a model to restrict the scope.
4. Click the **Apply translation** button in the list view header to force the system to reload and apply the customized terms.

Mass Translation Wizard
-----------------------
1. Navigate to **Settings / Translations / Mass Translation Manager**.
2. Select the operation (e.g., `Copy`).
3. Select the Source Language and the Destination Language.
4. Select the Target Model.
5. Choose whether to apply the operation on all translatable fields or a specific selection.
6. Choose whether to process all records or filter them using the domain widget.
7. Click **Execute**.

Contributors
============
* Numigi and all its contributors (https://bit.ly/numigiens)