#!env/bin/python3

import os
import sys
import argparse
from urllib.parse import urlparse
import monitoring.rid_qualifier.test_executor as test_executor

def is_url(url_string):
    try:
        urlparse(url_string)
    except ValueError:
        raise ValueError("A valid injection_url must be passed")

def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exceute RID_Qualifier for a locale")

    parser.add_argument(
        "--auth",
        required = True,
        help="Auth spec for obtaining authorization to DSS instances; see README.md")

    parser.add_argument(
        "--locale",
        required = True,
        help="A three letter ISO 3166 country code to run the qualifier against, this should be the same one used to simulate the flight_data in flight_data_generator.py module.")

    parser.add_argument(
        "--injection_base_url",
        required = True,
        help="A USS url where the test data is to be submitted")

    parser.add_argument(
      "--observation_base_url",
      required = True,
      help="A USS url where the system data can be observed")


    return parser.parse_args()


def main() -> int:
    args = parseArgs()

    auth_spec = args.auth
    locale = args.locale
    injection_base_url = args.injection_base_url

    is_url(injection_base_url)
    uss_config = test_executor.build_uss_config(injection_base_url= injection_base_url)
    test_configuration = test_executor.build_test_configuration(locale = locale, auth_spec=auth_spec,uss_config = uss_config)

    test_executor.main(test_configuration=test_configuration, observation_base_url=args.observation_base_url)

    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())