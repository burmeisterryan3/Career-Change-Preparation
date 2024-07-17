# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

# %run ./_common

# +
DA = DBAcademyHelper(course_config, lesson_config)
DA.reset_lesson()
DA.init()
DA.conclude_setup()

DA.paths.sales = f"{DA.paths.datasets}/ecommerce/sales/sales.delta"
DA.paths.users = f"{DA.paths.datasets}/ecommerce/users/users.delta"
DA.paths.events = f"{DA.paths.datasets}/ecommerce/events/events.delta"
DA.paths.products = f"{DA.paths.datasets}/products/products.delta"

DA.conclude_setup()

