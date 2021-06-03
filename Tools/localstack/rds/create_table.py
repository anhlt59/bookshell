#!/usr/bin/python3
import json
import os
import sys
import time
import uuid

import psycopg2

HOST = os.getenv("RDS_HOST", "localhost")
PORT = int(os.getenv("RDS_PORT", 5432))
DB_NAME = os.getenv("RDS_DB", "postgres")
USERNAME = os.getenv("RDS_USERNAME", "root")
PASSWORD = os.getenv("RDS_PASSWORD", "12345678")


def create_connection(retries=60):
    try:
        return psycopg2.connect(f"dbname='{DB_NAME}' user='{USERNAME}' host='{HOST}' password='{PASSWORD}'")
    except psycopg2.OperationalError:
        if retries:
            print("Retry connect to RDS ...")
            time.sleep(2)
            return create_connection(retries - 1)
        print("Exceeded maximum retry time")
        sys.exit(1)


def execute_query(connect, query):
    with connect.cursor() as cursor:
        try:
            cursor.execute(query)
            print(query)
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)
        connect.commit()
        if cursor.description:
            return list(cursor.fetchall())


def create_table(connection):
    queries = [
        """CREATE TABLE providers (
            id UUID NOT NULL,
            code VARCHAR(50) NOT NULL,
            name VARCHAR(100) NOT NULL,
            is_visible BOOLEAN,
            visible_count INTEGER,
            invisible_count INTEGER,
            cron_status BOOLEAN DEFAULT TRUE,
            oldest_pubdate TIMESTAMP WITH TIME ZONE,
            updated_at TIMESTAMP WITHOUT TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (name)
        )
        """,
        """CREATE TABLE countries (
            id SERIAL NOT NULL,
            name VARCHAR(100) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (name)
        )""",
        """CREATE TABLE individual_indicators (
            id SERIAL NOT NULL,
            provider_code VARCHAR(50) NOT NULL,
            key VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (id)
        )""",
        """CREATE TABLE monitoring_report_log (
            id UUID NOT NULL,
            datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            provider_code VARCHAR(50) NOT NULL,
            visible BOOLEAN,
            s3 INTEGER NOT NULL,
            insert INTEGER NOT NULL,
            update INTEGER NOT NULL,
            fail INTEGER NOT NULL,
            delete INTEGER NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id)
        )""",
        """CREATE TABLE articles (
            uuid UUID NOT NULL,
            unique_record TEXT NOT NULL,
            provider_code VARCHAR(250) NOT NULL,
            provider_article_id TEXT NOT NULL,
            provider_source TEXT,
            provider_title TEXT,
            provider_description TEXT,
            first_display_time TIMESTAMP WITHOUT TIME ZONE,
            last_build_date TIMESTAMP WITHOUT TIME ZONE,
            article_title TEXT,
            article_description TEXT,
            article_content TEXT,
            canonical_url TEXT,
            category JSON,
            category_id JSON,
            pub_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            provider_image TEXT,
            visible BOOLEAN NOT NULL,
            enable_display_body BOOLEAN NOT NULL,
            payload JSON,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            s3_file_path TEXT,
            default_language VARCHAR(250),
            provider_data_timezone VARCHAR(250),
            executed_timezone VARCHAR(250),
            PRIMARY KEY (uuid),
            UNIQUE (uuid)
        )""",
        """CREATE TABLE archived_articles (
            uuid UUID NOT NULL,
            unique_record TEXT NOT NULL,
            provider_code VARCHAR(250) NOT NULL,
            provider_article_id TEXT NOT NULL,
            provider_source TEXT,
            provider_title TEXT,
            provider_description TEXT,
            first_display_time TIMESTAMP WITHOUT TIME ZONE,
            last_build_date TIMESTAMP WITHOUT TIME ZONE,
            article_title TEXT,
            article_description TEXT,
            article_content TEXT,
            canonical_url TEXT,
            category JSON,
            category_id JSON,
            pub_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            provider_image TEXT,
            visible BOOLEAN NOT NULL,
            enable_display_body BOOLEAN NOT NULL,
            payload JSON,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            s3_file_path TEXT,
            default_language VARCHAR(250),
            provider_data_timezone VARCHAR(250),
            executed_timezone VARCHAR(250),
            origin_modified_at TIMESTAMP WITHOUT TIME ZONE,
            PRIMARY KEY (uuid),
            UNIQUE (uuid)
        )""",
        """CREATE TABLE individual_countries (
            id SERIAL NOT NULL,
            name VARCHAR(100) NOT NULL,
            provider_code VARCHAR(50) NOT NULL,
            country_id INTEGER NOT NULL,
            note TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY(country_id) REFERENCES countries (id)
        )""",
        """CREATE TABLE provider_settings (
            id UUID NOT NULL,
            code_id UUID NOT NULL,
            period INTEGER,
            yesterday_difference INTEGER,
            last_week_difference INTEGER,
            updated_at TIMESTAMP WITHOUT TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (id),
            FOREIGN KEY(code_id) REFERENCES providers (id)
        )""",
        """CREATE TABLE provider_errors (
            id UUID NOT NULL,
            code_id UUID NOT NULL,
            file_name VARCHAR(200) NOT NULL,
            error_message TEXT NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE,
            PRIMARY KEY (id),
            UNIQUE (id),
            FOREIGN KEY(code_id) REFERENCES providers (id)
        )""",
        """CREATE TABLE aggregated_indicators (
            id VARCHAR(50) NOT NULL,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            year INTEGER NOT NULL,
            half_year_period INTEGER,
            quarter_period INTEGER,
            month INTEGER,
            week INTEGER,
            day INTEGER,
            value FLOAT,
            scale VARCHAR(20),
            unit VARCHAR(20),
            individual_indicator_id INTEGER NOT NULL,
            individual_country_id INTEGER NOT NULL,
            provider_code VARCHAR(50) NOT NULL,
            interval VARCHAR(16) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE,
            modified_at TIMESTAMP WITHOUT TIME ZONE,
            PRIMARY KEY (id),
            FOREIGN KEY(individual_indicator_id) REFERENCES individual_indicators (id),
            FOREIGN KEY(individual_country_id) REFERENCES individual_countries (id)
        )""",
    ]

    for query in queries:
        execute_query(connection, query)


def upsert_providers(connection):
    def get_providers_from_setting_files(*file_paths):
        for path in file_paths:
            with open(path) as f:
                for _item in json.load(f):
                    payload = _item.get("Payload").get("Http") or _item.get("Payload").get("Ftp")
                    yield (
                        str(uuid.uuid4()),
                        _item.get("Code"),
                        _item.get("ProviderCode"),
                        "true" if payload.get("Visible") else "false",
                        "true" if payload.get("EnabledCron") else "false",
                    )

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    providers = get_providers_from_setting_files(
        os.path.join(base_dir, "config", "ftp_fetcher_settings.json"),
        os.path.join(base_dir, "config", "http_fetcher_settings.json"),
    )

    execute_query(
        connection,
        f"""
        INSERT INTO providers (id, code, name, is_visible, cron_status)
        VALUES
            {', '.join(str(item) for item in providers)}
        ON CONFLICT (name)
        DO
            UPDATE SET is_visible = EXCLUDED.is_visible, cron_status = EXCLUDED.cron_status ;
        """,  # noqa
    )


def main():
    connection = create_connection()
    create_table(connection)
    upsert_providers(connection)


if __name__ == "__main__":
    main()
