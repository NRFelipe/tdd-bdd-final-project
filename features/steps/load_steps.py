######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Steps

Steps file for products.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


def _to_bool(value) -> bool:
    """Converte strings comuns de booleano para bool real."""
    return str(value).strip().lower() in ("true", "1", "yes", "y", "t")


@given("the following products")
def step_impl(context):
    """Delete all Products and load new ones from the Background table"""
    rest_endpoint = f"{context.base_url}/products"

    # 1) Apaga tudo que existir
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK, (
        f"GET /products falhou: {context.resp.status_code} {context.resp.text}"
    )
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT, (
            f"DELETE /products/{product['id']} falhou: {context.resp.status_code} {context.resp.text}"
        )

    # 2) Carrega os dados do Background
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            # Deixe price como string; o serviço converte via Decimal
            "price": row["price"],
            "available": _to_bool(row["available"]),
            "category": row["category"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED, (
            f"POST /products falhou: {context.resp.status_code} {context.resp.text}"
        )
