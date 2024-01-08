import json
import logging
from pathlib import Path
from urllib.parse import urljoin
import requests
from requests.auth import AuthBase
from airflow.hooks.base import BaseHook
from typing import Optional, Union, Dict, Any, Generator

class GraphQLHook(BaseHook):
    def __init__(self, conn_id: str):
        conn_values = self.get_connection(conn_id)
        self.conn_id = conn_id
        self.api_url = conn_values.host
        self.auth_url = urljoin(self.api_url, "api/sign_in")
        self.payload = {
            "user[email]": conn_values.login,
            "user[password]": conn_values.password,
        }
        self.cert_path = conn_values.extra_dejson.get("cert_path") 

    def get_graphql_query_from_file(self, path_para_arquivo_query: Union[Path, str]) -> str:
        return open(path_para_arquivo_query).read()

    def get_session(self) -> requests.Session:
        session = requests.Session()

        try:
            r = session.post(self.auth_url, data=self.payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.info("A login error occurred: %s", str(e))
            raise e

        if self.cert_path:
            session.verify = self.cert_path
        else:
            session.verify = True

        return session

    def run_graphql_query(self, graphql_query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        response = self.get_session().post(
            self.api_url, json={"query": graphql_query, "variables": variables}
        )
        status_code = response.status_code
        assert status_code == 200, logging.ERROR(
            f"""Query:\n\n\t {graphql_query} \n\nhas returned status code: {status_code}"""
        )

        return response.json()

    def run_graphql_paginated_query(self, paginated_graphql_query: str, component_type: Optional[str] = None, variables: Optional[Dict[str, Any]] = {}) -> Generator[Dict[str, Any], None, None]:
        if "page" not in variables:
            variables = {**variables, "page": "null"}

        all_results = {"data": {"component": {"proposals": {"nodes": []}}}}

        while True:
            response = self.run_graphql_query(paginated_graphql_query, variables)

            all_results["data"]["component"]["proposals"]["nodes"].extend(response["data"]["component"]["proposals"]["nodes"])

            end_cursor = response["data"]["component"][component_type.lower()]["pageInfo"]["endCursor"]
            has_next_page = response["data"]["component"][component_type.lower()]["pageInfo"]["hasNextPage"]

            if has_next_page:
                variables["page"] = end_cursor
            else:
                yield all_results
                break

    def write_json_to_file(self, data: Dict[str, Any], output_path: str):
        with open(output_path, 'w') as output_file:
            json.dump(data, output_file, indent=2)