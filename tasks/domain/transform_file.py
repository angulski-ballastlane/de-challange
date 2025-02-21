import polars as pl
from datetime import datetime
import re

from config import get_file_path


#####################
##Support Functions##
#####################


def adjust_columns(df, end_of_year):
    df = df.with_columns(
        pl.col("annual_max")
        .str.replace("$", "", literal=True)
        .str.replace(",", "")
        .cast(pl.Float64)
        .alias("annual_max")
    )

    df = df.with_columns(
        pl.when(
            pl.col("expiration_date")
            .str.strptime(pl.Date, "%Y%m%d", strict=False)
            .is_null()
        )
        .then(pl.lit(end_of_year))
        .otherwise(
            pl.col("expiration_date").str.strptime(pl.Date, "%Y%m%d", strict=False)
        )
        .alias("expiration_date"),
        pl.when(pl.col("est_app_time").is_null())
        .then(pl.lit(datetime.now()))
        .otherwise(
            pl.col("est_app_time").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
        )
        .alias("est_app_time"),
    )

    df = df.with_columns(
        pl.col("last_updated")
        .str.strptime(pl.Date, "%m/%d/%Y")
        .dt.strftime("%Y%m%d")
        .alias("last_updated")
    )

    return df


def create_struct_cols(df):
    "Creates the columns Funding and Form cols"
    df = df.with_columns(
        pl.struct(
            [
                pl.lit("Enrollment Form").alias("name"),
                pl.col("enrollment_url").alias("link"),
            ]
        ).alias("forms")
    )
    df = df.with_columns(pl.col("forms").map_elements(lambda x: [x]).alias("forms"))

    # funding struct
    df = df.with_columns(
        pl.struct(
            [
                pl.when(pl.col("processing_vendor").is_null())
                .then(pl.lit("Data Not Available"))
                .when(pl.col("processing_vendor").str.to_lowercase() == "evergreen")
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("evergreen"),
                pl.when(pl.col("fund_level_type").is_null())
                .then(pl.lit("Data Not Available"))
                .otherwise(pl.col("fund_level_type"))
                .alias("current_funding_level"),
            ]
        ).alias("funding")
    )
    return df


########
##MAIN##
########
def transform_to_domain():
    CURRENT_YEAR = datetime.today().year
    END_OF_YEAR = f"{CURRENT_YEAR}1231"
    FILL_WITH_NULLS_COLS = [
        "est_app_time",
        "income_details",
        "max_number_uses",
        "activation_num",
        "madetails",
    ]

    READ_PATH = get_file_path("raw", "dupixent")
    SAVE_PATH = get_file_path("domain", "treated_data")

    df = pl.read_json(READ_PATH)
    df = df.rename(
        {
            column_name: re.sub(r"([a-z])([A-Z])", r"\1_\2", column_name).lower()
            for column_name in df.columns
        }
    )
    df = df.rename({"assistance_type": "program_type"})

    df = df.with_columns(
        [
            pl.col(col).replace("Data Not Available", None).alias(col)
            for col in FILL_WITH_NULLS_COLS
        ]
    )

    df = adjust_columns(df, END_OF_YEAR)

    df = create_struct_cols(df)

    df.write_json(SAVE_PATH)


if __name__ == "__main__":
    transform_to_domain()
