import polars as pl
import json

from agent.agent import create_model
from config import get_file_path, config


#####################
# Support Functions##
######################


def start_chat():
    model = create_model()

    chat_session = model.start_chat(history=None)

    return chat_session


def enrich_dataframe(df: pl.DataFrame, columns: list, chat_session) -> pl.DataFrame:
    def enrich_row(row: dict) -> dict:
        input_string = " | ".join(str(row[col]) for col in columns)
        try:
            response = chat_session.send_message(input_string).text
            enriched_data = json.loads(response)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error processing row {row}: {e}")
            enriched_data = {"benefits": [], "details": [], "requirements": []}

        return enriched_data

    enriched = df.select(columns).to_dicts()
    enriched_results = [enrich_row(row) for row in enriched]

    return df.with_columns(
        pl.Series([r["benefits"] for r in enriched_results]).alias("benefits"),
        pl.Series([r["details"] for r in enriched_results]).alias("details"),
        pl.Series([r["requirements"] for r in enriched_results]).alias("requirements"),
    )


########
##MAIN##
########
def enrich_data():
    DETAIL_COLUMNS = config["data"]["processed"]['enhanced_data']["config"]["detail_columns"]
    DOMAIN_INPUT_FILE = get_file_path("domain", "treated_data")
    PROCESSED_OUTPUT_FILE = get_file_path("processed", "enhanced_data")

    chat_session = start_chat()
    df = pl.read_json(DOMAIN_INPUT_FILE)

    df = enrich_dataframe(df, DETAIL_COLUMNS, chat_session)

    df.write_json(PROCESSED_OUTPUT_FILE)


if __name__ == "__main__":
    enrich_data()
